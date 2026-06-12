import React from "react";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import { Toaster } from "sonner";
import { AuthProvider } from "@/context/AuthContext";
import ProtectedRoute from "@/components/ProtectedRoute";
import DashboardLayout from "@/components/DashboardLayout";

import Landing from "@/pages/Landing";
import Login from "@/pages/Login";
import AuthCallback from "@/pages/AuthCallback";
import Dashboard from "@/pages/Dashboard";
import Profile from "@/pages/Profile";
import Resume from "@/pages/Resume";
import Careers from "@/pages/Careers";
import SkillGap from "@/pages/SkillGap";
import Roadmap from "@/pages/Roadmap";
import Courses from "@/pages/Courses";
import Jobs from "@/pages/Jobs";
import Interview from "@/pages/Interview";
import VoiceInterview from "@/pages/VoiceInterview";
import CareerTwin from "@/pages/CareerTwin";
import ShareProfile from "@/pages/ShareProfile";
import PublicProfile from "@/pages/PublicProfile";
import Chatbot from "@/pages/Chatbot";
import Portfolio from "@/pages/Portfolio";
import Trends from "@/pages/Trends";

function AppRouter() {
  const location = useLocation();
  // CRITICAL: detect OAuth callback synchronously, before ProtectedRoute checks
  if (location.hash?.includes("session_id=")) {
    return <AuthCallback />;
  }

  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/auth/callback" element={<AuthCallback />} />
      <Route path="/u/:slug" element={<PublicProfile />} />

      <Route element={<ProtectedRoute><DashboardLayout /></ProtectedRoute>}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/onboarding" element={<Profile onboarding />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/resume" element={<Resume />} />
        <Route path="/careers" element={<Careers />} />
        <Route path="/skills" element={<SkillGap />} />
        <Route path="/roadmap" element={<Roadmap />} />
        <Route path="/courses" element={<Courses />} />
        <Route path="/jobs" element={<Jobs />} />
        <Route path="/interview" element={<Interview />} />
        <Route path="/voice-interview" element={<VoiceInterview />} />
        <Route path="/twin" element={<CareerTwin />} />
        <Route path="/share" element={<ShareProfile />} />
        <Route path="/chat" element={<Chatbot />} />
        <Route path="/portfolio" element={<Portfolio />} />
        <Route path="/trends" element={<Trends />} />
      </Route>
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRouter />
        <Toaster theme="dark" position="top-right" toastOptions={{ style: { background: "#141414", border: "1px solid #27272a", color: "#fff", borderRadius: 0 } }} />
      </AuthProvider>
    </BrowserRouter>
  );
}
