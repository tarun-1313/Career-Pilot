# 🚀 CareerPilot AI — Intelligent Career Operating System

<div align="center">

### AI-Powered Career Intelligence Platform for Students, Freshers & Professionals

Build your career with AI-driven guidance, intelligent roadmaps, mock interviews, ATS optimization, and real-time job intelligence.

</div>

---

# 🌟 Overview

CareerPilot AI is a next-generation AI-powered career operating system designed to help users navigate their professional journey using advanced Artificial Intelligence and multi-agent systems.

Unlike traditional career platforms, CareerPilot AI acts as a personalized AI career mentor that continuously analyzes:

* Skills
* Resume quality
* Career goals
* Market demand
* Industry trends
* Interview readiness
* GitHub portfolio strength

The platform provides intelligent recommendations, dynamic learning roadmaps, AI-powered mock interviews, ATS resume optimization, and live job intelligence in one unified ecosystem.

---

# ✨ Core Features

## 🧠 AI Career Intelligence

* AI-powered career recommendations
* Career path prediction
* Industry alignment analysis
* Salary estimation
* Future growth forecasting

---

## 📄 ATS Resume Analyzer

* Resume upload (PDF/DOCX)
* ATS compatibility scoring
* Resume parsing & skill extraction
* AI-powered resume rewriting
* ATS keyword optimization
* Professional DOCX resume generation

---

## 🎯 Skill Gap Analysis

* Missing skill detection
* Industry comparison engine
* Technology demand analysis
* Learning priority suggestions
* AI-generated recommendations

---

## 🛣️ Personalized Learning Roadmaps

* Dynamic AI-generated roadmaps
* Month-by-month progression plans
* Recommended certifications
* AI-curated project suggestions
* Skill milestone tracking

---

## 🎤 AI Mock Interview Platform

* Technical interviews
* HR interviews
* Recruiter simulations
* Voice-based interviews
* Coding interview environment
* AI feedback generation
* Real-time transcript system
* Communication analysis

Powered by:

* Gemini AI
* ElevenLabs
* Deepgram

---

## 💼 AI Job Intelligence

* Live job recommendations
* AI-powered match scoring
* Hiring trend analysis
* Salary insights
* Remote job discovery
* Internship recommendations

Integrated APIs:

* JSearch API
* Adzuna API

---

## 🧑‍💻 GitHub Portfolio Analyzer

* Repository analysis
* Contribution tracking
* README evaluation
* AI portfolio scoring
* Deployment detection
* Skill intelligence extraction

---

## 🤖 Multi-Agent AI System

CareerPilot AI uses a centralized AI orchestration system powered by LangGraph.

### AI Agents:

* Career Intelligence Agent
* Skill Gap Agent
* Roadmap Agent
* Interview Agent
* Resume Agent
* Job Intelligence Agent
* Trend Intelligence Agent
* AI Mentor Agent

The platform behaves like a real AI career operating system instead of isolated tools.

---

# 🏗️ System Architecture

```bash
USER
   │
   ▼
Frontend (React + TailwindCSS)
   │
   ▼
FastAPI Backend
   │
   ▼
AI Orchestrator (LangGraph)
   │
 ┌─┼────────────────────────────────────┐
 │ │ │ │ │ │ │
 ▼ ▼ ▼ ▼ ▼ ▼ ▼

Career Agent
Skill Gap Agent
Roadmap Agent
Interview Agent
Resume Agent
Job Agent
Trend Agent

   │
   ▼
MongoDB Atlas + AI Memory Layer
```

---

# ⚡ Tech Stack

## Frontend

* React.js
* Tailwind CSS
* Framer Motion
* Monaco Editor
* Face-api.js
* Sonner
* Phosphor Icons

---

## Backend

* FastAPI
* Python 3.11
* Motor (Async MongoDB Driver)
* LangGraph
* LangChain
* Gemini 2.5 Flash

---

## Database

* MongoDB Atlas

---

## AI & APIs

* Gemini API
* ElevenLabs API
* Deepgram API
* GitHub API
* JSearch API
* Adzuna API
* YouTube Data API

---

# 📂 Project Structure

```bash
Career-Pilot/
│
├── backend/
│   ├── server.py
│   ├── requirements.txt
│   ├── agents/
│   ├── services/
│   ├── models/
│   ├── routes/
│   ├── utils/
│   ├── interview/
│   └── database/
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── context/
│   │   ├── hooks/
│   │   ├── lib/
│   │   └── App.js
│   │
│   ├── public/
│   ├── package.json
│   └── .env
│
├── screenshots/
├── docs/
├── README.md
└── .gitignore
```

---

# 📦 Prerequisites

Make sure the following tools are installed:

* Python 3.11+
* Node.js 18+
* Git
* MongoDB Atlas Account

Optional:

* MongoDB Local Installation

---

# 🚀 Installation Guide

# 1️⃣ Clone Repository

```bash
git clone https://github.com/tarun-1313/Career-Pilot.git
```

```bash
cd Career-Pilot
```

---

