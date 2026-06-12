"""CareerPilot AI - FastAPI backend."""
import os
import io
import json
import uuid
import base64
import logging
import asyncio
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any

import httpx
import fitz
import docx as docx_lib
import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request, Response, UploadFile, File, Cookie, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

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
YT_KEY = os.environ.get("YOUTUBE_API_KEY")
ADZUNA_APP_ID = os.environ.get("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.environ.get("ADZUNA_APP_KEY")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
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


# ---------- helpers ----------
def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def jsonable(doc: dict) -> dict:
    doc.pop("_id", None)
    return doc


async def get_current_user(request: Request, session_token: Optional[str] = Cookie(default=None)) -> dict:
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


# ---------- Pydantic Models ----------
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
    interview_type: str = "technical"


class InterviewAnswerIn(BaseModel):
    interview_id: str
    answer: str


class SalaryPredictIn(BaseModel):
    role: str
    experience_years: int = 0
    location: str = "India"
    skills: List[str] = []


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

    is_prod = os.environ.get("ENV") == "production"
    response.set_cookie(
        key="session_token",
        value=session_token,
        max_age=7 * 24 * 3600,
        httponly=True,
        secure=is_prod,
        samesite="lax" if not is_prod else "none",
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
    if RAPIDAPI_KEY:
        try:
            async with httpx.AsyncClient(timeout=20) as hx:
                r = await hx.get(
                    "https://jsearch.p.rapidapi.com/search",
                    headers={"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": "jsearch.p.rapidapi.com"},
                    params={"query": f"{q} in {location}", "page": "1", "num_pages": "1"},
                )
            if r.status_code == 200:
                for j in (r.json().get("data") or [])[:12]:
                    items.append({
                        "id": j.get("job_id"),
                        "title": j.get("job_title"),
                        "company": j.get("employer_name"),
                        "location": ", ".join(filter(None, [j.get("job_city"), j.get("job_country")])),
                        "salary": f"{j.get('job_min_salary')}-{j.get('job_max_salary')} {j.get('job_salary_currency') or ''}" if j.get("job_min_salary") else "Not disclosed",
                        "url": j.get("job_apply_link"),
                        "description": (j.get("job_description") or "")[:280],
                        "remote": j.get("job_is_remote", False),
                        "posted": j.get("job_posted_at_datetime_utc"),
                    })
        except Exception as e:
            log.warning("JSearch failed: %s", e)

    user_skills = {s.lower() for s in user.get("skills", [])}
    for it in items:
        text = (it.get("title", "") + " " + it.get("description", "")).lower()
        hits = sum(1 for s in user_skills if s and s in text)
        it["match_score"] = min(100, 40 + hits * 12) if user_skills else 60

    items.sort(key=lambda x: x["match_score"], reverse=True)
    return {"query": q, "location": location, "results": items}


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
        repos_r = await hx.get(f"https://api.github.com/users/{username}/repos", headers=headers, params={"sort": "updated", "per_page": 20})
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
        "user": {"login": gh_user.get("login"), "name": gh_user.get("name"), "bio": gh_user.get("bio"), "followers": gh_user.get("followers"), "public_repos": gh_user.get("public_repos")},
        "repos": repo_summary,
    }
    ai = await _gemini_json(sys_prompt, json.dumps(profile_text))

    out = {
        "username": username, "avatar": gh_user.get("avatar_url"), "name": gh_user.get("name") or username,
        "bio": gh_user.get("bio"), "public_repos": gh_user.get("public_repos", 0), "followers": gh_user.get("followers", 0),
        "repos": repo_summary, "analysis": ai, "created_at": now_utc().isoformat(),
    }
    await db.portfolios.update_one({"user_id": user["user_id"]}, {"$set": {"user_id": user["user_id"], **out}}, upsert=True)
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

# ---------- startup / shutdown / cors ----------
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

