"""CareerPilot AI - FastAPI backend."""
import os
import io
import json
import uuid
<<<<<<< HEAD
import base64
=======
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
import logging
import asyncio
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any

import httpx
<<<<<<< HEAD
import fitz
import docx as docx_lib
import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request, Response, UploadFile, File, Cookie, WebSocket, WebSocketDisconnect
=======
import fitz  # PyMuPDF
import docx as docx_lib
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request, Response, UploadFile, File, Cookie
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

<<<<<<< HEAD
# Import Gemini client
from gemini_client import gemini_generate_text, gemini_generate_json, gemini_stream_text, GEMINI_MODEL

# Third-party
from fastembed import TextEmbedding
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import websockets as ws_client

from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Load env
ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")

# Try Atlas URL first (MONGODB_URL), fallback to local (MONGO_URL)
MONGO_URL = os.environ.get("MONGODB_URL") or os.environ["MONGO_URL"]
DB_NAME = os.environ["DB_NAME"]
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
=======
from emergentintegrations.llm.chat import LlmChat, UserMessage, TextDelta, StreamDone

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")

MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ["DB_NAME"]
EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY")
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
YT_KEY = os.environ.get("YOUTUBE_API_KEY")
ADZUNA_APP_ID = os.environ.get("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.environ.get("ADZUNA_APP_KEY")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
<<<<<<< HEAD
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")

# DB
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
log = logging.getLogger("careerpilot")

# FastAPI
app = FastAPI(title="CareerPilot AI")
api = APIRouter(prefix="/api")


@app.get("/")
async def root():
    return {"service": "CareerPilot AI", "status": "ok", "version": "1.0.0"}

@api.get("/")
async def api_root():
    return {"service": "CareerPilot AI", "status": "ok", "version": "1.0.0"}
=======

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
log = logging.getLogger("careerpilot")

app = FastAPI(title="CareerPilot AI")
api = APIRouter(prefix="/api")

GEMINI_MODEL = ("gemini", "gemini-2.5-flash")
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b


# ---------- helpers ----------
def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def jsonable(doc: dict) -> dict:
    doc.pop("_id", None)
    return doc


<<<<<<< HEAD
async def get_current_user(request: Request, session_token: Optional[str] = Cookie(default=None)) -> dict:
=======
async def get_current_user(
    request: Request,
    session_token: Optional[str] = Cookie(default=None),
) -> dict:
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
    token = session_token
    if not token:
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth[7:]
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    sess = await db.user_sessions.find_one({"session_token": token}, {"_id": 0})
    if not sess:
        raise HTTPException(status_code=401, detail="Invalid session")

    exp = sess["expires_at"]
    if isinstance(exp, str):
        exp = datetime.fromisoformat(exp)
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    if exp < now_utc():
        raise HTTPException(status_code=401, detail="Session expired")

    user = await db.users.find_one({"user_id": sess["user_id"]}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


<<<<<<< HEAD
# ---------- Pydantic Models ----------
=======
# ---------- models ----------
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
class ProfileIn(BaseModel):
    name: Optional[str] = None
    education: Optional[str] = None
    degree: Optional[str] = None
    graduation_year: Optional[int] = None
    skills: List[str] = []
    interests: List[str] = []
    career_goals: Optional[str] = None
    preferred_industry: Optional[str] = None
    preferred_location: Optional[str] = None
    expected_salary: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None


class ChatIn(BaseModel):
    message: str
    session_id: Optional[str] = None


class InterviewStartIn(BaseModel):
    role: str
<<<<<<< HEAD
    interview_type: str = "technical"
=======
    interview_type: str = "technical"  # technical | hr | behavioral | system_design
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b


class InterviewAnswerIn(BaseModel):
    interview_id: str
    answer: str


class SalaryPredictIn(BaseModel):
    role: str
    experience_years: int = 0
    location: str = "India"
    skills: List[str] = []


<<<<<<< HEAD
class VoiceInterviewStart(BaseModel):
    role: str
    interview_type: str = "technical"
    difficulty: str = "intermediate"
    personality: str = "friendly"
    voice: str = "technical_male"
    use_resume: bool = True


class VoiceInterviewAnswer(BaseModel):
    interview_id: str
    transcript: str
    confidence: Optional[int] = None
    duration_s: Optional[float] = None
    wps: Optional[float] = None
    filler_words: Optional[int] = None
    code: Optional[str] = None
    language: Optional[str] = None


class EmotionFrame(BaseModel):
    interview_id: str
    turn_index: int
    emotions: Dict[str, float]


class PublishIn(BaseModel):
    slug: str
    bio: Optional[str] = None
    headline: Optional[str] = None
    show_resume: bool = False
    show_portfolio: bool = True


# ---------- Gemini helper ----------
async def _gemini_json(system: str, user_text: str) -> dict:
    try:
        return await gemini_generate_json(prompt=user_text, system_message=system, temperature=0.2)
    except Exception as e:
        log.warning("Gemini JSON parse failed; error=%s", str(e)[:200])
        return {}


# ---------- Embedding helpers ----------
_embedder: Optional[TextEmbedding] = None
def get_embedder() -> TextEmbedding:
    global _embedder
    if _embedder is None:
        _embedder = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
        log.info("fastembed loaded")
    return _embedder


async def embed_text(text: str) -> List[float]:
    def _embed():
        vecs = list(get_embedder().embed([text]))
        return vecs[0].tolist() if vecs else []
    return await asyncio.to_thread(_embed)


def cosine(a: List[float], b: List[float]) -> float:
    if not a or not b:
        return 0.0
    av, bv = np.array(a, dtype=np.float32), np.array(b, dtype=np.float32)
    denom = float(np.linalg.norm(av) * np.linalg.norm(bv))
    return float(av @ bv / denom) if denom else 0.0


async def memory_search(user_id: str, query: str, k: int = 5) -> List[dict]:
    try:
        qv = await embed_text(query)
        docs = await db.chat_memory.find({"user_id": user_id}, {"_id": 0}).to_list(500)
        scored = [(cosine(qv, d.get("embedding") or []), d) for d in docs]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in scored[:k]]
    except Exception as e:
        log.warning("memory_search failed: %s", e)
        return []


async def memory_store(user_id: str, role: str, content: str) -> None:
    try:
        vec = await embed_text(content)
        await db.chat_memory.insert_one({
            "user_id": user_id, "role": role, "content": content,
            "embedding": vec, "ts": now_utc().isoformat(),
        })
    except Exception as e:
        log.warning("memory_store failed: %s", e)


# ---------- Voice & TTS ----------
el_client = ElevenLabs(api_key=ELEVENLABS_API_KEY) if ELEVENLABS_API_KEY else None

VOICE_PRESETS = {
    "technical_male": {"voice_id": "JBFqnCBsd6RMkjVDRZzb", "label": "George — Technical Interviewer", "gender": "male"},
    "technical_female": {"voice_id": "EXAVITQu4vr4xnSDxMaL", "label": "Sarah — Senior Engineer", "gender": "female"},
    "hr_female": {"voice_id": "XrExE9yKIg1WjnnlVkGX", "label": "Matilda — HR Recruiter", "gender": "female"},
    "hr_male": {"voice_id": "TX3LPaxmHKxFdv7VOQHJ", "label": "Liam — Recruiter", "gender": "male"},
    "faang_strict": {"voice_id": "onwK4e9ZLuTAKqWW03F9", "label": "Daniel — FAANG Lead", "gender": "male"},
    "startup_friendly": {"voice_id": "pFZP5JQG7iQjIQuC4Bku", "label": "Lily — Startup Manager", "gender": "female"},
}

PERSONALITIES = {
    "friendly": "warm and encouraging; ask follow-ups gently",
    "strict_faang": "rigorous FAANG-style interviewer; probe deeply, ask about edge cases and complexity",
    "startup": "casual startup recruiter; mix of culture and technical questions",
    "hr": "professional HR manager; focus on behavioral and soft skills",
    "technical_architect": "senior technical architect; focus on system design, scalability, trade-offs",
}


@api.post("/voice/tts")
async def voice_tts(payload: Dict[str, str], _: dict = Depends(get_current_user)):
    text = payload.get("text", "").strip()
    voice_key = payload.get("voice", "technical_male")
    if not text:
        raise HTTPException(400, "text required")
    if not el_client:
        raise HTTPException(status_code=503, detail={"code": "tts_unavailable", "message": "ElevenLabs not configured."})
    voice_id = VOICE_PRESETS.get(voice_key, VOICE_PRESETS["technical_male"])["voice_id"]

    def _gen() -> bytes:
        stream = el_client.text_to_speech.convert(
            text=text, voice_id=voice_id, model_id="eleven_turbo_v2_5",
            output_format="mp3_44100_128",
            voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.75, style=0.3, use_speaker_boost=True),
        )
        buf = b""
        for chunk in stream:
            if chunk:
                buf += chunk
        return buf

    audio_bytes = await asyncio.to_thread(_gen)
    b64 = base64.b64encode(audio_bytes).decode()
    return {"audio_b64": b64, "mime": "audio/mpeg", "voice_id": voice_id}


=======
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
# ---------- auth ----------
@api.post("/auth/google/session")
async def auth_google_session(payload: Dict[str, str], response: Response):
    """Exchange Emergent session_id (from URL fragment) for our session_token cookie."""
    session_id = payload.get("session_id")
    if not session_id:
        raise HTTPException(400, "session_id required")

    async with httpx.AsyncClient(timeout=15) as hx:
        r = await hx.get(
            "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
            headers={"X-Session-ID": session_id},
        )
    if r.status_code != 200:
        raise HTTPException(401, "Invalid Emergent session")
    data = r.json()
    email = data["email"]
    name = data.get("name", email.split("@")[0])
    picture = data.get("picture")
    session_token = data["session_token"]

    user = await db.users.find_one({"email": email}, {"_id": 0})
    if not user:
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        user = {
            "user_id": user_id,
            "email": email,
            "name": name,
            "picture": picture,
            "created_at": now_utc().isoformat(),
            "onboarded": False,
            "skills": [],
            "interests": [],
        }
        await db.users.insert_one(dict(user))
    else:
        await db.users.update_one({"email": email}, {"$set": {"name": name, "picture": picture}})
        user["name"] = name
        user["picture"] = picture

    expires = now_utc() + timedelta(days=7)
    await db.user_sessions.insert_one({
        "user_id": user["user_id"],
        "session_token": session_token,
        "expires_at": expires.isoformat(),
        "created_at": now_utc().isoformat(),
    })

<<<<<<< HEAD
    is_prod = os.environ.get("ENV") == "production"
=======
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
    response.set_cookie(
        key="session_token",
        value=session_token,
        max_age=7 * 24 * 3600,
        httponly=True,
<<<<<<< HEAD
        secure=is_prod,
        samesite="lax" if not is_prod else "none",
=======
        secure=True,
        samesite="none",
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
        path="/",
    )
    return jsonable(user)


@api.get("/auth/me")
async def auth_me(user: dict = Depends(get_current_user)):
    return user


@api.post("/auth/logout")
async def auth_logout(response: Response, request: Request, session_token: Optional[str] = Cookie(default=None)):
    if session_token:
        await db.user_sessions.delete_one({"session_token": session_token})
    response.delete_cookie("session_token", path="/")
    return {"ok": True}


# ---------- profile ----------
@api.put("/profile")
async def update_profile(body: ProfileIn, user: dict = Depends(get_current_user)):
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    updates["onboarded"] = True
    updates["updated_at"] = now_utc().isoformat()
    await db.users.update_one({"user_id": user["user_id"]}, {"$set": updates})
    new = await db.users.find_one({"user_id": user["user_id"]}, {"_id": 0})
    return new


# ---------- resume ----------
def _extract_pdf(buf: bytes) -> str:
    text = []
    with fitz.open(stream=buf, filetype="pdf") as doc:
        for page in doc:
            text.append(page.get_text())
    return "\n".join(text)


def _extract_docx(buf: bytes) -> str:
    f = io.BytesIO(buf)
    d = docx_lib.Document(f)
    return "\n".join(p.text for p in d.paragraphs)


