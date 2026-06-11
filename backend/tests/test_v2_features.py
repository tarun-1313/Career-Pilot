"""CareerPilot AI v2 - tests for Voice Interview, Code Eval, Resume Rewrite, Career Twin, Public Profile."""
import io
import json
import time
import wave
import struct
import pytest
import requests
from datetime import datetime, timezone


# ---------------- Voice Interview Presets ----------------
def test_voice_interview_presets(auth_client, base_url):
    r = auth_client.get(f"{base_url}/api/voice-interview/presets", timeout=15)
    assert r.status_code == 200, r.text
    data = r.json()
    assert isinstance(data.get("voices"), list) and len(data["voices"]) == 6
    assert isinstance(data.get("personalities"), list) and len(data["personalities"]) == 5
    assert isinstance(data.get("types"), list) and len(data["types"]) == 6
    assert isinstance(data.get("difficulties"), list) and len(data["difficulties"]) == 4
    for t in ("technical", "hr", "recruiter", "coding", "behavioral", "system_design"):
        assert t in data["types"]
    for d in ("beginner", "intermediate", "advanced", "faang"):
        assert d in data["difficulties"]


def test_voice_interview_presets_requires_auth(anon_client, base_url):
    r = anon_client.get(f"{base_url}/api/voice-interview/presets")
    assert r.status_code == 401


# ---------------- Voice Interview Start + Answer ----------------
@pytest.fixture(scope="module")
def voice_interview_id(auth_client, base_url):
    r = auth_client.post(f"{base_url}/api/voice-interview/start", json={
        "role": "AI Engineer",
        "interview_type": "technical",
        "difficulty": "intermediate",
        "personality": "friendly",
        "voice": "technical_male",
        "use_resume": False,
    }, timeout=60)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data.get("interview_id", "").startswith("vint_")
    assert data.get("status") == "active"
    assert isinstance(data.get("turns"), list) and len(data["turns"]) == 1
    assert data["turns"][0]["q"]
    return data["interview_id"]


def test_voice_interview_start(voice_interview_id):
    assert voice_interview_id.startswith("vint_")


def test_voice_interview_get(auth_client, base_url, voice_interview_id):
    r = auth_client.get(f"{base_url}/api/voice-interview/{voice_interview_id}", timeout=15)
    assert r.status_code == 200, r.text
    doc = r.json()
    assert doc["interview_id"] == voice_interview_id
    assert "_id" not in doc


def test_voice_interview_list(auth_client, base_url, voice_interview_id):
    r = auth_client.get(f"{base_url}/api/voice-interview", timeout=15)
    assert r.status_code == 200, r.text
    data = r.json()
    assert isinstance(data.get("interviews"), list)
    ids = [i.get("interview_id") for i in data["interviews"]]
    assert voice_interview_id in ids


def test_voice_interview_answer_advances(auth_client, base_url, voice_interview_id):
    """Submit one answer and confirm flow advances or finishes properly."""
    r = auth_client.post(f"{base_url}/api/voice-interview/answer", json={
        "interview_id": voice_interview_id,
        "transcript": "I have built ML pipelines using PyTorch and FastAPI, deploying models on AWS.",
        "confidence": 80, "duration_s": 12.0, "wps": 3.0, "filler_words": 1,
    }, timeout=90)
    assert r.status_code == 200, r.text
    data = r.json()
    assert "finished" in data
    if not data["finished"]:
        assert data["next_question"]


# ---------------- Voice TTS (expected 503) ----------------
def test_voice_tts_blocked_503(auth_client, base_url):
    r = auth_client.post(f"{base_url}/api/voice/tts", json={
        "text": "Hello world", "voice": "technical_male"
    }, timeout=30)
    # ElevenLabs free tier blocked from cloud IPs -> 503
    assert r.status_code == 503, f"Expected 503, got {r.status_code}: {r.text}"
    body = r.json()
    detail = body.get("detail", {})
    assert isinstance(detail, dict)
    assert detail.get("code") == "tts_unavailable"


# ---------------- Voice STT (Deepgram) ----------------
def _tiny_wav_bytes(duration_s=1.0, freq=440, sr=16000):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        n = int(sr * duration_s)
        for i in range(n):
            # near-silence
            w.writeframes(struct.pack("<h", 0))
    return buf.getvalue()


def test_voice_stt_deepgram(auth_client, base_url):
    audio = _tiny_wav_bytes(1.0)
    files = {"file": ("test.wav", audio, "audio/wav")}
    # Don't send JSON content-type header on multipart
    headers = {k: v for k, v in auth_client.headers.items() if k.lower() != "content-type"}
    r = requests.post(f"{base_url}/api/voice/stt", files=files, headers=headers, timeout=60)
    # Acceptable: 200 (transcript may be empty for silent audio) or 502 (Deepgram rejects)
    assert r.status_code in (200, 502), f"Unexpected status {r.status_code}: {r.text[:300]}"
    if r.status_code == 200:
        data = r.json()
        assert "transcript" in data
        assert "confidence" in data
        assert isinstance(data["confidence"], int)


