"""CareerPilot AI - end-to-end backend API tests."""
import json
import time
import pytest


# ---------- health & auth ----------
def test_health(anon_client, base_url):
    r = anon_client.get(f"{base_url}/api/")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "ok"
    assert data.get("service") == "CareerPilot AI"


def test_auth_me_unauthenticated(anon_client, base_url):
    r = anon_client.get(f"{base_url}/api/auth/me")
    assert r.status_code == 401


def test_auth_google_session_bogus(anon_client, base_url):
    r = anon_client.post(f"{base_url}/api/auth/google/session", json={"session_id": "BOGUS_ID_DOES_NOT_EXIST"})
    assert r.status_code in (401, 400)


def test_auth_me_with_session(auth_client, base_url, test_user):
    user_id, _ = test_user
    r = auth_client.get(f"{base_url}/api/auth/me")
    assert r.status_code == 200
    data = r.json()
    assert data["user_id"] == user_id
    assert "_id" not in data


# ---------- profile ----------
def test_profile_update(auth_client, base_url):
    payload = {"name": "TEST Updated", "degree": "B.Tech CSE", "graduation_year": 2025, "skills": ["Python", "FastAPI", "MongoDB"]}
    r = auth_client.put(f"{base_url}/api/profile", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "TEST Updated"
    assert data["degree"] == "B.Tech CSE"
    assert data["onboarded"] is True
    assert "FastAPI" in data["skills"]
    # verify persistence
    r2 = auth_client.get(f"{base_url}/api/auth/me")
    assert r2.json()["name"] == "TEST Updated"


def test_resume_latest_empty(auth_client, base_url):
    r = auth_client.get(f"{base_url}/api/resume/latest")
    assert r.status_code == 200
    assert r.json() == {}


# ---------- AI: careers ----------
def test_careers_recommend(auth_client, base_url):
    r = auth_client.post(f"{base_url}/api/careers/recommend", json={}, timeout=60)
    assert r.status_code == 200, r.text
    data = r.json()
    assert "careers" in data
    assert isinstance(data["careers"], list)
    assert len(data["careers"]) >= 1
    c0 = data["careers"][0]
    assert "name" in c0
    assert "match_score" in c0


def test_careers_list_persisted(auth_client, base_url):
    r = auth_client.get(f"{base_url}/api/careers")
    assert r.status_code == 200
    assert isinstance(r.json().get("careers"), list)


# ---------- skill gap ----------
def test_skill_gap(auth_client, base_url):
    r = auth_client.post(f"{base_url}/api/skills/gap", json={"role": "AI Engineer"}, timeout=60)
    assert r.status_code == 200, r.text
    data = r.json()
    assert "missing_skills" in data
    assert isinstance(data["missing_skills"], list)


# ---------- roadmap ----------
def test_roadmap_flow(auth_client, base_url):
    # NOTE: backend uses Dict[str, str] so months must be string (frontend already converts)
    r = auth_client.post(f"{base_url}/api/roadmap/generate", json={"role": "ML Engineer", "months": "3"}, timeout=90)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data.get("target_role") == "ML Engineer"
    months = data.get("data", {}).get("months", [])
    assert isinstance(months, list) and len(months) >= 1

    r2 = auth_client.get(f"{base_url}/api/roadmap")
    assert r2.status_code == 200
    assert r2.json().get("target_role") == "ML Engineer"

    r3 = auth_client.post(f"{base_url}/api/roadmap/milestone/toggle", json={"key": "1-week-1"})
    assert r3.status_code == 200
    assert "1-week-1" in r3.json().get("completed_milestones", [])

    r4 = auth_client.post(f"{base_url}/api/roadmap/milestone/toggle", json={"key": "1-week-1"})
    assert r4.status_code == 200
    assert "1-week-1" not in r4.json().get("completed_milestones", [])


# ---------- courses ----------
def test_courses_search(auth_client, base_url):
    r = auth_client.get(f"{base_url}/api/courses/search", params={"q": "langchain"}, timeout=30)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["query"] == "langchain"
    assert isinstance(data["results"], list)
    assert len(data["results"]) >= 1
    item = data["results"][0]
    assert item["provider"] == "YouTube"
    assert item["url"].startswith("https://www.youtube.com/")


# ---------- jobs ----------
def test_jobs_search(auth_client, base_url):
    r = auth_client.get(f"{base_url}/api/jobs/search", params={"q": "AI Engineer", "location": "India"}, timeout=45)
    assert r.status_code == 200, r.text
    data = r.json()
    assert isinstance(data.get("results"), list)
    if data["results"]:
        first = data["results"][0]
        assert "match_score" in first
        assert isinstance(first["match_score"], int)


# ---------- portfolio ----------
def test_portfolio_analyze(auth_client, base_url):
    r = auth_client.post(f"{base_url}/api/portfolio/analyze", json={"github_url": "https://github.com/torvalds"}, timeout=90)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data.get("username") == "torvalds"
    assert isinstance(data.get("repos"), list) and len(data["repos"]) >= 1
    assert "analysis" in data


# ---------- trends ----------
def test_trends(auth_client, base_url):
    r = auth_client.get(f"{base_url}/api/trends", timeout=60)
    assert r.status_code == 200, r.text
    data = r.json()
    for key in ("trending_tech", "high_demand_roles", "salary_shifts", "ai_focus_areas"):
        assert key in data, f"missing key {key}"


# ---------- salary ----------
def test_salary_predict(auth_client, base_url):
    r = auth_client.post(f"{base_url}/api/salary/predict",
                         json={"role": "AI Engineer", "experience_years": 2, "location": "India", "skills": ["Python"]},
                         timeout=60)
    assert r.status_code == 200, r.text
    data = r.json()
    assert "india_range_inr" in data


# ---------- interview ----------
def test_interview_start_and_answer(auth_client, base_url):
    r = auth_client.post(f"{base_url}/api/interview/start", json={"role": "AI Engineer"}, timeout=60)
    assert r.status_code == 200, r.text
    doc = r.json()
    iid = doc["interview_id"]
    assert doc["qa"][0]["q"]

    r2 = auth_client.post(f"{base_url}/api/interview/answer",
                          json={"interview_id": iid, "answer": "I have 2 years of experience building ML models with PyTorch."},
                          timeout=90)
    assert r2.status_code == 200, r2.text
    data = r2.json()
    assert "finished" in data
    if not data["finished"]:
        assert data["next_question"]


# ---------- chat stream ----------
def test_chat_stream_sse(auth_client, base_url):
    headers = dict(auth_client.headers)
    with auth_client.post(
        f"{base_url}/api/chat/stream",
        data=json.dumps({"message": "Give me one tip to crack an AI engineer interview in under 30 words."}),
        headers=headers, stream=True, timeout=90,
    ) as r:
        assert r.status_code == 200, r.text
        assert "text/event-stream" in r.headers.get("content-type", "")
        saw_delta = False
        saw_done = False
        for line in r.iter_lines(decode_unicode=True):
            if not line:
                continue
            if line.startswith("data: "):
                payload = line[6:]
                if payload == "[DONE]":
                    saw_done = True
                    break
                try:
                    obj = json.loads(payload)
                    if "delta" in obj:
                        saw_delta = True
                except Exception:
                    pass
        assert saw_delta, "no delta chunks received"
        assert saw_done, "no [DONE] terminator"


# ---------- progress ----------
def test_progress(auth_client, base_url):
    r = auth_client.get(f"{base_url}/api/progress")
    assert r.status_code == 200
    data = r.json()
    for k in ("roadmap_total", "roadmap_done", "roadmap_percent", "interviews_taken", "resumes_uploaded", "ats_score", "skills_count"):
        assert k in data
        assert isinstance(data[k], int)
