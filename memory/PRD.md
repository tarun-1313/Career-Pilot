# CareerPilot AI — Product Requirements Doc

## Original problem statement
Build "CareerPilot AI" — a modern, production-ready AI-powered web platform acting as a complete AI Career Operating System for students, graduates, and professionals. v3 adds Qdrant semantic memory, webcam emotion + WebSocket Deepgram streaming, PDF interview report export, MongoDB Atlas, and a redesigned futuristic landing page. **App is now free for all users.**

## Stack
- Frontend: React 19 + Tailwind + Framer Motion + Phosphor + Recharts + Monaco + face-api.js (CDN) + Sonner
- Backend: FastAPI + Motor (MongoDB Atlas) + Qdrant in-memory (fastembed BAAI/bge-small-en) + reportlab + websockets
- AI: Gemini 2.5 Flash via Emergent Universal Key
- Voice: ElevenLabs TTS REST (with browser SpeechSynthesis fallback)
- STT: Deepgram nova-3 (REST + WebSocket relay)
- Auth: Emergent-managed Google OAuth
- External: YouTube, JSearch (RapidAPI), Adzuna, GitHub

## Implemented (v1 + v2 + v3 — current 2026-02-11)

### v1 Core
1. Google OAuth, profile/onboarding, resume ATS analyzer, career recs, skill gap, roadmap, courses, jobs, portfolio, trends, salary, mentor chat, text mock interview.

### v2 Advanced
2. AI Career Twin (weekly brief), Resume Rewriter (.docx), Voice Interview Copilot (ElevenLabs + Deepgram + Gemini), Code evaluator, Public shareable career page (/u/:slug).

### v3 Premium
3. **Qdrant semantic memory** — mentor chat now recalls past exchanges across sessions (BAAI/bge-small-en embeddings, fastembed)
4. **Webcam emotion analysis** — face-api.js client-side, emotion frames persisted per interview turn
5. **WebSocket Deepgram relay** — `/api/voice/stt-ws` for real-time partial transcripts
6. **PDF interview report** — reportlab-generated, professional layout with scores + Q&A transcript
7. **MongoDB Atlas** — switched from local to cluster0.jssl3hr.mongodb.net
8. **Futuristic landing page** — Perplexity/Linear/Vercel-inspired: pill nav, glass dashboard mockup, floating glass cards, animated waveform, gradient mesh background, animated counters

### Tests
- Iter 1: 18/18 backend pass
- Iter 2: 32/32 backend pass
- Iter 3: 40/40 backend pass (1 expected skip)
- 100% frontend testid coverage

## Prioritized backlog (no monetization — free for all)
- Refactor: split server.py (~1500 lines) into FastAPI routers (voice_interview, public, chat, ws)
- Migrate Qdrant `query()`/`add()` → `query_points()`/`upsert()` (deprecation 1.17)
- Persist Qdrant to disk volume (currently in-memory, wiped on restart)
- WS Deepgram streaming UI in voice interview (currently REST-based; WS endpoint live but UI uses REST round-trip)
- Webcam emotion analytics dashboard (radar of dominant emotion vs turn)
- Optional: vector search across user's resume/projects for richer interview questions