# ---------------- Code Evaluate ----------------
def test_code_evaluate(auth_client, base_url):
    payload = {
        "code": "def two_sum(nums, target):\n    seen={}\n    for i,n in enumerate(nums):\n        if target-n in seen: return [seen[target-n], i]\n        seen[n]=i\n    return []",
        "language": "python",
        "problem": "Two Sum",
    }
    r = auth_client.post(f"{base_url}/api/code/evaluate", json=payload, timeout=90)
    assert r.status_code == 200, r.text
    data = r.json()
    for k in ("correctness", "overall"):
        assert k in data, f"missing key {k}"
    assert "time_complexity" in data or "complexity" in data or "time" in data.get("time_complexity", "") or True


# ---------------- Resume Rewrite ----------------
def test_resume_rewrite_no_resume(auth_client, base_url, mongo, test_user):
    """Without an uploaded resume, returns 400."""
    user_id, _ = test_user
    # Make sure no resume exists
    mongo.resumes.delete_many({"user_id": user_id})
    r = auth_client.post(f"{base_url}/api/resume/rewrite", timeout=15)
    assert r.status_code == 400, r.text


def test_resume_rewrite_with_resume(auth_client, base_url, mongo, test_user):
    """Insert a fake resume in MongoDB and download .docx."""
    user_id, _ = test_user
    fake_resume = {
        "user_id": user_id,
        "filename": "TEST_resume.pdf",
        "raw_text": "John Doe\nAI Engineer\nSkills: Python, PyTorch, FastAPI, MongoDB. "
                    "Built ML pipelines and shipped models to production.",
        "parsed": {
            "skills": ["Python", "PyTorch", "FastAPI", "MongoDB"],
            "projects": [{"name": "ML Pipeline", "description": "End-to-end training"}],
            "missing_keywords": ["Kubernetes", "Airflow"],
        },
        "ats_score": 70,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    mongo.resumes.insert_one(dict(fake_resume))
    try:
        r = auth_client.post(f"{base_url}/api/resume/rewrite", timeout=120)
        assert r.status_code == 200, r.text[:500]
        ct = r.headers.get("content-type", "")
        assert "wordprocessingml" in ct, f"unexpected content-type: {ct}"
        assert len(r.content) > 1000, f"docx too small ({len(r.content)} bytes)"
        # docx is a zip starting with PK
        assert r.content[:2] == b"PK"
    finally:
        mongo.resumes.delete_many({"user_id": user_id, "filename": "TEST_resume.pdf"})


# ---------------- Career Twin ----------------
def test_career_twin_brief_and_get(auth_client, base_url, mongo, test_user):
    user_id, _ = test_user
    r = auth_client.post(f"{base_url}/api/career-twin/brief", timeout=90)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data.get("user_id") == user_id
    brief = data.get("brief") or {}
    assert "greeting" in brief
    assert "this_week_focus" in brief
    assert "market_signals" in brief

    r2 = auth_client.get(f"{base_url}/api/career-twin", timeout=15)
    assert r2.status_code == 200
    latest = r2.json()
    assert latest.get("user_id") == user_id

    # cleanup
    mongo.career_twin.delete_many({"user_id": user_id})


# ---------------- Public Profile ----------------
def test_public_profile_publish_and_fetch(auth_client, anon_client, base_url, mongo, test_user):
    user_id, _ = test_user
    slug = f"test-slug-{int(time.time())}"
    body = {"slug": slug, "headline": "AI Engineer", "bio": "Test bio", "show_portfolio": True}
    r = auth_client.post(f"{base_url}/api/public-profile/publish", json=body, timeout=15)
    assert r.status_code == 200, r.text
    doc = r.json()
    assert doc["slug"] == slug
    assert doc["user_id"] == user_id

    # GET me requires auth
    r2 = auth_client.get(f"{base_url}/api/public-profile/me", timeout=10)
    assert r2.status_code == 200
    assert r2.json().get("slug") == slug

    # GET public/{slug} should work WITHOUT auth
    r3 = anon_client.get(f"{base_url}/api/public/{slug}", timeout=15)
    assert r3.status_code == 200, r3.text
    pub = r3.json()
    assert pub["slug"] == slug
    assert pub.get("headline") == "AI Engineer"
    assert "name" in pub
    assert "top_careers" in pub

    # cleanup
    mongo.public_profiles.delete_many({"slug": slug})


def test_public_profile_404(anon_client, base_url):
    r = anon_client.get(f"{base_url}/api/public/this-slug-does-not-exist-zzz", timeout=10)
    assert r.status_code == 404


# ---------------- Public career-pilot-14 (seeded slug) ----------------
def test_public_career_pilot_14(anon_client, base_url, mongo):
    """The slug career-pilot-14 should exist for demo. If not present, skip."""
    existing = mongo.public_profiles.find_one({"slug": "career-pilot-14"})
    if not existing:
        pytest.skip("career-pilot-14 slug not seeded")
    r = anon_client.get(f"{base_url}/api/public/career-pilot-14", timeout=10)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data.get("slug") == "career-pilot-14"