<<<<<<< HEAD
=======
async def _gemini_json(system: str, user_text: str) -> dict:
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=f"oneshot_{uuid.uuid4().hex[:8]}",
        system_message=system,
    ).with_model(*GEMINI_MODEL)
    resp = await chat.send_message(UserMessage(text=user_text))
    txt = resp if isinstance(resp, str) else getattr(resp, "content", str(resp))
    # strip code fences
    s = txt.strip()
    if s.startswith("```"):
        s = s.strip("`")
        if s.lower().startswith("json"):
            s = s[4:]
    s = s.strip()
    # find first { ... last }
    a = s.find("{")
    b = s.rfind("}")
    if a >= 0 and b > a:
        s = s[a:b + 1]
    try:
        return json.loads(s)
    except Exception:
        log.warning("Gemini JSON parse failed; raw=%s", txt[:500])
        return {}


>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
@api.post("/resume/upload")
async def resume_upload(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    buf = await file.read()
    name = (file.filename or "").lower()
    if name.endswith(".pdf"):
        text = _extract_pdf(buf)
    elif name.endswith(".docx"):
        text = _extract_docx(buf)
    else:
        raise HTTPException(400, "Only .pdf or .docx supported")

    if not text.strip():
        raise HTTPException(400, "Could not extract text from resume")

    sys_prompt = (
        "You are an expert resume parser and ATS scorer. Return STRICT JSON only with keys: "
        "skills (list of strings), projects (list of {name, description}), certifications (list of strings), "
        "experience (list of {role, company, duration}), education (list of {degree, institution, year}), "
        "ats_score (int 0-100), strengths (list), improvements (list), missing_keywords (list of strings)."
    )
    parsed = await _gemini_json(sys_prompt, f"Parse and score this resume:\n\n{text[:12000]}")

    resume_id = f"res_{uuid.uuid4().hex[:12]}"
    doc = {
        "resume_id": resume_id,
        "user_id": user["user_id"],
        "filename": file.filename,
        "raw_text": text[:20000],
        "parsed": parsed,
        "ats_score": int(parsed.get("ats_score") or 0),
        "created_at": now_utc().isoformat(),
    }
    await db.resumes.insert_one(dict(doc))

    # update user skills
    if parsed.get("skills"):
        await db.users.update_one(
            {"user_id": user["user_id"]},
            {"$addToSet": {"skills": {"$each": parsed["skills"]}}},
        )
    return jsonable(doc)


@api.get("/resume/latest")
async def resume_latest(user: dict = Depends(get_current_user)):
    doc = await db.resumes.find_one(
        {"user_id": user["user_id"]}, {"_id": 0}, sort=[("created_at", -1)]
    )
    return doc or {}


# ---------- careers ----------
@api.post("/careers/recommend")
async def careers_recommend(user: dict = Depends(get_current_user)):
    sys_prompt = (
        "You are an AI career advisor. Recommend 5 career paths for the user. "
        "Return STRICT JSON: {careers: [{name, match_score (0-100 int), description, "
        "salary_range_inr (string e.g. '12-25 LPA'), demand_level ('Very High'|'High'|'Moderate'), "
        "growth_potential ('Excellent'|'Strong'|'Stable'), key_skills: [string]}]}"
    )
    profile = {
        "skills": user.get("skills", []),
        "interests": user.get("interests", []),
        "education": user.get("education"),
        "degree": user.get("degree"),
        "career_goals": user.get("career_goals"),
        "preferred_industry": user.get("preferred_industry"),
    }
    result = await _gemini_json(sys_prompt, f"User profile:\n{json.dumps(profile)}")
    careers = result.get("careers", [])
    await db.career_recommendations.delete_many({"user_id": user["user_id"]})
    if careers:
        await db.career_recommendations.insert_many([
            {"user_id": user["user_id"], "created_at": now_utc().isoformat(), **c} for c in careers
        ])
    return {"careers": careers}


@api.get("/careers")
async def careers_list(user: dict = Depends(get_current_user)):
    items = await db.career_recommendations.find(
        {"user_id": user["user_id"]}, {"_id": 0}
    ).to_list(20)
    return {"careers": items}


# ---------- skill gap ----------
@api.post("/skills/gap")
async def skill_gap(payload: Dict[str, str], user: dict = Depends(get_current_user)):
    target_role = payload.get("role") or user.get("career_goals") or "AI Engineer"
    sys_prompt = (
        "You are a skill-gap analyst. Return STRICT JSON: "
        "{target_role, current_skills:[string], required_skills:[string], "
        "missing_skills:[{name, priority('high'|'medium'|'low'), difficulty('beginner'|'intermediate'|'advanced'), estimated_weeks:int, reason}]}"
    )
    inp = {"target_role": target_role, "current_skills": user.get("skills", [])}
    result = await _gemini_json(sys_prompt, json.dumps(inp))
    await db.skill_gaps.update_one(
        {"user_id": user["user_id"], "target_role": target_role},
        {"$set": {**result, "user_id": user["user_id"], "target_role": target_role, "created_at": now_utc().isoformat()}},
        upsert=True,
    )
    return result


# ---------- roadmap ----------
@api.post("/roadmap/generate")
async def roadmap_generate(payload: Dict[str, str], user: dict = Depends(get_current_user)):
    target_role = payload.get("role") or user.get("career_goals") or "AI Engineer"
    months = int(payload.get("months") or 6)
    sys_prompt = (
        f"You are a career mentor. Generate a {months}-month personalized learning roadmap. "
        "Return STRICT JSON: {role, months:[{month:int, title:string, focus:string, "
        "weekly_goals:[string], projects:[string], certifications:[string]}]}"
    )
    inp = {"target_role": target_role, "current_skills": user.get("skills", []), "months": months}
    result = await _gemini_json(sys_prompt, json.dumps(inp))
    rid = f"road_{uuid.uuid4().hex[:10]}"
    doc = {
        "roadmap_id": rid, "user_id": user["user_id"], "target_role": target_role,
        "data": result, "completed_milestones": [],
        "created_at": now_utc().isoformat(),
    }
    await db.roadmaps.delete_many({"user_id": user["user_id"]})
    await db.roadmaps.insert_one(dict(doc))
    return jsonable(doc)


@api.get("/roadmap")
async def roadmap_get(user: dict = Depends(get_current_user)):
    doc = await db.roadmaps.find_one({"user_id": user["user_id"]}, {"_id": 0}, sort=[("created_at", -1)])
    return doc or {}


@api.post("/roadmap/milestone/toggle")
async def roadmap_toggle(payload: Dict[str, Any], user: dict = Depends(get_current_user)):
    key = payload.get("key")  # e.g. "1-week-1"
    if not key:
        raise HTTPException(400, "key required")
    doc = await db.roadmaps.find_one({"user_id": user["user_id"]})
    if not doc:
        raise HTTPException(404, "no roadmap")
    completed = set(doc.get("completed_milestones", []))
    if key in completed:
        completed.remove(key)
    else:
        completed.add(key)
    await db.roadmaps.update_one({"user_id": user["user_id"]}, {"$set": {"completed_milestones": list(completed)}})
    return {"completed_milestones": list(completed)}


# ---------- courses ----------
@api.get("/courses/search")
async def courses_search(q: str = "machine learning", user: dict = Depends(get_current_user)):
    items: List[Dict[str, Any]] = []
    if YT_KEY:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet", "q": f"{q} tutorial course", "type": "video",
            "maxResults": 12, "relevanceLanguage": "en", "key": YT_KEY,
        }
        async with httpx.AsyncClient(timeout=15) as hx:
            r = await hx.get(url, params=params)
        if r.status_code == 200:
            for v in r.json().get("items", []):
                vid = v["id"]["videoId"]
                sn = v["snippet"]
                items.append({
                    "id": vid,
                    "provider": "YouTube",
                    "title": sn["title"],
                    "channel": sn["channelTitle"],
                    "thumbnail": sn["thumbnails"]["high"]["url"],
                    "url": f"https://www.youtube.com/watch?v={vid}",
                    "description": sn.get("description", "")[:200],
                })
    return {"query": q, "results": items}


# ---------- jobs ----------
@api.get("/jobs/search")
async def jobs_search(q: str = "software engineer", location: str = "India", user: dict = Depends(get_current_user)):
    items: List[Dict[str, Any]] = []
<<<<<<< HEAD
    
    # First try JSearch (RapidAPI)
=======
    # try JSearch (RapidAPI) — broader coverage
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
    if RAPIDAPI_KEY:
        try:
            async with httpx.AsyncClient(timeout=20) as hx:
                r = await hx.get(
                    "https://jsearch.p.rapidapi.com/search",
<<<<<<< HEAD
                    headers={"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": "jsearch.p.rapidapi.com"},
=======
                    headers={
                        "X-RapidAPI-Key": RAPIDAPI_KEY,
                        "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
                    },
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
                    params={"query": f"{q} in {location}", "page": "1", "num_pages": "1"},
                )
            if r.status_code == 200:
                for j in (r.json().get("data") or [])[:12]:
                    items.append({
                        "id": j.get("job_id"),
                        "title": j.get("job_title"),
                        "company": j.get("employer_name"),
                        "location": ", ".join(filter(None, [j.get("job_city"), j.get("job_country")])),
<<<<<<< HEAD
                        "salary": f"{j.get('job_min_salary')}-{j.get('job_max_salary')} {j.get('job_salary_currency') or ''}" if j.get("job_min_salary") else "Not disclosed",
=======
                        "salary": (
                            f"{j.get('job_min_salary')}-{j.get('job_max_salary')} {j.get('job_salary_currency') or ''}"
                            if j.get("job_min_salary") else "Not disclosed"
                        ),
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
                        "url": j.get("job_apply_link"),
                        "description": (j.get("job_description") or "")[:280],
                        "remote": j.get("job_is_remote", False),
                        "posted": j.get("job_posted_at_datetime_utc"),
                    })
        except Exception as e:
            log.warning("JSearch failed: %s", e)
<<<<<<< HEAD
    
    # If no results from JSearch, try Adzuna as fallback
    if not items and ADZUNA_APP_ID and ADZUNA_APP_KEY:
        try:
            # Map location to Adzuna country code (simplified)
            country_code = "in"  # Default to India
            loc_lower = location.lower()
            if loc_lower in ["us", "united states", "usa"]: country_code = "us"
            if loc_lower in ["uk", "united kingdom", "england", "scotland", "wales"]: country_code = "gb"
            if loc_lower in ["ca", "canada"]: country_code = "ca"
            if loc_lower in ["au", "australia"]: country_code = "au"
            
            async with httpx.AsyncClient(timeout=20) as hx:
                adzuna_url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/1"
                params = {
                    "app_id": ADZUNA_APP_ID,
                    "app_key": ADZUNA_APP_KEY,
                    "results_per_page": 12,
                    "what": q,
                    "where": location,
                }
                r = await hx.get(adzuna_url, params=params)
                if r.status_code == 200:
                    adzuna_data = r.json()
                    for j in (adzuna_data.get("results", []))[:12]:
                        items.append({
                            "id": j.get("id"),
                            "title": j.get("title"),
                            "company": j.get("company", {}).get("display_name", "Unknown Company"),
                            "location": j.get("location", {}).get("display_name", location),
                            "salary": f"{j.get('salary_min', '')}-{j.get('salary_max', '')} {j.get('salary_currency', '')}" if j.get("salary_min") else "Not disclosed",
                            "url": j.get("redirect_url"),
                            "description": (j.get("description", "") or "")[:280],
                            "remote": "remote" in (j.get("title", "") + " " + j.get("description", "")).lower(),
                            "posted": j.get("created"),
                        })
        except Exception as e:
            log.warning("Adzuna failed: %s", e)
            
    # If both fail, generate AI mock jobs as final fallback using Gemini
    if not items:
        try:
            sys_prompt = (
                "You are a job search API. Generate 8 realistic job listings for the given role and location. "
                "Return STRICT JSON with a 'jobs' list where each job has: "
                "title, company, location, salary (string), url (can be fake but valid), description, remote (boolean). "
                "Make the jobs look real, with actual company names and plausible descriptions."
            )
            result = await _gemini_json(sys_prompt, f"Role: {q}, Location: {location}")
            for j in (result.get("jobs", []))[:8]:
                items.append({
                    "id": str(uuid.uuid4()),
                    "title": j.get("title"),
                    "company": j.get("company"),
                    "location": j.get("location"),
                    "salary": j.get("salary", "Not disclosed"),
                    "url": j.get("url", "#"),
                    "description": (j.get("description", "") or "")[:280],
                    "remote": j.get("remote", False),
                    "posted": now_utc().isoformat(),
                })
        except Exception as e:
            log.warning("Gemini mock jobs failed: %s", e)
            
    # User skills matching
