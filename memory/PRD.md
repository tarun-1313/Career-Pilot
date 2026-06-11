# CareerPilot AI — Product Requirements Doc

## Original problem statement
Build "CareerPilot AI" — a modern, production-ready AI-powered web platform acting as a complete AI Career Operating System. v2 adds an advanced AI Mock Interview Copilot (ElevenLabs + Deepgram + Gemini), AI Career Twin, Resume Rewriter (.docx), and a public shareable career page.

## Stack
- Frontend: React 19 (CRA) + Tailwind + Framer Motion + Phosphor Icons + Recharts + Monaco + Sonner
- Backend: FastAPI + Motor (MongoDB)
- AI: Gemini 2.5 Flash via Emergent Universal Key
- Voice: ElevenLabs TTS (REST), browser SpeechSynthesis fallback when blocked
- STT: Deepgram nova-3
- Auth: Emergent-managed Google OAuth
- External: YouTube Data, JSearch (RapidAPI), Adzuna, GitHub REST

## Implemented (v1 + v2 — 2026-02-11)

### v1 Core (32/32 backend tests passing)
1. Google OAuth + 7-day cookie/Bearer session
2. Profile + onboarding (skills, interests, goals)
3. Resume ATS analyzer (PDF/DOCX, Gemini)
4. Career recommendations (top 5 with match %, salary, demand)
5. Skill-gap diff
6. Personalized monthly roadmap with togglable milestones
7. YouTube course feed
8. Live jobs (JSearch + Adzuna) with match scoring
9. GitHub portfolio analyzer + AI critique
10. Industry trends + salary predictor + charts
11. Streaming AI mentor chatbot (SSE)
12. Text-based AI mock interview

### v2 Advanced (this iteration)
1. **AI Career Twin** — persistent weekly brief (greeting, focus, market signals, opportunities, action)
2. **Resume Rewriter** — Gemini-powered ATS-optimized .docx download
3. **Voice Interview Copilot** — full live experience:
   - 6 voice presets (Technical M/F, HR M/F, FAANG Strict, Startup Friendly)
   - 5 interviewer personalities, 4 difficulty levels, 6 interview types
   - ElevenLabs TTS w/ browser SpeechSynthesis fallback (cloud-IP blocked free tier handled)
   - Deepgram nova-3 STT with confidence + filler-word detection
   - MediaRecorder live audio capture
   - Monaco code editor for coding rounds (Py/JS/Java/C++/Go)
   - Animated avatar waveform, live transcript, confidence meter
   - 6-turn structured interview ending in scored report (5 axes + strengths/improvements/topics/projects)
4. **Public shareable career page** at `/u/:slug` — auto-builds from profile + GitHub + AI career matches
5. **Code evaluation** endpoint (Gemini-graded correctness, complexity, quality)

## Prioritized backlog
- P2: Qdrant vector memory for chatbot (semantic recall)
- P2: Webcam emotion analysis in voice interviews
- P2: AI interview history dashboard with radar + heatmap
- P3: WebSocket streaming Deepgram (true real-time partial transcripts)
- P3: PDF export of voice interview report
- P3: Stripe paid tier (Career Twin daily briefs + unlimited interviews)

## Backend test status
- Iteration 1: 18/18 passing
- Iteration 2: 32/32 passing (1 expected skip for empty seed)
