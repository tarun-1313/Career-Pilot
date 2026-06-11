# CareerPilot AI — Product Requirements Doc

## Original problem statement
Build "CareerPilot AI" — a modern, production-ready AI-powered web platform acting as a complete AI Career Operating System for students, graduates, and professionals. Provides career recommendations, skill-gap analysis, personalized learning roadmaps, course/job matching, resume ATS analysis, portfolio evaluation, AI mock interviews, salary prediction, industry trend tracking, progress monitoring, and an AI chatbot.

## Stack actually used
- Frontend: React 19 (CRA) + Tailwind + shadcn primitives + Framer Motion + Phosphor Icons + Recharts + Sonner toasts
- Backend: FastAPI + Motor (MongoDB)
- AI: Gemini 2.5 Flash via Emergent Universal Key (`emergentintegrations`)
- Auth: Emergent-managed Google OAuth (cookie + Bearer)
- External: YouTube Data API, JSearch (RapidAPI), Adzuna, GitHub REST API

## User personas
- Final-year CSE/engineering students choosing a career path
- Graduates targeting first AI/ML/SWE job
- Working professionals planning a career switch

## Core requirements (static)
1. Google OAuth (one-click) with 7-day session cookie
2. User profile + onboarding (education, skills, interests, goals)
3. Resume upload (PDF/DOCX) → ATS score + extraction + rewrites
4. AI career recommendations (top 5 with match %, salary, demand)
5. Skill-gap analysis vs target role
6. Personalized monthly learning roadmap with togglable milestones
7. YouTube course/resource recommendations
8. Live job matching (JSearch + Adzuna) with match scoring
9. GitHub portfolio analyzer (repos + AI critique)
10. Industry trends dashboard + salary predictor
11. AI mock interview (technical/HR/behavioural/system-design) with final report
12. Streaming AI career mentor chatbot
13. Progress dashboard

## What's been implemented (2026-02-11)
- Full landing page (Archetype 4 dark theme, Cabinet Grotesk + Satoshi)
- Login + Google OAuth callback (Emergent)
- Dashboard with stats + career matches + roadmap snapshot
- Profile + onboarding flow
- Resume upload/ATS endpoint + UI
- Career recommendations + Skill gap + Roadmap with milestone tracking
- Courses (YouTube), Jobs (JSearch+Adzuna fallback)
- Portfolio analyzer (GitHub + AI)
- Trends dashboard with charts + salary predictor
- AI Mentor streaming chat (SSE)
- AI Mock Interview with multi-turn flow + scored report
- Loading skeletons on AI-heavy pages
- 18/18 backend pytest passing; all frontend routes load

## Prioritized backlog
- P1: AI Career Twin agent (persistent LangGraph supervisor)
- P1: Resume rewriter (download .docx with applied improvements)
- P2: Voice + webcam in mock interviews
- P2: Vector DB (Qdrant) semantic memory for chatbot
- P2: Public profile / shareable career page
- P3: Stripe paid tier (resume rewriter + unlimited mocks)