=======

    # fallback to Adzuna
    if not items and ADZUNA_APP_ID and ADZUNA_APP_KEY:
        country = "in" if "india" in location.lower() else "gb"
        try:
            async with httpx.AsyncClient(timeout=20) as hx:
                r = await hx.get(
                    f"https://api.adzuna.com/v1/api/jobs/{country}/search/1",
                    params={
                        "app_id": ADZUNA_APP_ID, "app_key": ADZUNA_APP_KEY,
                        "results_per_page": 12, "what": q, "where": location,
                    },
                )
            if r.status_code == 200:
                for j in r.json().get("results", []):
                    items.append({
                        "id": str(j.get("id")),
                        "title": j.get("title"),
                        "company": (j.get("company") or {}).get("display_name"),
                        "location": (j.get("location") or {}).get("display_name"),
                        "salary": (
                            f"₹{int(j.get('salary_min',0)):,}-{int(j.get('salary_max',0)):,}"
                            if j.get("salary_min") else "Not disclosed"
                        ),
                        "url": j.get("redirect_url"),
                        "description": (j.get("description") or "")[:280],
                        "remote": False,
                        "posted": j.get("created"),
                    })
        except Exception as e:
            log.warning("Adzuna failed: %s", e)

    # compute match score
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
    user_skills = {s.lower() for s in user.get("skills", [])}
    for it in items:
        text = (it.get("title", "") + " " + it.get("description", "")).lower()
        hits = sum(1 for s in user_skills if s and s in text)
        it["match_score"] = min(100, 40 + hits * 12) if user_skills else 60

    items.sort(key=lambda x: x["match_score"], reverse=True)
    return {"query": q, "location": location, "results": items}


<<<<<<< HEAD
# ---------- chatbot ----------
@api.post("/chat/stream")
async def chat_stream(body: ChatIn, user: dict = Depends(get_current_user)):
    sid = body.session_id or f"chat_{user['user_id']}"
    profile_ctx = {
        "name": user.get("name"),
        "skills": user.get("skills", []),
        "career_goals": user.get("career_goals"),
        "education": user.get("education"),
    }

    # Persistent semantic recall from MongoDB Atlas
    recall_lines = []
    try:
        hits = await memory_search(user["user_id"], body.message, k=5)
        for h in hits:
            if h.get("role") and h.get("content"):
                recall_lines.append(f"[{h['role']}] {h['content'][:240]}")
    except Exception as e:
        log.warning("memory search err: %s", e)

    memory_block = ("\n".join(recall_lines[:5])) or "(no relevant past memory)"

    sys = (
        "You are CareerPilot AI, a friendly expert career mentor. "
        "Give concise, actionable, modern advice. Use bullet points where useful.\n"
        f"User context: {json.dumps(profile_ctx)}\n"
        f"Relevant past conversation memory:\n{memory_block}"
    )

    await db.chat_messages.insert_one({
        "user_id": user["user_id"], "session_id": sid,
        "role": "user", "content": body.message, "ts": now_utc().isoformat(),
    })
    await memory_store(user["user_id"], "user", body.message)

    async def gen():
        full = []
        try:
            async for chunk in gemini_stream_text(
                prompt=body.message,
                system_message=sys,
                temperature=0.7,
            ):
                full.append(chunk)
                yield f"data: {json.dumps({'delta': chunk})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        assistant_text = "".join(full)
        await db.chat_messages.insert_one({
            "user_id": user["user_id"], "session_id": sid,
            "role": "assistant", "content": assistant_text, "ts": now_utc().isoformat(),
        })
        if assistant_text:
            await memory_store(user["user_id"], "assistant", assistant_text)
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        gen(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@api.get("/chat/history")
async def chat_history(user: dict = Depends(get_current_user)):
    sid = f"chat_{user['user_id']}"
    msgs = await db.chat_messages.find(
        {"user_id": user["user_id"], "session_id": sid}, {"_id": 0}
    ).sort("ts", 1).to_list(200)
    return {"messages": msgs}


=======
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
# ---------- portfolio / github ----------
@api.post("/portfolio/analyze")
async def portfolio_analyze(payload: Dict[str, str], user: dict = Depends(get_current_user)):
    gh_url = payload.get("github_url") or user.get("github_url") or ""
    if "github.com/" not in gh_url:
        raise HTTPException(400, "Provide a valid GitHub URL")
    username = gh_url.rstrip("/").split("github.com/")[-1].split("/")[0]

    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    async with httpx.AsyncClient(timeout=20) as hx:
        user_r = await hx.get(f"https://api.github.com/users/{username}", headers=headers)
<<<<<<< HEAD
        repos_r = await hx.get(f"https://api.github.com/users/{username}/repos", headers=headers, params={"sort": "updated", "per_page": 20})
=======
        repos_r = await hx.get(
            f"https://api.github.com/users/{username}/repos",
            headers=headers, params={"sort": "updated", "per_page": 20},
        )
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
    if user_r.status_code != 200:
        raise HTTPException(404, f"GitHub user '{username}' not found")
    gh_user = user_r.json()
    repos = repos_r.json() if repos_r.status_code == 200 else []

    repo_summary = [{
        "name": r.get("name"),
        "description": r.get("description"),
        "language": r.get("language"),
        "stars": r.get("stargazers_count", 0),
        "forks": r.get("forks_count", 0),
        "url": r.get("html_url"),
        "has_pages": r.get("has_pages", False),
    } for r in repos[:15]]

    sys_prompt = (
        "You are a senior engineer reviewing a GitHub portfolio. Return STRICT JSON: "
        "{score:int 0-100, summary:string, strengths:[string], improvements:[string], top_projects:[{name, comment}]}"
    )
    profile_text = {
<<<<<<< HEAD
        "user": {"login": gh_user.get("login"), "name": gh_user.get("name"), "bio": gh_user.get("bio"), "followers": gh_user.get("followers"), "public_repos": gh_user.get("public_repos")},
=======
        "user": {
            "login": gh_user.get("login"), "name": gh_user.get("name"),
            "bio": gh_user.get("bio"), "followers": gh_user.get("followers"),
            "public_repos": gh_user.get("public_repos"),
        },
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
        "repos": repo_summary,
    }
    ai = await _gemini_json(sys_prompt, json.dumps(profile_text))

    out = {
<<<<<<< HEAD
        "username": username, "avatar": gh_user.get("avatar_url"), "name": gh_user.get("name") or username,
        "bio": gh_user.get("bio"), "public_repos": gh_user.get("public_repos", 0), "followers": gh_user.get("followers", 0),
        "repos": repo_summary, "analysis": ai, "created_at": now_utc().isoformat(),
    }
    await db.portfolios.update_one({"user_id": user["user_id"]}, {"$set": {"user_id": user["user_id"], **out}}, upsert=True)
=======
        "username": username,
        "avatar": gh_user.get("avatar_url"),
        "name": gh_user.get("name") or username,
        "bio": gh_user.get("bio"),
        "public_repos": gh_user.get("public_repos", 0),
        "followers": gh_user.get("followers", 0),
        "repos": repo_summary,
        "analysis": ai,
        "created_at": now_utc().isoformat(),
    }
    await db.portfolios.update_one(
        {"user_id": user["user_id"]},
        {"$set": {"user_id": user["user_id"], **out}},
        upsert=True,
    )
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
    if gh_url:
        await db.users.update_one({"user_id": user["user_id"]}, {"$set": {"github_url": gh_url}})
    return out


# ---------- salary ----------
@api.post("/salary/predict")
async def salary_predict(payload: SalaryPredictIn, user: dict = Depends(get_current_user)):
    sys_prompt = (
        "You are a compensation analyst. Return STRICT JSON: "
        "{role, experience_years, india_range_inr:string, remote_range_usd:string, "
        "international_range_usd:string, factors:[string], confidence(0-100 int)}"
    )
    inp = payload.model_dump()
    inp["user_skills"] = user.get("skills", [])
    res = await _gemini_json(sys_prompt, json.dumps(inp))
    return res


# ---------- trends ----------
@api.get("/trends")
async def trends(user: dict = Depends(get_current_user)):
    sys_prompt = (
        "Return STRICT JSON of industry trends for 2026: "
        "{trending_tech:[{name, momentum:int 1-100, category}], "
        "high_demand_roles:[{role, demand:int, growth:string}], "
        "salary_shifts:[{role, change_pct:int, note}], "
        "ai_focus_areas:[string]}"
    )
    res = await _gemini_json(sys_prompt, "Generate current tech industry trends.")
    return res

<<<<<<< HEAD
# ---------- progress ----------
@api.get("/progress")
async def progress(user: dict = Depends(get_current_user)):
    # Roadmap progress
    roadmap = await db.roadmaps.find_one({"user_id": user["user_id"]}, {"_id": 0})
    roadmap_total = 0
    roadmap_done = 0
    if roadmap and roadmap.get("data", {}).get("months"):
        months = roadmap["data"]["months"]
        roadmap_total = len(months) * 4  # approx 4 weeks per month
        roadmap_done = len(roadmap.get("completed_milestones", []))
    roadmap_percent = int((roadmap_done / roadmap_total * 100) if roadmap_total > 0 else 0)
    
    # Interviews taken
    interviews_taken = await db.interviews.count_documents({"user_id": user["user_id"]})
    
    # Resumes uploaded
    resumes_uploaded = await db.resumes.count_documents({"user_id": user["user_id"]})
    
    # ATS score
    latest_resume = await db.resumes.find_one({"user_id": user["user_id"]}, {"_id": 0}, sort=[("created_at", -1)])
    ats_score = latest_resume.get("ats_score", 0) if latest_resume else 0
    
    # Skills count
    skills_count = len(user.get("skills", []))
    
    return {
        "roadmap_total": roadmap_total,
        "roadmap_done": roadmap_done,
        "roadmap_percent": roadmap_percent,
        "interviews_taken": interviews_taken,
        "resumes_uploaded": resumes_uploaded,
        "ats_score": ats_score,
        "skills_count": skills_count
    }

# ---------- interview ----------
class InterviewStartIn(BaseModel):
    role: str
    interview_type: str = "technical"

class InterviewAnswerIn(BaseModel):
    interview_id: str
    answer: str

