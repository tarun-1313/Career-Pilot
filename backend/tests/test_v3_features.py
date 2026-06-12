"""CareerPilot AI v3 — Qdrant semantic memory, emotion log, PDF export, STT WS."""
import asyncio
import json
import time
from urllib.parse import urlparse

import pytest
import requests
import websockets


# ---------- Qdrant semantic recall in chat/stream ----------
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


def test_chat_stream_qdrant_semantic_recall(auth_client, base_url):
    """Round-1: assert love of Python/FastAPI. Round-2: ask 'what did I say I love?'.

    The Qdrant Filter object (which previously could throw) must not raise; the
    second answer should reference Python or FastAPI from past memory.
    """
    msg1 = "Hey mentor — I want to be honest: I really love Python and FastAPI. Please remember this."
    with auth_client.post(
        f"{base_url}/api/chat/stream",
        data=json.dumps({"message": msg1}),
        headers={**auth_client.headers, "Accept": "text/event-stream"},
        stream=True, timeout=90,
    ) as r:
        assert r.status_code == 200, r.text
        _ = _consume_sse(r)

    # Give Qdrant a moment to index the assistant turn as well
    time.sleep(2)

    msg2 = "Quick check: what did I say I love? Answer in under 20 words."
    with auth_client.post(
        f"{base_url}/api/chat/stream",
        data=json.dumps({"message": msg2}),
        headers={**auth_client.headers, "Accept": "text/event-stream"},
        stream=True, timeout=90,
    ) as r:
        assert r.status_code == 200, r.text
        answer = _consume_sse(r).lower()

    assert answer, "no delta received on round 2"
    assert ("python" in answer) or ("fastapi" in answer), (
        f"semantic recall failed — round-2 answer did not reference round-1 fact: {answer!r}"
    )


# ---------- Voice Interview Emotion frame ----------
@pytest.fixture(scope="module")
def vi_started(auth_client, base_url):
    r = auth_client.post(f"{base_url}/api/voice-interview/start", json={
        "role": "AI Engineer",
        "interview_type": "technical",
        "difficulty": "intermediate",
        "personality": "friendly",
        "voice": "technical_male",
        "use_resume": False,
    }, timeout=60)
    assert r.status_code == 200, r.text
    return r.json()["interview_id"]


def test_voice_interview_emotion_append(auth_client, base_url, vi_started, mongo, test_user):
    interview_id = vi_started
    payload = {
        "interview_id": interview_id,
        "turn_index": 0,
        "emotions": {"happy": 0.4, "neutral": 0.5, "surprised": 0.1},
    }
    r = auth_client.post(f"{base_url}/api/voice-interview/emotion", json=payload, timeout=15)
    assert r.status_code == 200, r.text
    assert r.json() == {"ok": True}

    user_id, _ = test_user
    doc = mongo.voice_interviews.find_one({"interview_id": interview_id, "user_id": user_id})
    assert doc is not None, "voice interview doc not found"
    log = doc.get("emotion_log") or []
    assert len(log) >= 1
    last = log[-1]
    assert last["turn_index"] == 0
    assert abs(last["emotions"]["happy"] - 0.4) < 1e-6


def test_voice_interview_emotion_requires_auth(anon_client, base_url, vi_started):
    r = anon_client.post(f"{base_url}/api/voice-interview/emotion", json={
        "interview_id": vi_started, "turn_index": 0, "emotions": {"neutral": 1.0},
    })
    assert r.status_code == 401


# ---------- PDF export ----------
def test_voice_interview_pdf_incomplete_returns_400(auth_client, base_url, vi_started):
    r = auth_client.get(f"{base_url}/api/voice-interview/{vi_started}/pdf", timeout=15)
    assert r.status_code == 400, r.text
    assert "not yet complete" in (r.text or "").lower()


def test_voice_interview_pdf_complete_returns_pdf(auth_client, base_url, mongo, test_user):
    """Seed a completed voice_interviews doc directly in Mongo and fetch PDF."""
    user_id, _ = test_user
    iid = f"vint_pdftest_{int(time.time()*1000)}"
    mongo.voice_interviews.insert_one({
        "interview_id": iid,
        "user_id": user_id,
        "role": "AI Engineer",
        "interview_type": "technical",
        "difficulty": "intermediate",
        "personality": "friendly",
        "voice": "technical_male",
        "status": "completed",
        "created_at": "2026-01-01T00:00:00+00:00",
        "turns": [
            {"q": "Tell me about yourself.", "a": "I am a software engineer with 2 yrs experience in ML."},
            {"q": "What is overfitting?", "a": "When a model memorizes the training data."},
        ],
        "report": {
            "overall": 82,
            "technical_score": 80,
            "communication_score": 85,
            "confidence_score": 80,
            "problem_solving_score": 78,
            "clarity_score": 88,
            "strengths": ["Clear communicator", "Solid ML basics"],
            "improvements": ["Deeper system design"],
            "recommended_topics": ["Transformers", "Vector DBs"],
            "suggested_projects": ["RAG chatbot"],
            "summary": "Strong fundamentals; expand on system design.",
        },
    })
    try:
        r = auth_client.get(f"{base_url}/api/voice-interview/{iid}/pdf", timeout=30)
        assert r.status_code == 200, r.text
        assert r.headers.get("content-type", "").startswith("application/pdf")
        assert r.content[:4] == b"%PDF", "response body is not a PDF"
        assert len(r.content) > 1000, "PDF body suspiciously small"
        cd = r.headers.get("content-disposition", "")
        assert iid in cd
    finally:
        mongo.voice_interviews.delete_one({"interview_id": iid})


def test_voice_interview_pdf_not_found(auth_client, base_url):
    r = auth_client.get(f"{base_url}/api/voice-interview/vint_does_not_exist/pdf", timeout=15)
    assert r.status_code == 404


# ---------- WebSocket /api/voice/stt-ws ----------
def _ws_url(base_url: str, path: str) -> str:
    p = urlparse(base_url)
    scheme = "wss" if p.scheme == "https" else "ws"
    return f"{scheme}://{p.netloc}{path}"


def test_stt_ws_rejects_missing_token(base_url):
    async def run():
        url = _ws_url(base_url, "/api/voice/stt-ws")
        # missing token -> server should send error then close with 4401
        try:
            async with websockets.connect(url, open_timeout=10, close_timeout=5) as ws:
                # may receive the error frame before close
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=5)
                    data = json.loads(msg)
                    assert data.get("type") == "error"
                except Exception:
                    pass
                # await close
                try:
                    await asyncio.wait_for(ws.wait_closed(), timeout=5)
                except Exception:
                    pass
                code = ws.close_code
                assert code == 4401, f"expected close code 4401, got {code}"
        except websockets.exceptions.ConnectionClosed as e:
            assert e.code == 4401, f"expected 4401, got {e.code}"

    asyncio.run(run())


def test_stt_ws_accepts_valid_token(base_url, test_user):
    user_id, token = test_user

    async def run():
        url = _ws_url(base_url, f"/api/voice/stt-ws?token={token}")
        async with websockets.connect(url, open_timeout=15, close_timeout=5) as ws:
            # The connection upgraded successfully. If Deepgram unreachable the server
            # would emit an "error" frame; otherwise it stays open waiting for audio.
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=4)
                # If we got a message, make sure it's NOT auth-rejection
                try:
                    data = json.loads(msg)
                    assert data.get("message") != "auth required"
                except Exception:
                    pass
            except asyncio.TimeoutError:
                # No message within 4s == socket is open and waiting for audio.
                pass

            assert ws.close_code is None or ws.close_code != 4401
            await ws.close()

    asyncio.run(run())
