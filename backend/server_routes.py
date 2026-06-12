"""Additional routes for CareerPilot AI server."""
import os
import io
import json
import uuid
import base64
import logging
import asyncio
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

import httpx
import numpy as np
from fastapi import Depends, HTTPException, UploadFile, File, Cookie, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse

# Import from main server module
from server import (
    api, db, get_current_user, now_utc, jsonable, log,
    _gemini_json, gemini_generate_text, gemini_stream_text,
    GEMINI_MODEL, embed_text, memory_search, memory_store,
    el_client, VOICE_PRESETS, PERSONALITIES,
    VoiceInterviewStart, VoiceInterviewAnswer, EmotionFrame,
    PublishIn, InterviewStartIn, InterviewAnswerIn, SalaryPredictIn,
    YT_KEY, ADZUNA_APP_ID, ADZUNA_APP_KEY, RAPIDAPI_KEY,
    GITHUB_TOKEN, ELEVENLABS_API_KEY, DEEPGRAM_API_KEY
)

from elevenlabs import VoiceSettings
import websockets as ws_client

from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER


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


# ---------- chatbot ----------
@api.post("/chat/stream")
async def chat_stream(body, user: dict = Depends(get_current_user)):
    from server import ChatIn
    body = ChatIn(**body) if isinstance(body, dict) else body
    sid = body.session_id or f"chat_{user['user_id']}"
    profile_ctx = {"name": user.get("name"), "skills": user.get("skills", []), "career_goals": user.get("career_goals"), "education": user.get("education")}

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