# 2️⃣ Backend Setup

Navigate to backend folder:

```bash
cd backend
```

Create virtual environment:

## Windows

```bash
python -m venv venv
```

Activate virtual environment:

```bash
venv\Scripts\activate
```

## Mac/Linux

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 3️⃣ Frontend Setup

Open a new terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

---

# ⚙️ Environment Variables

# Backend `.env`

Create `.env` inside backend folder:

```env
# MongoDB Atlas
MONGODB_URL=your_mongodb_atlas_url
DB_NAME=careerpilot

# Gemini AI
GEMINI_API_KEY=your_gemini_api_key

# JSearch API
RAPIDAPI_KEY=your_rapidapi_key

# Adzuna
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key

# Deepgram
DEEPGRAM_API_KEY=your_deepgram_api_key

# ElevenLabs
ELEVENLABS_API_KEY=your_elevenlabs_api_key

# YouTube API
YOUTUBE_API_KEY=your_youtube_api_key

# GitHub
GITHUB_TOKEN=your_github_token

# Emergent Auth
EMERGENT_LLM_KEY=your_emergent_key
```

---

# Frontend `.env`

Create `.env` inside frontend folder:

```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

---

# 🌐 MongoDB Atlas Setup

1. Create MongoDB Atlas account
2. Create a cluster
3. Create database user
4. Whitelist IP address
5. Copy MongoDB URI

Example:

```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/careerpilot
```

---

# ▶️ Running The Application

# Start Backend

Open terminal inside backend folder:

```bash
cd backend
```

Activate virtual environment:

## Windows

```bash
venv\Scripts\activate
```

## Mac/Linux

```bash
source venv/bin/activate
```

Run backend server:

```bash
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

Backend runs on:

```bash
http://localhost:8000
```

Swagger Docs:

```bash
http://localhost:8000/docs
```

---

# Start Frontend

Open another terminal:

```bash
cd frontend
```

Run React app:

```bash
npm start
```

Frontend runs on:

```bash
http://localhost:3000
```

---

# 🎤 AI Interview Flow

```bash
User Speaks
↓
Deepgram Speech-to-Text
↓
Gemini AI Evaluation
↓
AI Feedback Generation
↓
ElevenLabs Voice Response
↓
Real-Time Analytics Display
```

---

# 📊 Main Modules

| Module                 | Description                     |
| ---------------------- | ------------------------------- |
| Dashboard              | Career overview & analytics     |
| Resume Analyzer        | ATS optimization system         |
| Career Recommendations | AI career prediction            |
| Skill Gap Analysis     | Missing skills detection        |
| Roadmap Generator      | Personalized learning plans     |
| Job Intelligence       | Live job matching               |
| Mock Interviews        | AI interview simulation         |
| GitHub Analyzer        | Portfolio intelligence          |
| AI Mentor              | Conversational career assistant |

---

# 🔐 Security Features

* JWT Authentication
* Google OAuth
* Secure API routes
* Password hashing
* MongoDB Atlas cloud storage
* Environment variable protection

---

# 🧠 AI Interview Platform

Professional AI interview environment inspired by:

* Google interview systems
* OpenAI Voice Mode
* Enterprise recruiting platforms

Features:

* AI interviewer avatars
* Voice interaction
* Real-time transcripts
* Coding interviews
* Emotion analysis
* AI-generated reports

---

# 🚀 Deployment

## Frontend Deployment

Deploy on:

* Vercel

Build frontend:

```bash
npm run build
```

---

## Backend Deployment

Deploy backend on:

* Railway
* Render

---

## Database

Use:

* MongoDB Atlas

---

# 📸 Screenshots

Create `/screenshots` folder and add:

* Dashboard UI
* Resume Analyzer
* AI Interview Platform
* Skill Gap Dashboard
* Roadmap Generator
* Job Intelligence Page

---

# 🧪 Future Improvements

* AI Career Twin
* LinkedIn Integration
* AI Networking Agent
* Real-Time AI Recruiter
* Multi-user Interview Rooms
* AI Collaboration Engine
* Hiring Probability Prediction
* AI Startup Advisor

---

# 🎯 Use Cases

CareerPilot AI is designed for:

* Students
* Freshers
* Developers
* AI Engineers
* Career Switchers
* Hackathon Projects
* Startup MVPs

---

# 🤝 Contributing

Contributions are welcome.

Feel free to:

* Fork the repository
* Create pull requests
* Report issues
* Suggest improvements

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

## Tarun

Aspiring AI/ML Engineer passionate about:

* Generative AI
* AI Agents
* LangGraph
* LLM Applications
* Intelligent Systems

GitHub:
https://github.com/tarun-1313

---

# ⭐ Support

If you like this project:

* Star the repository
* Fork the project
* Share feedback
* Contribute improvements

---

# 🚀 Final Vision

CareerPilot AI is not just a career recommendation website.

It is an AI-powered Career Operating System that continuously learns, adapts, and guides users through every stage of their professional journey using advanced AI, intelligent agents, and real-time market intelligence.