@api.post("/interview/start")
async def interview_start(payload: InterviewStartIn, user: dict = Depends(get_current_user)):
    interview_id = f"int_{uuid.uuid4().hex[:12]}"
    sys_prompt = f"You are a {payload.interview_type} interviewer for the role of {payload.role}. Ask the first question. Return STRICT JSON with 'question': string"
    res = await _gemini_json(sys_prompt, "Ask the first interview question.")
    question = res.get("question", "Tell me about yourself.")
    doc = {
        "interview_id": interview_id,
        "user_id": user["user_id"],
        "role": payload.role,
        "interview_type": payload.interview_type,
        "status": "active",
        "created_at": now_utc().isoformat(),
        "qa": [{"q": question}]
=======

# ---------- chatbot ----------
@api.post("/chat/stream")
async def chat_stream(body: ChatIn, user: dict = Depends(get_current_user)):
    sid = body.session_id or f"chat_{user['user_id']}"
    profile_ctx = {
        "name": user.get("name"),
        "skills": user.get("skills", []),
        "career_goals": user.get("career_goals"),
        "education": user.get("education"),
    }

    # Persistent semantic recall from MongoDB Atlas
    recall_lines = []
    try:
        hits = await memory_search(user["user_id"], body.message, k=5)
        for h in hits:
            if h.get("role") and h.get("content"):
                recall_lines.append(f"[{h['role']}] {h['content'][:240]}")
    except Exception as e:
        log.warning("memory search err: %s", e)

    memory_block = ("\n".join(recall_lines[:5])) or "(no relevant past memory)"

    sys = (
        "You are CareerPilot AI, a friendly expert career mentor. "
        "Give concise, actionable, modern advice. Use bullet points where useful.\n"
        f"User context: {json.dumps(profile_ctx)}\n"
        f"Relevant past conversation memory:\n{memory_block}"
    )
    chat = LlmChat(api_key=EMERGENT_LLM_KEY, session_id=sid, system_message=sys).with_model(*GEMINI_MODEL)

    await db.chat_messages.insert_one({
        "user_id": user["user_id"], "session_id": sid,
        "role": "user", "content": body.message, "ts": now_utc().isoformat(),
    })
    # persist to Atlas-backed vector memory
    await memory_store(user["user_id"], "user", body.message)

    async def gen():
        full = []
        try:
            async for ev in chat.stream_message(UserMessage(text=body.message)):
                if isinstance(ev, TextDelta):
                    full.append(ev.content)
                    yield f"data: {json.dumps({'delta': ev.content})}\n\n"
                elif isinstance(ev, StreamDone):
                    break
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        assistant_text = "".join(full)
        await db.chat_messages.insert_one({
            "user_id": user["user_id"], "session_id": sid,
            "role": "assistant", "content": assistant_text, "ts": now_utc().isoformat(),
        })
        if assistant_text:
            await memory_store(user["user_id"], "assistant", assistant_text)
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        gen(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@api.get("/chat/history")
async def chat_history(user: dict = Depends(get_current_user)):
    sid = f"chat_{user['user_id']}"
    msgs = await db.chat_messages.find(
        {"user_id": user["user_id"], "session_id": sid}, {"_id": 0}
    ).sort("ts", 1).to_list(200)
    return {"messages": msgs}


# ---------- mock interview ----------
@api.post("/interview/start")
async def interview_start(body: InterviewStartIn, user: dict = Depends(get_current_user)):
    iid = f"int_{uuid.uuid4().hex[:10]}"
    sys = (
        f"You are an interviewer conducting a {body.interview_type} interview for the role of {body.role}. "
        "Ask ONE question at a time, then wait. After the candidate answers, evaluate briefly and ask the next question. "
        "After 5 questions, return a STRICT JSON final report wrapped in <report> tags with keys: "
        "technical_score(0-100), confidence_score(0-100), communication_score(0-100), overall(0-100), "
        "strengths:[string], improvements:[string], summary:string."
    )
    chat = LlmChat(api_key=EMERGENT_LLM_KEY, session_id=iid, system_message=sys).with_model(*GEMINI_MODEL)
    resp = await chat.send_message(UserMessage(text=f"Begin the interview for {body.role}. Ask the first question."))
    first_q = resp if isinstance(resp, str) else getattr(resp, "content", str(resp))

    doc = {
        "interview_id": iid, "user_id": user["user_id"], "role": body.role,
        "interview_type": body.interview_type, "qa": [{"q": first_q, "a": None}],
        "status": "active", "created_at": now_utc().isoformat(),
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
    }
    await db.interviews.insert_one(dict(doc))
    return jsonable(doc)

<<<<<<< HEAD
@api.post("/interview/answer")
async def interview_answer(payload: InterviewAnswerIn, user: dict = Depends(get_current_user)):
    interview = await db.interviews.find_one({"interview_id": payload.interview_id, "user_id": user["user_id"]})
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    # Update last QA with answer
    qa = interview["qa"]
    qa[-1]["a"] = payload.answer
    
    # Ask next question or finish
    sys_prompt = f"You are a {interview['interview_type']} interviewer for {interview['role']}. Given the conversation history, ask the next question. If you think we've asked enough questions, return {{'finished': true, 'feedback': string}}. Otherwise return {{'question': string}}."
    history = json.dumps(qa)
    res = await _gemini_json(sys_prompt, history)
    if res.get("finished"):
        await db.interviews.update_one({"interview_id": payload.interview_id}, {"$set": {"status": "completed", "qa": qa, "feedback": res.get("feedback")}})
        return {"finished": True, "feedback": res.get("feedback")}
    else:
        question = res.get("question", "Thank you, that's all for today.")
        qa.append({"q": question})
        await db.interviews.update_one({"interview_id": payload.interview_id}, {"$set": {"qa": qa}})
        return {"finished": False, "next_question": question}

@api.get("/interview/history")
async def interview_history(user: dict = Depends(get_current_user)):
    interviews = await db.interviews.find({"user_id": user["user_id"]}, {"_id": 0}).sort("created_at", -1).to_list(50)
    return {"interviews": interviews}

# ---------- voice-interview ----------
@api.get("/voice-interview/presets")
async def voice_interview_presets(user: dict = Depends(get_current_user)):
    voices = [{"key": k, **v} for k, v in VOICE_PRESETS.items()]
    personalities = [{"key": k, "label": k.replace("_", " ").title(), "desc": v} for k, v in PERSONALITIES.items()]
    types = ["technical", "hr", "recruiter", "coding", "behavioral", "system_design"]
    difficulties = ["beginner", "intermediate", "advanced", "faang"]
    return {"voices": voices, "personalities": personalities, "types": types, "difficulties": difficulties}

@api.post("/voice-interview/start")
async def voice_interview_start(payload: VoiceInterviewStart, user: dict = Depends(get_current_user)):
    interview_id = f"vint_{uuid.uuid4().hex[:12]}"
    # Get resume if needed
    resume_context = ""
    if payload.use_resume:
        resume = await db.resumes.find_one({"user_id": user["user_id"]}, {"_id": 0}, sort=[("created_at", -1)])
        if resume:
            resume_context = f"Candidate's resume: {resume.get('raw_text', '')}"
    sys_prompt = (
        f"You are a {payload.personality} {payload.interview_type} interviewer for the role of {payload.role}. "
        f"{payload.difficulty} difficulty. Ask the first question. Return STRICT JSON with 'question': string"
    )
    res = await _gemini_json(sys_prompt, f"{resume_context} Ask the first interview question.")
    question = res.get("question", "Tell me about yourself.")
    doc = {
        "interview_id": interview_id,
        "user_id": user["user_id"],
        "role": payload.role,
        "interview_type": payload.interview_type,
        "difficulty": payload.difficulty,
        "personality": payload.personality,
        "voice": payload.voice,
        "use_resume": payload.use_resume,
        "status": "active",
        "created_at": now_utc().isoformat(),
        "turns": [{"q": question}],
        "emotion_log": []
=======

@api.post("/interview/answer")
async def interview_answer(body: InterviewAnswerIn, user: dict = Depends(get_current_user)):
    doc = await db.interviews.find_one({"interview_id": body.interview_id, "user_id": user["user_id"]}, {"_id": 0})
    if not doc:
        raise HTTPException(404, "interview not found")

    iid = body.interview_id
    sys = (
        f"You are an interviewer conducting a {doc['interview_type']} interview for the role of {doc['role']}. "
        "Ask ONE question at a time. After 5 total questions, output ONLY a JSON report wrapped in <report>...</report> tags "
        "with keys: technical_score, confidence_score, communication_score, overall, strengths, improvements, summary."
    )
    chat = LlmChat(api_key=EMERGENT_LLM_KEY, session_id=iid, system_message=sys).with_model(*GEMINI_MODEL)

    # replay prior turns
    qa = doc["qa"]
    for turn in qa:
        if turn.get("a"):
            await chat.send_message(UserMessage(text=turn["a"]))

    # last open question -> answer it
    if qa and qa[-1].get("a") is None:
        qa[-1]["a"] = body.answer
    resp = await chat.send_message(UserMessage(text=body.answer))
    reply = resp if isinstance(resp, str) else getattr(resp, "content", str(resp))

    finished = "<report>" in reply
    report = None
    if finished:
        try:
            s = reply.split("<report>", 1)[1].split("</report>", 1)[0]
            s = s.strip().strip("`")
            if s.lower().startswith("json"):
                s = s[4:]
            report = json.loads(s)
        except Exception as e:
            log.warning("interview report parse: %s", e)
        doc["status"] = "completed"
        doc["report"] = report
    else:
        qa.append({"q": reply, "a": None})

    await db.interviews.update_one(
        {"interview_id": iid}, {"$set": {"qa": qa, "status": doc["status"], "report": doc.get("report")}}
    )
    return {"interview_id": iid, "next_question": None if finished else reply, "finished": finished, "report": report}


@api.get("/interview/history")
async def interview_history(user: dict = Depends(get_current_user)):
    items = await db.interviews.find({"user_id": user["user_id"]}, {"_id": 0}).sort("created_at", -1).to_list(20)
    return {"interviews": items}


# ---------- progress ----------
@api.get("/progress")
async def progress(user: dict = Depends(get_current_user)):
    road = await db.roadmaps.find_one({"user_id": user["user_id"]}, {"_id": 0}, sort=[("created_at", -1)])
    total_milestones = 0
    if road and road.get("data", {}).get("months"):
        for m in road["data"]["months"]:
            total_milestones += len(m.get("weekly_goals", []))
    done = len(road.get("completed_milestones", [])) if road else 0
    interviews_count = await db.interviews.count_documents({"user_id": user["user_id"]})
    resumes_count = await db.resumes.count_documents({"user_id": user["user_id"]})
    resume_doc = await db.resumes.find_one({"user_id": user["user_id"]}, {"_id": 0}, sort=[("created_at", -1)])
    ats = resume_doc.get("ats_score", 0) if resume_doc else 0
    return {
        "roadmap_total": total_milestones,
        "roadmap_done": done,
        "roadmap_percent": int(done / total_milestones * 100) if total_milestones else 0,
        "interviews_taken": interviews_count,
        "resumes_uploaded": resumes_count,
        "ats_score": ats,
        "skills_count": len(user.get("skills", [])),
    }


# ---------- health ----------
@api.get("/")
async def root():
    return {"service": "CareerPilot AI", "status": "ok"}


import base64
import numpy as np
from fastembed import TextEmbedding
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from fastapi import WebSocket, WebSocketDisconnect
import websockets as ws_client
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Embedding model for chat memory — embeddings persisted in MongoDB Atlas (no local vector store)
_embedder: Optional[TextEmbedding] = None
def get_embedder() -> TextEmbedding:
    global _embedder
    if _embedder is None:
        _embedder = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
        log.info("fastembed loaded")
    return _embedder


async def embed_text(text: str) -> List[float]:
    def _embed():
        vecs = list(get_embedder().embed([text]))
        return vecs[0].tolist() if vecs else []
    return await asyncio.to_thread(_embed)


def cosine(a: List[float], b: List[float]) -> float:
    if not a or not b: return 0.0
    av, bv = np.array(a, dtype=np.float32), np.array(b, dtype=np.float32)
    denom = float(np.linalg.norm(av) * np.linalg.norm(bv))
    return float(av @ bv / denom) if denom else 0.0


async def memory_search(user_id: str, query: str, k: int = 5) -> List[dict]:
    """Persistent semantic search over MongoDB Atlas chat_memory collection."""
    try:
        qv = await embed_text(query)
        docs = await db.chat_memory.find({"user_id": user_id}, {"_id": 0}).to_list(500)
        scored = [(cosine(qv, d.get("embedding") or []), d) for d in docs]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in scored[:k]]
    except Exception as e:
        log.warning("memory_search failed: %s", e)
        return []


async def memory_store(user_id: str, role: str, content: str) -> None:
    try:
        vec = await embed_text(content)
        await db.chat_memory.insert_one({
            "user_id": user_id, "role": role, "content": content,
            "embedding": vec, "ts": now_utc().isoformat(),
        })
    except Exception as e:
        log.warning("memory_store failed: %s", e)


# ElevenLabs client (sync — wrap with run_in_executor where needed)
el_client = ElevenLabs(api_key=ELEVENLABS_API_KEY) if ELEVENLABS_API_KEY else None

# Voice presets — pre-made ElevenLabs voices
VOICE_PRESETS = {
    "technical_male": {"voice_id": "JBFqnCBsd6RMkjVDRZzb", "label": "George — Technical Interviewer", "gender": "male"},
    "technical_female": {"voice_id": "EXAVITQu4vr4xnSDxMaL", "label": "Sarah — Senior Engineer", "gender": "female"},
    "hr_female": {"voice_id": "XrExE9yKIg1WjnnlVkGX", "label": "Matilda — HR Recruiter", "gender": "female"},
    "hr_male": {"voice_id": "TX3LPaxmHKxFdv7VOQHJ", "label": "Liam — Recruiter", "gender": "male"},
    "faang_strict": {"voice_id": "onwK4e9ZLuTAKqWW03F9", "label": "Daniel — FAANG Lead", "gender": "male"},
    "startup_friendly": {"voice_id": "pFZP5JQG7iQjIQuC4Bku", "label": "Lily — Startup Manager", "gender": "female"},
}

PERSONALITIES = {
    "friendly": "warm and encouraging; ask follow-ups gently",
    "strict_faang": "rigorous FAANG-style interviewer; probe deeply, ask about edge cases and complexity",
    "startup": "casual startup recruiter; mix of culture and technical questions",
    "hr": "professional HR manager; focus on behavioral and soft skills",
    "technical_architect": "senior technical architect; focus on system design, scalability, trade-offs",
}


# ---------- voice TTS ----------
@api.post("/voice/tts")
async def voice_tts(payload: Dict[str, str], _: dict = Depends(get_current_user)):
    text = payload.get("text", "").strip()
    voice_key = payload.get("voice", "technical_male")
    if not text:
        raise HTTPException(400, "text required")
    if not el_client:
        raise HTTPException(status_code=503, detail={
            "code": "tts_unavailable",
            "message": "ElevenLabs not configured. Frontend should fall back to browser TTS.",
        })
    voice_id = VOICE_PRESETS.get(voice_key, VOICE_PRESETS["technical_male"])["voice_id"]

    def _gen() -> bytes:
        stream = el_client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_turbo_v2_5",
            output_format="mp3_44100_128",
            voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.75, style=0.3, use_speaker_boost=True),
        )
        buf = b""
        for chunk in stream:
            if chunk:
                buf += chunk
        return buf

    audio_bytes = b""
    try:
        audio_bytes = await asyncio.to_thread(_gen)
    except Exception as e:
        log.warning("ElevenLabs TTS failed: %s", str(e)[:200])
        raise HTTPException(status_code=503, detail={
            "code": "tts_unavailable",
            "message": "ElevenLabs unavailable (free tier may be blocked from cloud IPs). Frontend should fall back to browser TTS.",
        })
    b64 = base64.b64encode(audio_bytes).decode()
    return {"audio_b64": b64, "mime": "audio/mpeg", "voice_id": voice_id}


