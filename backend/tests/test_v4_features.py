"""CareerPilot AI v4 — fastembed + MongoDB chat_memory + startup indexes."""
import json
import time
import pytest


def _consume_sse(resp):
    full = ""
    for line in resp.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data: "):
            continue
        payload = line[6:]
        if payload == "[DONE]":
            break
        try:
            obj = json.loads(payload)
            if "delta" in obj:
                full += obj["delta"]
        except Exception:
            pass
    return full


# ---------- chat_memory collection schema in MongoDB ----------
def test_chat_memory_persisted_in_mongo_atlas(auth_client, base_url, mongo, test_user):
    """After a /chat/stream request, MongoDB chat_memory must contain documents
    with {user_id, role, content, embedding (list of 384 floats), ts}.
    """
    user_id, _ = test_user
    # clear any previous entries for the test user
    mongo.chat_memory.delete_many({"user_id": user_id})

    msg = "Probe message for v4 chat_memory persistence — please remember the word PINEAPPLE_V4."
    with auth_client.post(
        f"{base_url}/api/chat/stream",
        data=json.dumps({"message": msg}),
        headers={**auth_client.headers, "Accept": "text/event-stream"},
        stream=True, timeout=120,
    ) as r:
        assert r.status_code == 200, r.text
        _ = _consume_sse(r)

    # Give the async memory_store a moment
    time.sleep(2)

    docs = list(mongo.chat_memory.find({"user_id": user_id}))
    assert len(docs) >= 1, "no chat_memory document persisted in MongoDB Atlas"

    user_doc = next((d for d in docs if d.get("role") == "user"), None)
    assert user_doc is not None, "no user-role chat_memory doc found"
    for key in ("user_id", "role", "content", "embedding", "ts"):
        assert key in user_doc, f"missing key {key} in chat_memory doc"

    emb = user_doc["embedding"]
    assert isinstance(emb, list), "embedding must be a list"
    assert len(emb) == 384, f"BAAI/bge-small-en-v1.5 should yield 384 dims, got {len(emb)}"
    assert all(isinstance(x, (int, float)) for x in emb[:10]), "embedding entries must be numeric"
    assert user_doc["content"] == msg

    # cleanup
    mongo.chat_memory.delete_many({"user_id": user_id})


# ---------- Semantic recall via MongoDB cosine similarity (NOT Qdrant) ----------
def test_chat_stream_mongo_semantic_recall_rust_langgraph(auth_client, base_url, mongo, test_user):
    """Round-1 'I love Rust and LangGraph' followed by round-2 'What did I just say'.
    The assistant must reference Rust or LangGraph (recall from chat_memory)."""
    user_id, _ = test_user
    mongo.chat_memory.delete_many({"user_id": user_id})

    msg1 = "I love Rust and LangGraph — please remember this fact about me."
    with auth_client.post(
        f"{base_url}/api/chat/stream",
        data=json.dumps({"message": msg1}),
        headers={**auth_client.headers, "Accept": "text/event-stream"},
        stream=True, timeout=120,
    ) as r:
        assert r.status_code == 200, r.text
        _ = _consume_sse(r)

    time.sleep(2)

    msg2 = "What did I just say I love? Answer briefly in under 25 words."
    with auth_client.post(
        f"{base_url}/api/chat/stream",
        data=json.dumps({"message": msg2}),
        headers={**auth_client.headers, "Accept": "text/event-stream"},
        stream=True, timeout=120,
    ) as r:
        assert r.status_code == 200, r.text
        answer = _consume_sse(r).lower()

    assert answer, "no delta received on round 2"
    assert ("rust" in answer) or ("langgraph" in answer), (
        f"semantic recall failed — round-2 answer did not reference Rust/LangGraph: {answer!r}"
    )

    # cleanup
    mongo.chat_memory.delete_many({"user_id": user_id})


# ---------- Mongo indexes ensured on startup ----------
def test_mongo_indexes_created_on_startup(mongo):
    """Indexes must exist for users.user_id (unique), users.email (unique),
    user_sessions.session_token (unique), public_profiles.slug (unique), etc."""
    expected = {
        "users": [("user_id", True), ("email", True)],
        "user_sessions": [("session_token", True), ("user_id", False)],
        "public_profiles": [("slug", True)],
        "portfolios": [("user_id", True)],
        "chat_memory": [("user_id", False)],
        "resumes": [("user_id_1_created_at_-1", False)],
        "voice_interviews": [("user_id_1_created_at_-1", False)],
        "interviews": [("user_id_1_created_at_-1", False)],
        "chat_messages": [("user_id_1_ts_1", False)],
        "career_recommendations": [("user_id", False)],
        "skill_gaps": [("user_id_1_target_role_1", False)],
        "roadmaps": [("user_id_1_created_at_-1", False)],
        "career_twin": [("user_id_1_week_of_-1", False)],
    }
    for coll_name, expectations in expected.items():
        idxs = list(mongo[coll_name].list_indexes())
        for field_or_name, must_unique in expectations:
            matched = None
            for idx in idxs:
                key = idx.get("key") or {}
                name = idx.get("name", "")
                # single field index — key is {"<field>": 1/-1}
                if field_or_name in key and len(key) == 1:
                    matched = idx; break
                if name == field_or_name:
                    matched = idx; break
            assert matched is not None, (
                f"expected index on {coll_name}.{field_or_name} not found; existing: "
                f"{[i.get('name') for i in idxs]}"
            )
            if must_unique:
                assert matched.get("unique") is True, (
                    f"index {coll_name}.{field_or_name} should be unique"
                )
