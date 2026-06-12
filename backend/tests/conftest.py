"""Shared fixtures for CareerPilot AI backend tests."""
import os
import time
import pytest
import requests
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv

# Load backend/.env so MONGO_URL points to Atlas matching the running backend
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://career-pilot-14.preview.emergentagent.com").rstrip("/")
MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ.get("DB_NAME", "careerpilot")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def mongo():
    c = MongoClient(MONGO_URL)
    yield c[DB_NAME]
    c.close()


@pytest.fixture(scope="session")
def test_user(mongo):
    """Create a mock user + session and yield (user_id, session_token)."""
    ts = int(time.time() * 1000)
    user_id = f"user_test_{ts}"
    session_token = f"test_session_{ts}"
    mongo.users.insert_one({
        "user_id": user_id,
        "email": f"TEST_user_{ts}@example.com",
        "name": "TEST User",
        "picture": "https://via.placeholder.com/150",
        "created_at": "2026-01-01T00:00:00+00:00",
        "onboarded": False,
        "skills": ["Python", "Machine Learning", "SQL"],
        "interests": ["AI", "MLOps"],
        "career_goals": "AI Engineer",
    })
    # expires 7 days in future
    from datetime import datetime, timedelta, timezone
    expires = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
    mongo.user_sessions.insert_one({
        "user_id": user_id,
        "session_token": session_token,
        "expires_at": expires,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    yield user_id, session_token
    # cleanup
    mongo.users.delete_many({"user_id": user_id})
    mongo.user_sessions.delete_many({"user_id": user_id})
    mongo.resumes.delete_many({"user_id": user_id})
    mongo.career_recommendations.delete_many({"user_id": user_id})
    mongo.skill_gaps.delete_many({"user_id": user_id})
    mongo.roadmaps.delete_many({"user_id": user_id})
    mongo.portfolios.delete_many({"user_id": user_id})
    mongo.interviews.delete_many({"user_id": user_id})
    mongo.chat_messages.delete_many({"user_id": user_id})


@pytest.fixture(scope="session")
def auth_client(test_user):
    user_id, token = test_user
    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    return s


@pytest.fixture(scope="session")
def anon_client():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s