# ---------- voice STT (Deepgram) ----------
@api.post("/voice/stt")
async def voice_stt(file: UploadFile = File(...), _: dict = Depends(get_current_user)):
    if not DEEPGRAM_API_KEY:
        raise HTTPException(500, "Deepgram not configured")
    buf = await file.read()
    mime = file.content_type or "audio/webm"
    params = {
        "model": "nova-3", "language": "en", "smart_format": "true",
        "punctuate": "true", "diarize": "false", "filler_words": "true",
    }
    async with httpx.AsyncClient(timeout=60) as hx:
        r = await hx.post(
            "https://api.deepgram.com/v1/listen",
            params=params,
            headers={"Authorization": f"Token {DEEPGRAM_API_KEY}", "Content-Type": mime},
            content=buf,
        )
    if r.status_code != 200:
        # fallback to nova-2 if nova-3 unavailable
        params["model"] = "nova-2"
        async with httpx.AsyncClient(timeout=60) as hx:
            r = await hx.post(
                "https://api.deepgram.com/v1/listen",
                params=params,
                headers={"Authorization": f"Token {DEEPGRAM_API_KEY}", "Content-Type": mime},
                content=buf,
            )
    if r.status_code != 200:
        log.warning("Deepgram error: %s %s", r.status_code, r.text[:200])
        raise HTTPException(502, "transcription failed")
    data = r.json()
    alt = (data.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}]) or [{}])[0]
    text = alt.get("transcript", "")
    words = alt.get("words", []) or []
    duration = float(data.get("metadata", {}).get("duration", 0) or 0)
    # rough confidence proxy: words per sec + average word confidence + filler ratio
    avg_conf = sum(float(w.get("confidence", 0.8)) for w in words) / max(1, len(words))
    wps = len(words) / max(0.1, duration)
    fillers = sum(1 for w in words if (w.get("word", "").lower() in {"um", "uh", "like", "you know", "actually", "basically"}))
    filler_ratio = fillers / max(1, len(words))
    # Compose confidence 0-100
    confidence = int(max(0, min(100, avg_conf * 100 - filler_ratio * 60 - max(0, wps - 3.2) * 5)))
    return {
        "transcript": text, "duration_s": duration, "words": len(words),
        "wps": round(wps, 2), "filler_words": fillers, "confidence": confidence,
    }


# ---------- Voice Interview Copilot ----------
class VoiceInterviewStart(BaseModel):
    role: str
    interview_type: str = "technical"  # technical|hr|recruiter|coding|behavioral|system_design
    difficulty: str = "intermediate"   # beginner|intermediate|advanced|faang
    personality: str = "friendly"
    voice: str = "technical_male"
    use_resume: bool = True


class VoiceInterviewAnswer(BaseModel):
    interview_id: str
    transcript: str
    confidence: Optional[int] = None
    duration_s: Optional[float] = None
    wps: Optional[float] = None
    filler_words: Optional[int] = None
    code: Optional[str] = None
    language: Optional[str] = None


async def _vi_chat(sid: str, system: str) -> LlmChat:
    return LlmChat(api_key=EMERGENT_LLM_KEY, session_id=sid, system_message=system).with_model(*GEMINI_MODEL)


def _vi_system(role: str, itype: str, difficulty: str, personality: str, resume_skills: list, resume_projects: list) -> str:
    style = PERSONALITIES.get(personality, PERSONALITIES["friendly"])
    resume_ctx = ""
    if resume_skills or resume_projects:
        resume_ctx = (
            f"\nThe candidate's resume includes skills: {', '.join(resume_skills[:25])}."
            f"\nProjects: {json.dumps(resume_projects[:5])}."
            "\nAsk at least TWO questions grounded in these projects/skills."
        )
    return (
        f"You are conducting a {difficulty.upper()} {itype} interview for the role of {role}. "
        f"Personality: {style}. Speak conversationally as if voice — short, natural sentences. "
        "Ask ONE concise question per turn. After candidate answers, briefly acknowledge (1 sentence), "
        "then ask the next question or a follow-up. "
        + resume_ctx +
        " After EXACTLY 6 candidate turns, output ONLY a JSON report wrapped in <report>...</report> with keys: "
        "technical_score(0-100), communication_score(0-100), confidence_score(0-100), problem_solving_score(0-100), "
        "clarity_score(0-100), overall(0-100), strengths(list), improvements(list), "
        "recommended_topics(list), suggested_projects(list), summary(string). "
        "Do not include any text outside the <report> tags when finishing."
    )


@api.get("/voice-interview/presets")
async def vi_presets(_: dict = Depends(get_current_user)):
    return {
        "voices": [{"key": k, **v} for k, v in VOICE_PRESETS.items()],
        "personalities": [{"key": k, "label": k.replace("_", " ").title(), "desc": v} for k, v in PERSONALITIES.items()],
        "types": ["technical", "hr", "recruiter", "coding", "behavioral", "system_design"],
        "difficulties": ["beginner", "intermediate", "advanced", "faang"],
    }


@api.post("/voice-interview/start")
async def vi_start(body: VoiceInterviewStart, user: dict = Depends(get_current_user)):
    resume_skills, resume_projects = [], []
    if body.use_resume:
        rdoc = await db.resumes.find_one({"user_id": user["user_id"]}, {"_id": 0}, sort=[("created_at", -1)])
        if rdoc and rdoc.get("parsed"):
            resume_skills = rdoc["parsed"].get("skills", []) or []
            resume_projects = rdoc["parsed"].get("projects", []) or []

    iid = f"vint_{uuid.uuid4().hex[:10]}"
    system = _vi_system(body.role, body.interview_type, body.difficulty, body.personality, resume_skills, resume_projects)

    chat = await _vi_chat(iid, system)
    resp = await chat.send_message(UserMessage(text=f"Begin the {body.interview_type} interview for {body.role}. Greet briefly (1 sentence) then ask your first question."))
    first_q = resp if isinstance(resp, str) else getattr(resp, "content", str(resp))

    doc = {
        "interview_id": iid, "user_id": user["user_id"],
        "role": body.role, "interview_type": body.interview_type, "difficulty": body.difficulty,
        "personality": body.personality, "voice": body.voice,
        "system_prompt": system,
        "turns": [{"q": first_q, "a": None, "metrics": None, "code": None}],
        "status": "active", "report": None,
        "created_at": now_utc().isoformat(),
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
    }
    await db.voice_interviews.insert_one(dict(doc))
    return jsonable(doc)

<<<<<<< HEAD
@api.get("/voice-interview")
async def voice_interview_list(user: dict = Depends(get_current_user)):
    interviews = await db.voice_interviews.find({"user_id": user["user_id"]}, {"_id": 0}).sort("created_at", -1).to_list(50)
    return {"interviews": interviews}

@api.get("/voice-interview/{interview_id}")
async def voice_interview_get(interview_id: str, user: dict = Depends(get_current_user)):
    interview = await db.voice_interviews.find_one({"interview_id": interview_id, "user_id": user["user_id"]}, {"_id": 0})
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview

@api.post("/voice-interview/answer")
async def voice_interview_answer(payload: VoiceInterviewAnswer, user: dict = Depends(get_current_user)):
    interview = await db.voice_interviews.find_one({"interview_id": payload.interview_id, "user_id": user["user_id"]})
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    turns = interview["turns"]
    # Update last turn
    turns[-1]["a"] = payload.transcript
    turns[-1]["confidence"] = payload.confidence
    turns[-1]["duration_s"] = payload.duration_s
    turns[-1]["wps"] = payload.wps
    turns[-1]["filler_words"] = payload.filler_words
    turns[-1]["code"] = payload.code
    turns[-1]["language"] = payload.language

    # Check if we're done (6 turns)
    if len(turns) >= 6:
        # Generate report
        sys_prompt = (
            "You are an interview evaluator. Evaluate this interview and return STRICT JSON: "
            "{"
            "overall: int 0-100, "
            "technical_score: int 0-100, "
            "communication_score: int 0-100, "
            "confidence_score: int 0-100, "
            "problem_solving_score: int 0-100, "
            "clarity_score: int 0-100, "
            "strengths: [string], "
            "improvements: [string], "
            "recommended_topics: [string], "
            "suggested_projects: [string], "
            "summary: string"
            "}"
        )
        report = await _gemini_json(sys_prompt, json.dumps(turns))
        await db.voice_interviews.update_one(
            {"interview_id": payload.interview_id},
            {"$set": {"status": "completed", "turns": turns, "report": report}}
        )
        return {"finished": True, "report": report}
    else:
        # Ask next question
        sys_prompt = (
            f"You are a {interview['personality']} {interview['interview_type']} interviewer for {interview['role']}. "
            f"Ask the next question. Return STRICT JSON with 'question': string"
        )
        res = await _gemini_json(sys_prompt, json.dumps(turns))
        question = res.get("question", "Thank you, that's all for today.")
        turns.append({"q": question})
        await db.voice_interviews.update_one(
            {"interview_id": payload.interview_id},
            {"$set": {"turns": turns}}
        )
        return {"finished": False, "next_question": question}

@api.post("/voice-interview/emotion")
async def voice_interview_emotion(payload: EmotionFrame, user: dict = Depends(get_current_user)):
    interview = await db.voice_interviews.find_one({"interview_id": payload.interview_id, "user_id": user["user_id"]})
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    emotion_entry = {
        "turn_index": payload.turn_index,
        "emotions": payload.emotions,
        "ts": now_utc().isoformat()
    }
    await db.voice_interviews.update_one(
        {"interview_id": payload.interview_id},
        {"$push": {"emotion_log": emotion_entry}}
    )
    return {"ok": True}

