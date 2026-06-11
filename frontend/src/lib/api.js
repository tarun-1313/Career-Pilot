import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

export const api = axios.create({
  baseURL: API,
  withCredentials: true,
});

// Auth
export const exchangeSession = (session_id) =>
  api.post("/auth/google/session", { session_id }).then((r) => r.data);
export const fetchMe = () => api.get("/auth/me").then((r) => r.data);
export const logout = () => api.post("/auth/logout").then((r) => r.data);

// Profile
export const updateProfile = (data) => api.put("/profile", data).then((r) => r.data);

// Resume
export const uploadResume = (file) => {
  const fd = new FormData();
  fd.append("file", file);
  return api.post("/resume/upload", fd, { headers: { "Content-Type": "multipart/form-data" } }).then((r) => r.data);
};
export const getLatestResume = () => api.get("/resume/latest").then((r) => r.data);

// Careers
export const recommendCareers = () => api.post("/careers/recommend").then((r) => r.data);
export const listCareers = () => api.get("/careers").then((r) => r.data);

// Skill gap
export const skillGap = (role) => api.post("/skills/gap", { role }).then((r) => r.data);

// Roadmap
export const generateRoadmap = (role, months = 6) =>
  api.post("/roadmap/generate", { role, months: String(months) }).then((r) => r.data);
export const getRoadmap = () => api.get("/roadmap").then((r) => r.data);
export const toggleMilestone = (key) =>
  api.post("/roadmap/milestone/toggle", { key }).then((r) => r.data);

// Courses
export const searchCourses = (q) =>
  api.get("/courses/search", { params: { q } }).then((r) => r.data);

// Jobs
export const searchJobs = (q, location) =>
  api.get("/jobs/search", { params: { q, location } }).then((r) => r.data);

// Portfolio
export const analyzePortfolio = (github_url) =>
  api.post("/portfolio/analyze", { github_url }).then((r) => r.data);

// Salary
export const predictSalary = (data) => api.post("/salary/predict", data).then((r) => r.data);

// Trends
export const getTrends = () => api.get("/trends").then((r) => r.data);

// Chat (streaming)
export const chatStream = async (message, onDelta, onDone, sessionId = null) => {
  const res = await fetch(`${API}/chat/stream`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id: sessionId }),
  });
  if (!res.ok) {
    onDone && onDone(new Error("chat failed"));
    return;
  }
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buf = "";
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    const lines = buf.split("\n\n");
    buf = lines.pop();
    for (const line of lines) {
      if (!line.startsWith("data:")) continue;
      const data = line.slice(5).trim();
      if (data === "[DONE]") { onDone && onDone(); return; }
      try {
        const obj = JSON.parse(data);
        if (obj.delta) onDelta(obj.delta);
      } catch {}
    }
  }
  onDone && onDone();
};
export const getChatHistory = () => api.get("/chat/history").then((r) => r.data);

// Interview
export const startInterview = (role, interview_type) =>
  api.post("/interview/start", { role, interview_type }).then((r) => r.data);
export const answerInterview = (interview_id, answer) =>
  api.post("/interview/answer", { interview_id, answer }).then((r) => r.data);
export const interviewHistory = () => api.get("/interview/history").then((r) => r.data);

// Resume rewriter (download)
export const downloadRewrittenResume = async () => {
  const res = await fetch(`${API}/resume/rewrite`, { method: "POST", credentials: "include" });
  if (!res.ok) throw new Error("rewrite failed");
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = "ATS_Resume.docx"; a.click();
  URL.revokeObjectURL(url);
};

// Progress
export const getProgress = () => api.get("/progress").then((r) => r.data);
