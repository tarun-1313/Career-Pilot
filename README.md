
# 🚀Margdarshak Sathi AI — Intelligent Career Operating System

<div align="center">

### AI-Powered Career Intelligence Platform for Students, Freshers & Professionals

Build your career with AI-driven guidance, intelligent roadmaps, mock interviews, ATS optimization, and real-time job intelligence.

</div>

---

# 🌟 Overview

Margdarshak AI is a next-generation AI-powered career operating system designed to help users navigate their professional journey using advanced Artificial Intelligence and multi-agent systems.

Unlike traditional career platforms, Margdarshak Sathi AI acts as a personalized AI career mentor that continuously analyzes:

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

Margdarshak Sathi AI uses a centralized AI orchestration system powered by LangGraph.

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
MargdarshakSathi/
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
git clone https://github.com/tarun-1313/Margdarshak-Sathi.git
```

```bash
cd Margdarshak-Sathi
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
=======
# MargdarshakSathi AI

🚀 Your personal AI-powered career coach! Everything you need to land your dream job in one place.

## 📋 Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Running the App](#running-the-app)
7. [Usage Guide](#usage-guide)
8. [Project Structure](#project-structure)
9. [Troubleshooting](#troubleshooting)

---

## ✨ Features <a name="features"></a>

### 🔐 Authentication & Profiles
- **Google OAuth Login**: Secure, one-click sign-in with Google
- **User Profiles**: Manage your personal info, skills, education, and more
- **Public Profiles**: Share your career profile with a public URL

### 📝 Resume Tools
- **Resume Upload & Parsing**: Upload your PDF/DOCX, we extract and analyze it
- **ATS Scoring**: Instant score + feedback on how ATS-friendly your resume is
- **AI Resume Rewrite**: Generate a professionally formatted, ATS-optimized resume in DOCX

### 🎯 Career Guidance
- **AI Career Recommendations**: Personalized career paths based on your skills
- **Skill Gap Analysis**: Shows exactly which skills you're missing for your target role
- **Learning Roadmaps**: 6-month step-by-step plans to reach your goals
- **Trending Careers**: Real-time data on in-demand roles and salaries

### 💼 Job Search
- **Job Search (JSearch + Adzuna)**: Multiple job board APIs for maximum results
- **AI-Powered Match Scoring**: See how well each job matches your skills
- **Save & Apply**: Easy access to job descriptions and application links

### 🎤 Interview Prep
- **AI Interview Simulator**: Practice interviews with 6 different AI personas
- **Voice Interviews**: Record your answers via microphone (Speech-to-Text via Deepgram)
- **Text & Code Answers**: Type responses or solve coding problems live
- **Webcam Emotion Analysis**: Get feedback on your confidence and demeanor (via face-api.js)
- **Interview Reports**: Detailed feedback on technical skills, communication, and more (PDF export)

### 🤖 Additional Features
- **Portfolio Analysis**: Analyze your GitHub repos
- **AI Chatbot**: Ask your career coach anything
- **Courses Search**: Find free/paid courses to learn missing skills
- **Career Twin**: Compare your profile to successful professionals in your field

---

## 🛠️ Tech Stack <a name="tech-stack"></a>

### Frontend
- React (Create React App)
- Tailwind CSS
- Phosphor Icons
- Sonner (toasts)
- Framer Motion (animations)
- Monaco Editor (code editor)
- Face-api.js (emotion detection)

### Backend
- Python 3.11
- FastAPI
- Motor (async MongoDB driver)
- Google Gemini 2.5 Flash (AI)
- Deepgram (Speech-to-Text)
- JSearch API (jobs)
- Adzuna API (jobs fallback)
- YouTube Data API (courses)
- python-docx (resume generation)
- ReportLab (PDF reports)

### Database
- MongoDB Atlas (cloud) or MongoDB local

---

## 📦 Prerequisites <a name="prerequisites"></a>

Make sure you have these installed:

- [Python 3.11](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [Git](https://git-scm.com/)
- [MongoDB (optional, for local dev)](https://www.mongodb.com/try/download/community)

You'll also need API keys for these services (all are free tier available):
- Google Cloud (Gemini API)
- RapidAPI (JSearch)
- Adzuna
- YouTube Data API
- Deepgram
- GitHub (optional, for portfolio analysis)
- ElevenLabs (optional, for TTS)

---

## 🚀 Installation <a name="installation"></a>

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Margdarshak-Sathi
```

### 2. Backend Setup

```bash
cd backend
# Create virtual environment
python -m venv venv
# Activate virtual environment (Windows)
venv\Scripts\activate
# Activate virtual environment (Mac/Linux)
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd ../frontend
>>>>>>> f53c755 (Updated landing page and AI dashboard)
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
=======
## ⚙️ Configuration <a name="configuration"></a>

### Backend Configuration

Create a `.env` file in the `backend` directory (use `backend/.env.example` if available, or use the template below):

```env
# MongoDB
MONGO_URL=mongodb://localhost:27017/careerpilot
DB_NAME=careerpilot
# Or use MongoDB Atlas
MONGODB_URL=mongodb+srv://<username>:<password>@cluster0.jssl3hr.mongodb.net/?appName=Cluster0

# AI & APIs
GEMINI_API_KEY=your_gemini_api_key_here
RAPIDAPI_KEY=your_rapidapi_key_here
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
YOUTUBE_API_KEY=your_youtube_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key
GITHUB_TOKEN=your_github_token (optional)
ELEVENLABS_API_KEY=your_elevenlabs_key (optional)

# Emergent (for auth, pre-configured)
EMERGENT_LLM_KEY=sk-emergent-18bF83582C1652196F
```

### Frontend Configuration

Create a `.env` file in the `frontend` directory:
>>>>>>> f53c755 (Updated landing page and AI dashboard)

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
=======
## ▶️ Running the App <a name="running-the-app"></a>

### 1. Start the Backend (in backend directory)

First make sure your virtual environment is activated:

```bash
cd backend
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Mac/Linux
```

Then run the server:
>>>>>>> f53c755 (Updated landing page and AI dashboard)

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
=======
The backend will be running at http://localhost:8000

You can check the API docs at http://localhost:8000/docs

### 2. Start the Frontend (in frontend directory, in a new terminal)

```bash
cd frontend
npm start
```

The app will open at http://localhost:3000

---

## 📖 Usage Guide <a name="usage-guide"></a>

### First Time Setup

1. Go to http://localhost:3000
2. Click "Login with Google" to create your account
3. Complete your profile at http://localhost:3000/profile
4. Upload your resume at http://localhost:3000/resume
5. Explore all the features!

### Quick Feature Walkthrough

- **Dashboard**: Get an overview of your stats
- **Resume Page**: Upload, analyze, and generate an ATS-optimized resume
- **Careers Page**: Get career recommendations
- **Skill Gap Page**: See what skills you're missing
- **Roadmap Page**: Generate your learning roadmap
- **Jobs Page**: Search and filter jobs with AI matching
- **Interview/Voice Interview**: Practice interviews with AI
- **Chatbot**: Ask your career coach anything
- **Portfolio Page**: Connect your GitHub

---

## 📂 Project Structure <a name="project-structure"></a>

```
Margdarshak-Sathi-main/
├── backend/
│   ├── server.py              # Main FastAPI server
│   ├── gemini_client.py       # Gemini AI client
│   ├── requirements.txt       # Python dependencies
│   ├── tests/                 # Backend tests
│   └── .env                   # Backend config
├── frontend/
│   ├── src/
│   │   ├── pages/             # All page components
│   │   ├── components/        # Reusable components
│   │   ├── lib/               # API client, utils
│   │   ├── context/           # React context
│   │   └── App.js             # Main app
│   ├── public/
│   ├── package.json
│   └── .env                   # Frontend config
└── README.md
>>>>>>> f53c755 (Updated landing page and AI dashboard)
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
=======
## 🔍 Troubleshooting <a name="troubleshooting"></a>

### Common Issues

1. **Backend won't start**:
   - Check if all required dependencies are installed
   - Verify your `.env` file exists and keys are correct
   - Make sure no other process is using port 8000

2. **Frontend can't connect to backend**:
   - Check if `REACT_APP_BACKEND_URL` is set correctly in `frontend/.env`
   - Make sure the backend server is running
   - Check for CORS errors in the browser dev tools

3. **Resume generation not working**:
   - Check if `python-docx` is installed
   - Make sure your Gemini API key is valid

4. **Job search not working**:
   - Try both JSearch and Adzuna (the app will automatically fall back)
   - Verify your API keys in `backend/.env`

5. **Voice interview not recording**:
   - Make sure you allow microphone permissions in your browser
   - Check browser console for errors
   - If STT isn't working, you can still type your answer

### Getting Help

If you're stuck:
1. Check the backend terminal logs for errors
2. Check the browser dev tools (F12) for frontend errors
3. Verify all API keys are correct

---

## 📄 License

MIT License - feel free to use this for your own projects!

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or PRs.

---

## 📧 Support

If you have questions or feedback, feel free to reach out!

---

🎉 **Thanks for using CareerPilot AI! We hope it helps you land your dream job!**