@api.get("/voice-interview/{interview_id}/pdf")
async def voice_interview_pdf(interview_id: str, user: dict = Depends(get_current_user)):
    interview = await db.voice_interviews.find_one({"interview_id": interview_id, "user_id": user["user_id"]})
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    if interview.get("status") != "completed":
        raise HTTPException(status_code=400, detail="Interview not yet completed")
    
    # Generate PDF
    buffer = io.BytesIO()
    doc_pdf = SimpleDocTemplate(buffer, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph(f"Interview Report: {interview['role']}", styles['Title']))
    story.append(Paragraph(f"Date: {interview['created_at']}", styles['Heading2']))
    report = interview.get("report", {})
    story.append(Paragraph(f"Overall Score: {report.get('overall', 0)}/100", styles['Heading3']))
    
    # Scores
    scores = [
        ("Technical Score", report.get('technical_score')),
        ("Communication Score", report.get('communication_score')),
        ("Confidence Score", report.get('confidence_score')),
        ("Problem Solving Score", report.get('problem_solving_score')),
        ("Clarity Score", report.get('clarity_score'))
    ]
    for name, score in scores:
        story.append(Paragraph(f"{name}: {score or 0}/100", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Summary
    story.append(Paragraph("Summary", styles['Heading3']))
    story.append(Paragraph(report.get('summary', ""), styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Strengths
    story.append(Paragraph("Strengths", styles['Heading3']))
    for s in report.get('strengths', []):
        story.append(Paragraph(f"- {s}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Improvements
    story.append(Paragraph("Areas for Improvement", styles['Heading3']))
    for i in report.get('improvements', []):
        story.append(Paragraph(f"- {i}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # QA
    story.append(PageBreak())
    story.append(Paragraph("Interview Questions & Answers", styles['Heading2']))
    for i, turn in enumerate(interview.get('turns', [])):
        story.append(Paragraph(f"Q{i+1}: {turn.get('q', '')}", styles['Heading3']))
        story.append(Paragraph(f"A{i+1}: {turn.get('a', '')}", styles['Normal']))
        story.append(Spacer(1, 12))
    
    doc_pdf.build(story)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=interview_report_{interview_id}.pdf"})

# ---------- voice/stt ----------
@api.post("/voice/stt")
async def voice_stt(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    if not DEEPGRAM_API_KEY:
        raise HTTPException(status_code=503, detail="Deepgram not configured")
    audio_bytes = await file.read()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.deepgram.com/v1/listen",
                headers={"Authorization": f"Token {DEEPGRAM_API_KEY}", "Content-Type": "audio/*"},
                data=audio_bytes,
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            transcript = data.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0].get("transcript", "")
            confidence = data.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0].get("confidence", 0)
            return {"transcript": transcript, "confidence": int(confidence * 100)}
    except Exception as e:
        log.error(f"Deepgram error: {e}")
        raise HTTPException(status_code=502, detail="STT failed")

# ---------- voice/stt-ws (WebSocket) ----------
@app.websocket("/api/voice/stt-ws")
async def voice_stt_ws(websocket: WebSocket):
    # Note: This is a placeholder. For real implementation, you'd proxy to Deepgram WS API
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            # Echo back for now
            await websocket.send_json({"type": "transcript", "text": "", "is_final": False})
    except WebSocketDisconnect:
        pass
    except Exception as e:
        log.error(f"STT WS error: {e}")

# ---------- code/evaluate ----------
class CodeEvaluateIn(BaseModel):
    code: str
    language: str
    problem: str

@api.post("/code/evaluate")
async def code_evaluate(payload: CodeEvaluateIn, user: dict = Depends(get_current_user)):
    sys_prompt = (
        "You are a senior software engineer. Evaluate this code. Return STRICT JSON: "
        "{"
        "correctness: int 0-100, "
        "overall: int 0-100, "
        "complexity: string, "
        "strengths: [string], "
        "improvements: [string]"
        "}"
    )
    res = await _gemini_json(sys_prompt, f"Problem: {payload.problem}\n\nCode:\n{payload.code}")
    return res

# ---------- resume/rewrite ----------
@api.post("/resume/rewrite")
async def resume_rewrite(user: dict = Depends(get_current_user)):
    # Step 1: Get all relevant data for resume
    resume_doc = await db.resumes.find_one({"user_id": user["user_id"]}, {"_id": 0}, sort=[("created_at", -1)])
    if not resume_doc:
        raise HTTPException(status_code=400, detail="No resume uploaded")
    
    portfolio_doc = await db.portfolios.find_one({"user_id": user["user_id"]}, {"_id": 0})
    
    # Prepare context for Gemini
    raw_text = resume_doc.get('raw_text', '')
    parsed = resume_doc.get('parsed', {})
    user_profile = {
        'name': user.get('name', 'Your Name'),
        'email': user.get('email', ''),
        'github_url': user.get('github_url', ''),
        'portfolio_url': user.get('portfolio_url', ''),
        'skills': user.get('skills', []),
        'career_goals': user.get('career_goals', ''),
        'education': user.get('education', ''),
        'degree': user.get('degree', ''),
        'graduation_year': user.get('graduation_year', ''),
    }
    
    # Step 2: Use Gemini to generate structured, ATS-optimized resume content
    sys_prompt = (
        "You are an expert professional resume writer and ATS optimization specialist. "
        "Generate a complete, ATS-optimized resume. "
        "Return your response ONLY as valid JSON with these keys (NO OTHER TEXT):\n"
        "  'contact': {'name': string, 'email': string, 'phone': string, 'linkedin': string, 'github': string, 'portfolio': string},\n"
        "  'professional_summary': string,\n"
        "  'skills': {'technical': [string], 'soft': [string], 'tools': [string]},\n"
        "  'projects': [{'name': string, 'description': string, 'technologies': [string]}],\n"
        "  'education': [{'degree': string, 'institution': string, 'year': string}],\n"
        "  'certifications': [string],\n"
        "  'experience': [{'role': string, 'company': string, 'duration': string, 'achievements': [string]}]"
    )
    
    context = f"User profile: {json.dumps(user_profile)}\n\nOriginal resume text: {raw_text}\n\nParsed data: {json.dumps(parsed)}"
    if portfolio_doc:
        context += f"\n\nPortfolio data: {json.dumps(portfolio_doc)}"
        
    # Try to get JSON, if failed use parsed data from uploaded resume
    try:
        ai_content = await _gemini_json(sys_prompt, context)
    except Exception as e:
        log.warning(f"Failed to get Gemini JSON, using fallback: {e}")
        ai_content = {}
    
    # Build fallback content from parsed resume data
    if not ai_content:
        ai_content = {
            'contact': {
                'name': user.get('name', 'Your Name'),
                'email': user.get('email', ''),
                'phone': '',
                'linkedin': '',
                'github': user.get('github_url', ''),
                'portfolio': user.get('portfolio_url', '')
            },
            'professional_summary': f"Experienced professional with skills in {', '.join(user.get('skills', []))}.",
            'skills': {
                'technical': parsed.get('skills', []) or user.get('skills', []),
                'soft': ['Teamwork', 'Communication'],
                'tools': []
            },
            'projects': parsed.get('projects', []) or [],
            'education': parsed.get('education', []) or [],
            'certifications': parsed.get('certifications', []) or [],
            'experience': parsed.get('experience', []) or []
        }
    
    # Ensure all keys exist
    ai_content.setdefault('contact', {})
    ai_content.setdefault('professional_summary', '')
    ai_content.setdefault('skills', {})
    ai_content.setdefault('projects', [])
    ai_content.setdefault('education', [])
    ai_content.setdefault('certifications', [])
    ai_content.setdefault('experience', [])
    
    # Step3: Generate professional DOCX
    buffer = io.BytesIO()
    doc = docx_lib.Document()
    
    # Set margins for ATS compliance
    sections = doc.sections
    for section in sections:
        section.top_margin = docx_lib.shared.Inches(0.75)
        section.bottom_margin = docx_lib.shared.Inches(0.75)
        section.left_margin = docx_lib.shared.Inches(0.75)
        section.right_margin = docx_lib.shared.Inches(0.75)
        
    # Normalize fonts
    def set_font(paragraph, name='Calibri', size=11, bold=False):
        for run in paragraph.runs:
            run.font.name = name
            run.font.size = docx_lib.shared.Pt(size)
            run.font.bold = bold
            # For compatibility with Word on macOS
            run._element.rPr.rFonts.set(docx_lib.oxml.ns.qn('w:eastAsia'), name)
            
    # Contact Information Section
    contact = ai_content.get('contact', {})
    contact_name = contact.get('name', user.get('name', 'Your Name'))
    header_para = doc.add_paragraph()
    header_run = header_para.add_run(contact_name)
    header_run.font.name = 'Calibri'
    header_run.font.size = docx_lib.shared.Pt(16)
    header_run.font.bold = True
    header_para.alignment = docx_lib.enum.text.WD_ALIGN_PARAGRAPH.CENTER
    header_run._element.rPr.rFonts.set(docx_lib.oxml.ns.qn('w:eastAsia'), 'Calibri')
    
    contact_line = []
    if contact.get('email'): contact_line.append(contact['email'])
    if contact.get('phone'): contact_line.append(contact['phone'])
    if contact.get('linkedin'): contact_line.append(contact['linkedin'])
    if contact.get('github'): contact_line.append(contact['github'])
    if contact.get('portfolio'): contact_line.append(contact['portfolio'])
    
    if contact_line:
        contact_para = doc.add_paragraph()
        contact_para.add_run(' | '.join(contact_line))
        contact_para.alignment = docx_lib.enum.text.WD_ALIGN_PARAGRAPH.CENTER
        set_font(contact_para, size=11)
        
    doc.add_paragraph()  # Add spacing
    
    # Professional Summary
    if ai_content.get('professional_summary'):
        summary_heading = doc.add_paragraph()
        summary_heading.add_run('PROFESSIONAL SUMMARY').bold = True
        set_font(summary_heading, size=12)
        summary_para = doc.add_paragraph(ai_content['professional_summary'])
        set_font(summary_para, size=11)
        summary_para.paragraph_format.line_spacing = 1.15
        doc.add_paragraph()
        
    # Skills Section
    skills = ai_content.get('skills', {})
    if skills:
        skills_heading = doc.add_paragraph()
        skills_heading.add_run('SKILLS').bold = True
        set_font(skills_heading, size=12)
        
        skill_items = []
        if skills.get('technical'):
            skill_items.append(f"Technical: {', '.join(skills['technical'])}")
        if skills.get('tools'):
            skill_items.append(f"Tools: {', '.join(skills['tools'])}")
        if skills.get('soft'):
            skill_items.append(f"Soft: {', '.join(skills['soft'])}")
            
        skills_para = doc.add_paragraph()
        skills_para.add_run('; '.join(skill_items))
        set_font(skills_para, size=11)
        doc.add_paragraph()
        
    # Experience Section
    experience = ai_content.get('experience', [])
    if experience:
        exp_heading = doc.add_paragraph()
        exp_heading.add_run('PROFESSIONAL EXPERIENCE').bold = True
        set_font(exp_heading, size=12)
        
        for exp in experience:
            role = exp.get('role', '')
            company = exp.get('company', '')
            duration = exp.get('duration', '')
            
            role_para = doc.add_paragraph()
            role_run = role_para.add_run(f"{role}")
            role_run.bold = True
            set_font(role_para, size=11)
            role_para.paragraph_format.space_after = docx_lib.shared.Pt(0)
            
            company_para = doc.add_paragraph()
            company_para.add_run(f"{company} | {duration}").italic = True
            set_font(company_para, size=11)
            company_para.paragraph_format.space_after = docx_lib.shared.Pt(0)
            
            for ach in exp.get('achievements', []):
                ach_para = doc.add_paragraph(ach, style='List Bullet')
                set_font(ach_para, size=11)
                ach_para.paragraph_format.space_after = docx_lib.shared.Pt(0)
                
            doc.add_paragraph()
            
    # Projects Section
    projects = ai_content.get('projects', [])
    if projects:
        proj_heading = doc.add_paragraph()
        proj_heading.add_run('PROJECTS').bold = True
        set_font(proj_heading, size=12)
        
        for proj in projects:
            name = proj.get('name', '')
            techs = ', '.join(proj.get('technologies', []))
            desc = proj.get('description', '')
            
            proj_name_para = doc.add_paragraph()
            proj_name_para.add_run(name).bold = True
            if techs:
                proj_name_para.add_run(f" — {techs}").italic = True
            set_font(proj_name_para, size=11)
            proj_name_para.paragraph_format.space_after = docx_lib.shared.Pt(0)
            
            desc_para = doc.add_paragraph(desc)
            set_font(desc_para, size=11)
            doc.add_paragraph()
            
    # Education Section
    education = ai_content.get('education', [])
    if education:
        edu_heading = doc.add_paragraph()
        edu_heading.add_run('EDUCATION').bold = True
        set_font(edu_heading, size=12)
        
        for edu in education:
            degree = edu.get('degree', '')
            institution = edu.get('institution', '')
            year = edu.get('year', '')
            
            edu_para = doc.add_paragraph()
            edu_para.add_run(f"{degree}").bold = True
            set_font(edu_para, size=11)
            edu_para.paragraph_format.space_after = docx_lib.shared.Pt(0)
            
            inst_para = doc.add_paragraph(f"{institution} | {year}")
            set_font(inst_para, size=11)
            doc.add_paragraph()
            
    # Certifications Section
    certifications = ai_content.get('certifications', [])
    if certifications:
        cert_heading = doc.add_paragraph()
        cert_heading.add_run('CERTIFICATIONS').bold = True
        set_font(cert_heading, size=12)
        
        for cert in certifications:
            cert_para = doc.add_paragraph(cert, style='List Bullet')
            set_font(cert_para, size=11)
        doc.add_paragraph()
        
    # Save document
    doc.save(buffer)
    buffer.seek(0)
    
    # Return file for download
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=ATS_Optimized_Resume.docx"}
    )

# ---------- career-twin ----------
@api.post("/career-twin/brief")
async def career_twin_brief(user: dict = Depends(get_current_user)):
    week_of = now_utc().strftime("%Y-%m-%d")
    sys_prompt = (
        "You are an AI career twin. Generate a weekly brief. Return STRICT JSON: "
        "{"
        "greeting: string, "
        "this_week_focus: string, "
        "market_signals: [string], "
        "recommended_action: string, "
        "opportunities: [{title: string, why_now: string}]"
        "}"
    )
    profile = json.dumps(user)
    brief = await _gemini_json(sys_prompt, profile)
    doc = {
        "user_id": user["user_id"],
        "week_of": week_of,
        "brief": brief,
        "created_at": now_utc().isoformat()
    }
    await db.career_twin.insert_one(dict(doc))
    return jsonable(doc)

@api.get("/career-twin")
async def career_twin_get(user: dict = Depends(get_current_user)):
    latest = await db.career_twin.find_one({"user_id": user["user_id"]}, {"_id": 0}, sort=[("created_at", -1)])
    return latest or {}

# ---------- public-profile ----------
@api.get("/public-profile/me")
async def public_profile_me(user: dict = Depends(get_current_user)):
    profile = await db.public_profiles.find_one({"user_id": user["user_id"]}, {"_id": 0})
    return profile or {}

@api.post("/public-profile/publish")
async def public_profile_publish(payload: PublishIn, user: dict = Depends(get_current_user)):
    # Check if slug exists
    existing = await db.public_profiles.find_one({"slug": payload.slug})
    if existing and existing["user_id"] != user["user_id"]:
        raise HTTPException(status_code=400, detail="Slug already taken")
    # Get user data
    career_rec = await db.career_recommendations.find_one({"user_id": user["user_id"]}, {"_id": 0}, sort=[("created_at", -1)])
    portfolio = await db.portfolios.find_one({"user_id": user["user_id"]}, {"_id": 0})
    doc = {
        "user_id": user["user_id"],
        "slug": payload.slug,
        "name": user.get("name", ""),
        "picture": user.get("picture", ""),
        "headline": payload.headline or "",
        "bio": payload.bio or "",
        "skills": user.get("skills", []),
        "show_resume": payload.show_resume,
        "show_portfolio": payload.show_portfolio,
        "top_careers": career_rec.get("careers", [])[:5] if career_rec else [],
        "portfolio": portfolio if portfolio and payload.show_portfolio else None,
        "created_at": now_utc().isoformat(),
        "updated_at": now_utc().isoformat()
    }
    await db.public_profiles.update_one({"user_id": user["user_id"]}, {"$set": doc}, upsert=True)
    return jsonable(doc)

# ---------- public profile (unauthenticated) ----------
@api.get("/public/{slug}")
async def public_profile(slug: str):
    profile = await db.public_profiles.find_one({"slug": slug}, {"_id": 0, "user_id": 0})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

# ---------- startup / shutdown / cors ----------
=======

@api.post("/voice-interview/answer")
async def vi_answer(body: VoiceInterviewAnswer, user: dict = Depends(get_current_user)):
    doc = await db.voice_interviews.find_one({"interview_id": body.interview_id, "user_id": user["user_id"]}, {"_id": 0})
    if not doc:
        raise HTTPException(404, "interview not found")

    chat = await _vi_chat(body.interview_id, doc["system_prompt"])
    turns = doc["turns"]
    # replay prior answers to rebuild context (Gemini LlmChat persists by session_id but reload safety)
    for t in turns:
        if t.get("a"):
            await chat.send_message(UserMessage(text=t["a"]))

    metrics = {
        "confidence": body.confidence, "duration_s": body.duration_s,
        "wps": body.wps, "filler_words": body.filler_words,
    }
    answer_payload = body.transcript
    if body.code:
        answer_payload += f"\n\nMy code ({body.language or 'python'}):\n```\n{body.code}\n```"

    if turns and turns[-1].get("a") is None:
        turns[-1]["a"] = body.transcript
        turns[-1]["metrics"] = metrics
        if body.code:
            turns[-1]["code"] = {"language": body.language, "code": body.code}

    resp = await chat.send_message(UserMessage(text=answer_payload))
    reply = resp if isinstance(resp, str) else getattr(resp, "content", str(resp))

    finished = "<report>" in reply
    report = None
    if finished:
        try:
            s = reply.split("<report>", 1)[1].split("</report>", 1)[0]
            s = s.strip().strip("`")
            if s.lower().startswith("json"):
                s = s[4:]
            a, b = s.find("{"), s.rfind("}")
            if a >= 0 and b > a:
                s = s[a:b + 1]
            report = json.loads(s)
        except Exception as e:
            log.warning("vi report parse: %s", e)
        doc["status"] = "completed"
        doc["report"] = report
    else:
        turns.append({"q": reply, "a": None, "metrics": None, "code": None})

    await db.voice_interviews.update_one(
        {"interview_id": body.interview_id},
        {"$set": {"turns": turns, "status": doc["status"], "report": doc.get("report")}},
    )
    return {
        "interview_id": body.interview_id,
        "finished": finished,
        "next_question": None if finished else reply,
        "report": report,
    }


@api.get("/voice-interview/{interview_id}")
async def vi_get(interview_id: str, user: dict = Depends(get_current_user)):
    doc = await db.voice_interviews.find_one(
        {"interview_id": interview_id, "user_id": user["user_id"]}, {"_id": 0}
    )
    if not doc:
        raise HTTPException(404, "not found")
    return doc


@api.get("/voice-interview")
async def vi_list(user: dict = Depends(get_current_user)):
    items = await db.voice_interviews.find(
        {"user_id": user["user_id"]}, {"_id": 0}
    ).sort("created_at", -1).to_list(30)
    return {"interviews": items}


# ---------- Code evaluation ----------
@api.post("/code/evaluate")
async def code_evaluate(payload: Dict[str, str], _: dict = Depends(get_current_user)):
    code = payload.get("code", "")
    language = payload.get("language", "python")
    problem = payload.get("problem", "")
    if not code:
        raise HTTPException(400, "code required")
    sys_p = (
        "You are a senior coding interviewer. Evaluate the candidate's code. "
        "Return STRICT JSON: {correctness(0-100), time_complexity, space_complexity, "
        "code_quality(0-100), bugs(list), improvements(list), better_solution(string), overall(0-100)}"
    )
    result = await _gemini_json(sys_p, json.dumps({"language": language, "problem": problem, "code": code[:6000]}))
    return result


# ---------- Resume Rewriter ----------
@api.post("/resume/rewrite")
async def resume_rewrite(user: dict = Depends(get_current_user)):
    rdoc = await db.resumes.find_one({"user_id": user["user_id"]}, {"_id": 0}, sort=[("created_at", -1)])
    if not rdoc:
        raise HTTPException(400, "Upload a resume first")
    sys_p = (
        "You are an expert ATS resume writer. Rewrite the candidate's resume to maximise ATS score and impact. "
        "Use STRONG action verbs, quantify achievements, integrate the missing_keywords naturally, "
        "and keep it truthful (do not invent facts). Return STRICT JSON: "
        "{name, headline, summary, contact:{location, email}, "
        "experience:[{role, company, duration, bullets:[string]}], "
        "projects:[{name, bullets:[string]}], "
        "education:[{degree, institution, year}], "
        "skills:[string], certifications:[string]}"
    )
    payload = {
        "user_profile": {"name": user.get("name"), "email": user.get("email"), "career_goals": user.get("career_goals")},
        "original_text": rdoc.get("raw_text", "")[:9000],
        "parsed": rdoc.get("parsed", {}),
        "missing_keywords": (rdoc.get("parsed") or {}).get("missing_keywords", []),
    }
    rewritten = await _gemini_json(sys_p, json.dumps(payload))

    # Build DOCX
    from docx import Document
    from docx.shared import Pt, RGBColor
    doc = Document()
    styles = doc.styles
    # Title
    name = rewritten.get("name") or user.get("name") or "Candidate"
    h = doc.add_paragraph()
    run = h.add_run(name)
    run.bold = True
    run.font.size = Pt(20)
    if rewritten.get("headline"):
        p = doc.add_paragraph(rewritten["headline"])
        p.runs[0].italic = True
    contact = rewritten.get("contact") or {}
    contact_line = " · ".join(filter(None, [contact.get("location"), contact.get("email") or user.get("email")]))
    if contact_line:
        doc.add_paragraph(contact_line)

    def section(title):
        p = doc.add_paragraph()
        r = p.add_run(title.upper())
        r.bold = True
        r.font.size = Pt(12)

    if rewritten.get("summary"):
        section("Summary")
        doc.add_paragraph(rewritten["summary"])

    if rewritten.get("skills"):
        section("Skills")
        doc.add_paragraph(" • ".join(rewritten["skills"]))

    for sec_key, sec_label in [("experience", "Experience"), ("projects", "Projects")]:
        items = rewritten.get(sec_key) or []
        if not items:
            continue
        section(sec_label)
        for it in items:
            head = doc.add_paragraph()
            r1 = head.add_run(it.get("role") or it.get("name") or "")
            r1.bold = True
            sub = []
            if it.get("company"): sub.append(it["company"])
            if it.get("duration"): sub.append(it["duration"])
            if sub: head.add_run(" — " + " · ".join(sub))
            for b in (it.get("bullets") or []):
                doc.add_paragraph(b, style="List Bullet")

    if rewritten.get("education"):
        section("Education")
        for e in rewritten["education"]:
            doc.add_paragraph(f"{e.get('degree','')} — {e.get('institution','')} ({e.get('year','')})")

    if rewritten.get("certifications"):
        section("Certifications")
        for c in rewritten["certifications"]:
            doc.add_paragraph(c, style="List Bullet")

    out = io.BytesIO()
    doc.save(out)
    out.seek(0)
    fname = f"{name.replace(' ', '_')}_ATS_Resume.docx"
    return StreamingResponse(
        out,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{fname}"'},
    )


# ---------- AI Career Twin ----------
@api.post("/career-twin/brief")
async def career_twin_brief(user: dict = Depends(get_current_user)):
    progress = await db.users.find_one({"user_id": user["user_id"]}, {"_id": 0})
    road = await db.roadmaps.find_one({"user_id": user["user_id"]}, {"_id": 0}, sort=[("created_at", -1)])
    careers = await db.career_recommendations.find({"user_id": user["user_id"]}, {"_id": 0}).to_list(10)
    trends_doc = await db.trends_cache.find_one({"_id": "latest"}, {"_id": 0})
    sys_p = (
        "You are the user's AI Career Twin — a persistent agent that tracks their growth and the market. "
        "Generate this week's brief. Be specific, opinionated, and actionable. "
        "Return STRICT JSON: {greeting, this_week_focus, market_signals:[string], opportunities:[{title, why_now}], "
        "skills_to_practice:[string], recommended_action:string, motivation_quote}"
    )
    inp = {
        "user": {"name": progress.get("name"), "skills": progress.get("skills"), "goals": progress.get("career_goals")},
        "roadmap": road.get("data") if road else None,
        "completed_milestones": (road or {}).get("completed_milestones", []),
        "career_matches": [{"name": c.get("name"), "match": c.get("match_score")} for c in careers],
        "week_of": now_utc().isoformat()[:10],
    }
    brief = await _gemini_json(sys_p, json.dumps(inp))
    doc = {
        "user_id": user["user_id"],
        "week_of": inp["week_of"],
        "brief": brief,
        "created_at": now_utc().isoformat(),
    }
    await db.career_twin.update_one(
        {"user_id": user["user_id"], "week_of": doc["week_of"]},
        {"$set": doc}, upsert=True,
    )
    return doc


@api.get("/career-twin")
async def career_twin_latest(user: dict = Depends(get_current_user)):
    doc = await db.career_twin.find_one(
        {"user_id": user["user_id"]}, {"_id": 0}, sort=[("created_at", -1)]
    )
    return doc or {}


# ---------- Public Profile ----------
class PublishIn(BaseModel):
    slug: str
    bio: Optional[str] = None
    headline: Optional[str] = None
    show_resume: bool = False
    show_portfolio: bool = True


@api.post("/public-profile/publish")
async def publish_profile(body: PublishIn, user: dict = Depends(get_current_user)):
    slug = body.slug.lower().strip().replace(" ", "-")
    if not slug.replace("-", "").isalnum():
        raise HTTPException(400, "slug must be alphanumeric or hyphenated")
    existing = await db.public_profiles.find_one({"slug": slug, "user_id": {"$ne": user["user_id"]}})
    if existing:
        raise HTTPException(409, "slug taken")
    doc = {
        "slug": slug, "user_id": user["user_id"],
        "headline": body.headline, "bio": body.bio,
        "show_resume": body.show_resume, "show_portfolio": body.show_portfolio,
        "updated_at": now_utc().isoformat(),
    }
    await db.public_profiles.update_one({"user_id": user["user_id"]}, {"$set": doc}, upsert=True)
    return doc


@api.get("/public-profile/me")
async def get_my_public_profile(user: dict = Depends(get_current_user)):
    doc = await db.public_profiles.find_one({"user_id": user["user_id"]}, {"_id": 0})
    return doc or {}


@api.get("/public/{slug}")
async def get_public_profile(slug: str):
    p = await db.public_profiles.find_one({"slug": slug.lower()}, {"_id": 0})
    if not p:
        raise HTTPException(404, "Profile not found")
    user = await db.users.find_one({"user_id": p["user_id"]}, {"_id": 0})
    if not user:
        raise HTTPException(404, "User not found")
    out = {
        "slug": p["slug"],
        "headline": p.get("headline"),
        "bio": p.get("bio"),
        "name": user.get("name"),
        "picture": user.get("picture"),
        "skills": user.get("skills", []),
        "education": user.get("education"),
        "degree": user.get("degree"),
        "career_goals": user.get("career_goals"),
        "github_url": user.get("github_url"),
        "portfolio_url": user.get("portfolio_url"),
    }
    if p.get("show_portfolio"):
        port = await db.portfolios.find_one({"user_id": p["user_id"]}, {"_id": 0})
        if port:
            out["portfolio"] = {
                "score": (port.get("analysis") or {}).get("score"),
                "repos": (port.get("repos") or [])[:6],
            }
    careers = await db.career_recommendations.find({"user_id": p["user_id"]}, {"_id": 0}).limit(3).to_list(3)
    out["top_careers"] = [{"name": c.get("name"), "match": c.get("match_score")} for c in careers]
    return out


# ---------- Webcam Emotion summary ----------
class EmotionFrame(BaseModel):
    interview_id: str
    turn_index: int
    emotions: Dict[str, float]  # {happy: 0.4, neutral: 0.5, sad: 0.05, ...}


@api.post("/voice-interview/emotion")
async def vi_emotion(body: EmotionFrame, user: dict = Depends(get_current_user)):
    """Browser sends batched face-api.js emotion summaries. We compute aggregates per turn."""
    await db.voice_interviews.update_one(
        {"interview_id": body.interview_id, "user_id": user["user_id"]},
        {"$push": {"emotion_log": {
            "turn_index": body.turn_index,
            "emotions": body.emotions,
            "ts": now_utc().isoformat(),
        }}},
    )
    return {"ok": True}


# ---------- PDF export for voice interview report ----------
@api.get("/voice-interview/{interview_id}/pdf")
async def vi_pdf(interview_id: str, user: dict = Depends(get_current_user)):
    doc = await db.voice_interviews.find_one(
        {"interview_id": interview_id, "user_id": user["user_id"]}, {"_id": 0}
    )
    if not doc:
        raise HTTPException(404, "interview not found")
    if not doc.get("report"):
        raise HTTPException(400, "interview not yet complete")

    report = doc["report"]
    buf = io.BytesIO()
    pdf = SimpleDocTemplate(buf, pagesize=LETTER, leftMargin=0.7*inch, rightMargin=0.7*inch,
                            topMargin=0.7*inch, bottomMargin=0.7*inch)
    styles = getSampleStyleSheet()
    h_title = ParagraphStyle("HTitle", parent=styles["Title"], fontName="Helvetica-Bold",
                             fontSize=26, leading=30, alignment=TA_LEFT, textColor=colors.black)
    h_section = ParagraphStyle("HSection", parent=styles["Heading2"], fontName="Helvetica-Bold",
                               fontSize=11, leading=14, alignment=TA_LEFT,
                               textColor=colors.HexColor("#71717a"), spaceBefore=18, spaceAfter=8)
    body_st = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10.5, leading=15)
    mono_st = ParagraphStyle("Mono", parent=styles["Normal"], fontName="Courier",
                             fontSize=9, textColor=colors.HexColor("#71717a"))

    story = []
    story.append(Paragraph("CareerPilot AI · Interview Report", body_st))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"{doc.get('role','—')}", h_title))
    story.append(Paragraph(
        f"{doc.get('interview_type','').upper()} · {doc.get('difficulty','').upper()} · "
        f"{(doc.get('personality') or '').replace('_',' ').upper()} · "
        f"{doc.get('created_at','')[:10]}", mono_st,
    ))
    story.append(Spacer(1, 10))

    # Overall
    story.append(Paragraph(f"OVERALL SCORE: <b>{report.get('overall','—')}/100</b>", body_st))

    # Score table
    story.append(Paragraph("SCORE BREAKDOWN", h_section))
    rows = [["Metric", "Score"]]
    for k, label in [("technical_score","Technical"),("communication_score","Communication"),
                     ("confidence_score","Confidence"),("problem_solving_score","Problem-solving"),
                     ("clarity_score","Clarity")]:
        v = report.get(k)
        rows.append([label, f"{v}/100" if v is not None else "—"])
    t = Table(rows, hAlign="LEFT", colWidths=[3*inch, 1.2*inch])
    t.setStyle(TableStyle([
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),10),
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1e1e1e")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("BACKGROUND",(0,1),(-1,-1),colors.HexColor("#f4f4f5")),
        ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#27272a")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#fafafa"), colors.white]),
        ("LEFTPADDING",(0,0),(-1,-1),10),
        ("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
    ]))
    story.append(t)

    for key, label in [("strengths","STRENGTHS"),("improvements","IMPROVEMENTS"),
                       ("recommended_topics","RECOMMENDED TOPICS"),("suggested_projects","SUGGESTED PROJECTS")]:
        items = report.get(key) or []
        if items:
            story.append(Paragraph(label, h_section))
            for it in items:
                story.append(Paragraph(f"• {it}", body_st))

    if report.get("summary"):
        story.append(Paragraph("SUMMARY", h_section))
        story.append(Paragraph(report["summary"], body_st))

    # Q&A
    story.append(PageBreak())
    story.append(Paragraph("FULL TRANSCRIPT", h_section))
    for i, t_ in enumerate(doc.get("turns", []), 1):
        story.append(Paragraph(f"<b>Q{i}.</b> {t_.get('q','')}", body_st))
        if t_.get("a"):
            story.append(Paragraph(f"<i>You:</i> {t_['a']}", body_st))
        story.append(Spacer(1, 8))

    pdf.build(story)
    buf.seek(0)
    fname = f"CareerPilot_Interview_{interview_id}.pdf"
    return StreamingResponse(
        buf, media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{fname}"'},
    )


# ---------- Deepgram WebSocket relay (real-time partial transcripts) ----------
@app.websocket("/api/voice/stt-ws")
async def stt_websocket(websocket: WebSocket, token: str = ""):
    """Relay browser audio chunks to Deepgram's WS API and forward transcripts back."""
    await websocket.accept()
    # auth
    sess = await db.user_sessions.find_one({"session_token": token}) if token else None
    if not sess:
        await websocket.send_json({"type": "error", "message": "auth required"})
        await websocket.close(code=4401)
        return
    if not DEEPGRAM_API_KEY:
        await websocket.send_json({"type": "error", "message": "deepgram not configured"})
        await websocket.close()
        return

    dg_url = (
        "wss://api.deepgram.com/v1/listen?"
        "model=nova-3&language=en&punctuate=true&smart_format=true&interim_results=true&"
        "encoding=opus"
    )
    headers = [("Authorization", f"Token {DEEPGRAM_API_KEY}")]
    try:
        async with ws_client.connect(dg_url, additional_headers=headers, max_size=None) as dg:
            async def from_browser():
                try:
                    while True:
                        msg = await websocket.receive()
                        if msg.get("type") == "websocket.disconnect":
                            break
                        if msg.get("bytes") is not None:
                            await dg.send(msg["bytes"])
                        elif msg.get("text") is not None:
                            if msg["text"] == "stop":
                                await dg.send(json.dumps({"type": "CloseStream"}))
                                break
                except WebSocketDisconnect:
                    pass

            async def from_deepgram():
                try:
                    async for raw in dg:
                        try:
                            data = json.loads(raw) if isinstance(raw, (str, bytes)) else {}
                        except Exception:
                            continue
                        alt = (data.get("channel", {}).get("alternatives", [{}]) or [{}])[0]
                        text = alt.get("transcript", "")
                        if text:
                            await websocket.send_json({
                                "type": "transcript",
                                "text": text,
                                "is_final": bool(data.get("is_final")),
                                "speech_final": bool(data.get("speech_final")),
                            })
                except Exception as e:
                    log.warning("dg recv error: %s", e)

            await asyncio.gather(from_browser(), from_deepgram())
    except Exception as e:
        log.warning("stt-ws error: %s", e)
        try: await websocket.send_json({"type": "error", "message": str(e)[:200]})
        except Exception: pass
    finally:
        try: await websocket.close()
        except Exception: pass


>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
app.include_router(api)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    # Indexes for performance — all data lives in MongoDB Atlas
    try:
        await db.users.create_index("user_id", unique=True)
        await db.users.create_index("email", unique=True)
        await db.user_sessions.create_index("session_token", unique=True)
        await db.user_sessions.create_index("user_id")
        await db.resumes.create_index([("user_id", 1), ("created_at", -1)])
        await db.career_recommendations.create_index("user_id")
        await db.skill_gaps.create_index([("user_id", 1), ("target_role", 1)])
        await db.roadmaps.create_index([("user_id", 1), ("created_at", -1)])
        await db.voice_interviews.create_index([("user_id", 1), ("created_at", -1)])
        await db.interviews.create_index([("user_id", 1), ("created_at", -1)])
        await db.chat_messages.create_index([("user_id", 1), ("ts", 1)])
        await db.chat_memory.create_index("user_id")
        await db.portfolios.create_index("user_id", unique=True)
        await db.career_twin.create_index([("user_id", 1), ("week_of", -1)])
        await db.public_profiles.create_index("slug", unique=True)
        log.info("Mongo indexes ensured")
    except Exception as e:
        log.warning("index init: %s", e)


@app.on_event("shutdown")
async def shutdown():
    client.close()
<<<<<<< HEAD

=======
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
