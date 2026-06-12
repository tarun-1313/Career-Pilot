import React, { useEffect, useRef, useState, useCallback } from "react";
import { api, API } from "@/lib/api";
import { toast } from "sonner";
import { motion, AnimatePresence } from "framer-motion";
import Editor from "@monaco-editor/react";
import {
  Microphone, PaperPlaneTilt, Trophy, SpeakerHigh, ArrowsClockwise,
  Code, User, Stop, FilePdf, VideoCamera, VideoCameraSlash, CircleNotch,
  Clock, Waveform, ChartBar, Sparkle, X,
} from "@phosphor-icons/react";

/* ---------- Audio helpers ---------- */
const tryBackendTTS = async (text, voice) => {
  try {
    const r = await api.post("/voice/tts", { text, voice });
    return r.data.audio_b64;
  } catch { return null; }
};

const browserTTS = (text, voice) =>
  new Promise((resolve) => {
    if (!("speechSynthesis" in window)) return resolve();
    const utter = new SpeechSynthesisUtterance(text);
    const voices = window.speechSynthesis.getVoices();
    const female = voice?.includes("female") || voice?.includes("hr_female") || voice?.includes("startup_friendly");
    const match = voices.find((v) => /en/i.test(v.lang) && (female ? /female|samantha|google uk english female/i.test(v.name) : /male|google uk english male|daniel/i.test(v.name)))
              || voices.find((v) => /en/i.test(v.lang)) || voices[0];
    if (match) utter.voice = match;
    utter.rate = 1.0; utter.pitch = 1.0;
    utter.onend = () => resolve();
    utter.onerror = () => resolve();
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utter);
  });

const playB64Mp3 = (b64) =>
  new Promise((resolve) => {
    const audio = new Audio("data:audio/mpeg;base64," + b64);
    audio.onended = () => resolve();
    audio.onerror = () => resolve();
    audio.play().catch(() => resolve());
  });

<<<<<<< HEAD
/* ---------- WebSocket live STT (with REST fallback) ---------- */
const useLiveSTT = (interviewId, sessionToken) => {
  const mrRef = useRef(null);
  const streamRef = useRef(null);
  const chunksRef = useRef([]);
=======
/* ---------- WebSocket live STT ---------- */
const useLiveSTT = (interviewId, sessionToken) => {
  const wsRef = useRef(null);
  const mrRef = useRef(null);
  const streamRef = useRef(null);
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
  const [interim, setInterim] = useState("");
  const [finalText, setFinalText] = useState("");
  const [recording, setRecording] = useState(false);

<<<<<<< HEAD
  const getSupportedMimeType = () => {
    const types = [
      "audio/webm;codecs=opus",
      "audio/webm",
      "audio/ogg;codecs=opus",
      "audio/mp4",
    ];
    for (const type of types) {
      if (MediaRecorder.isTypeSupported(type)) return type;
    }
    return undefined; // Use default
  };

  const start = useCallback(async () => {
    if (recording) return;
    setInterim(""); setFinalText(""); chunksRef.current = [];
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: { 
          echoCancellation: true, 
          noiseSuppression: true, 
          autoGainControl: true 
        } 
      });
      streamRef.current = stream;
      
      const mimeType = getSupportedMimeType();
      const mr = mimeType 
        ? new MediaRecorder(stream, { mimeType }) 
        : new MediaRecorder(stream);
      
      mrRef.current = mr;
      mr.ondataavailable = async (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };
      mr.start(250); // Chunking for reliability
      setRecording(true);
      toast.success("Recording started!");
    } catch (e) { 
      console.error("Mic error:", e);
      toast.error("Mic permission denied or not available"); 
    }
  }, [recording]);

  const stop = useCallback(async () => {
    return new Promise(async (resolve) => {
      const mr = mrRef.current;
      const stream = streamRef.current;
      
      const finalize = async () => {
        setRecording(false);
        try { 
          if (stream) {
            stream.getTracks().forEach((t) => t.stop()); 
          }
        } catch(e) { console.error(e); }
        mrRef.current = null; streamRef.current = null;
        
        // Send to REST endpoint if we have chunks
        if (chunksRef.current.length > 0) {
          try {
            const blob = new Blob(chunksRef.current, { type: mr?.mimeType || "audio/webm" });
            const formData = new FormData();
            formData.append("file", blob, "recording.webm");
            
            const r = await fetch(`${API}/voice/stt`, { 
              method: "POST", 
              credentials: "include", 
              body: formData 
            });
            if (r.ok) {
              const data = await r.json();
              if (data.transcript) {
                setFinalText((t) => (t ? t + " " : "") + data.transcript.trim());
              }
            }
          } catch(e) { 
            console.error("STT REST error:", e);
            toast.warning("Transcription unavailable, but recording saved locally (check console)"); 
          }
        }
        chunksRef.current = [];
        setTimeout(() => resolve(), 250);
      };
      
      if (!mr) {
        await finalize();
        return;
      }
      
      mr.onstop = finalize;
      try { 
        mr.stop(); 
      } catch { 
        await finalize(); 
      }
=======
  const start = useCallback(async () => {
    if (recording) return;
    setInterim(""); setFinalText("");
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      // Try WS streaming first
      const wsProto = window.location.protocol === "https:" ? "wss:" : "ws:";
      const wsUrl = `${API.replace(/^https?:/, wsProto)}/voice/stt-ws?token=${encodeURIComponent(sessionToken || "")}`;
      const ws = new WebSocket(wsUrl);
      ws.binaryType = "arraybuffer";
      wsRef.current = ws;
      let mr;
      ws.onopen = () => {
        mr = new MediaRecorder(stream, { mimeType: "audio/webm;codecs=opus" });
        mrRef.current = mr;
        mr.ondataavailable = async (e) => {
          if (e.data.size > 0 && ws.readyState === WebSocket.OPEN) {
            const buf = await e.data.arrayBuffer();
            ws.send(buf);
          }
        };
        mr.start(250); // 250ms chunks for low latency
        setRecording(true);
      };
      ws.onmessage = (ev) => {
        try {
          const msg = JSON.parse(ev.data);
          if (msg.type === "transcript" && msg.text) {
            if (msg.is_final) {
              setFinalText((t) => (t ? t + " " : "") + msg.text);
              setInterim("");
            } else {
              setInterim(msg.text);
            }
          }
        } catch {}
      };
      ws.onerror = () => { /* fallback handled by REST in stop() */ };
      ws.onclose = () => { setRecording(false); };
    } catch (e) { toast.error("Mic permission denied"); }
  }, [recording, sessionToken]);

  const stop = useCallback(async () => {
    return new Promise((resolve) => {
      const mr = mrRef.current;
      const ws = wsRef.current;
      const stream = streamRef.current;
      const done = () => {
        setRecording(false);
        try { stream?.getTracks().forEach((t) => t.stop()); } catch {}
        try { ws?.close(); } catch {}
        mrRef.current = null; wsRef.current = null; streamRef.current = null;
        // Allow a tick for final transcript
        setTimeout(() => resolve(), 250);
      };
      if (!mr) return done();
      mr.onstop = done;
      try { mr.stop(); } catch { done(); }
>>>>>>> 7a4583bb30b4662d8be51904ce12acd3b81fe09b
    });
  }, []);

  return { start, stop, recording, interim, finalText, setFinalText };
};

/* ---------- Waveform ---------- */
const Waveform32 = ({ active }) => (
  <div className="flex items-end gap-[2px] h-8">
    {[...Array(28)].map((_, i) => (
      <motion.span
        key={i}
        animate={active ? { height: ["18%", "85%", "30%", "70%", "18%"] } : { height: "12%" }}
        transition={{ duration: 1.2 + (i % 5) * 0.1, repeat: active ? Infinity : 0, delay: i * 0.04, ease: "easeInOut" }}
        className="w-[2.5px] bg-gradient-to-t from-blue-500/40 to-blue-300 inline-block"
      />
    ))}
  </div>
);

/* ---------- Webcam emotion ---------- */
const FACE_API_CDN = "https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/dist/face-api.min.js";
const FACE_MODELS = "https://justadudewhohacks.github.io/face-api.js/models";
const ensureFaceApi = async () => {
  if (window.faceapi) return window.faceapi;
  await new Promise((res, rej) => {
    const s = document.createElement("script"); s.src = FACE_API_CDN; s.onload = res; s.onerror = rej;
    document.head.appendChild(s);
  });
  await window.faceapi.nets.tinyFaceDetector.loadFromUri(FACE_MODELS);
  await window.faceapi.nets.faceExpressionNet.loadFromUri(FACE_MODELS);
  return window.faceapi;
};
const useWebcamEmotion = (enabled, onEmotions) => {
  const videoRef = useRef(null);
  const intervalRef = useRef(null);
  const streamRef = useRef(null);
  useEffect(() => {
    if (!enabled) {
      if (intervalRef.current) clearInterval(intervalRef.current);
      if (streamRef.current) streamRef.current.getTracks().forEach((t) => t.stop());
      return;
    }
    let cancelled = false;
    (async () => {
      try {
        const fa = await ensureFaceApi();
        const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 320, height: 240 } });
        if (cancelled) { stream.getTracks().forEach((t) => t.stop()); return; }
        streamRef.current = stream;
        if (videoRef.current) { videoRef.current.srcObject = stream; await videoRef.current.play(); }
        intervalRef.current = setInterval(async () => {
          if (!videoRef.current) return;
          try {
            const det = await fa.detectSingleFace(videoRef.current, new fa.TinyFaceDetectorOptions({ inputSize: 224, scoreThreshold: 0.5 })).withFaceExpressions();
            if (det?.expressions) onEmotions(det.expressions);
          } catch {}
        }, 1200);
      } catch (e) { console.warn("webcam init failed", e); }
    })();
    return () => {
      cancelled = true;
      if (intervalRef.current) clearInterval(intervalRef.current);
      if (streamRef.current) streamRef.current.getTracks().forEach((t) => t.stop());
    };
  }, [enabled]); // eslint-disable-line
  return videoRef;
};

/* ============================================================ */
/* ============== SETUP SCREEN — minimal corporate ============ */
/* ============================================================ */
const SetupScreen = ({ onStart }) => {
  const [presets, setPresets] = useState(null);
  const [config, setConfig] = useState({
    role: "Senior ML Engineer", interview_type: "technical", difficulty: "intermediate",
    personality: "friendly", voice: "technical_male", use_resume: true,
  });
  const [starting, setStarting] = useState(false);

  useEffect(() => { api.get("/voice-interview/presets").then((r) => setPresets(r.data)); }, []);

  const start = async () => {
    setStarting(true);
    try { const r = await api.post("/voice-interview/start", config); onStart(r.data); }
    catch { toast.error("Could not start interview"); }
    finally { setStarting(false); }
  };

  if (!presets) return <div className="dot-loader"><span/><span/><span/></div>;

  return (
    <div className="max-w-4xl space-y-10" data-testid="vi-setup">
      <div>
        <div className="overline mb-3 flex items-center gap-2 text-zinc-500">
          <span className="block w-1.5 h-1.5 bg-blue-400 animate-pulse rounded-full" />
          AI INTERVIEW SYSTEM · v3
        </div>
        <h1 className="font-display text-4xl lg:text-5xl font-black tracking-[-0.03em] leading-[1.05]">
          Configure your interview.
        </h1>
        <p className="text-zinc-400 mt-3 max-w-2xl">
          Six interviewer personas. Four difficulty tiers. Voice + Code + Webcam.
          Built for engineers preparing for FAANG, OpenAI, and Anthropic-style loops.
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-px bg-white/[0.06] border border-white/[0.06]">
        <div className="bg-[#0a0a0a] p-6">
          <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-3">ROLE</div>
          <input value={config.role} onChange={(e) => setConfig({ ...config, role: e.target.value })}
            className="w-full bg-transparent border-0 border-b border-white/10 px-0 py-2.5 text-lg outline-none focus:border-blue-400 transition-colors"
            data-testid="vi-role-input"/>
        </div>
        <div className="bg-[#0a0a0a] p-6">
          <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-3">RESUME GROUNDING</div>
          <button onClick={() => setConfig({ ...config, use_resume: !config.use_resume })}
            className={`text-sm py-1 ${config.use_resume ? "text-blue-300" : "text-zinc-500"}`}
            data-testid="vi-resume-toggle">
            {config.use_resume ? "ENABLED · Questions will reference your projects" : "DISABLED · Generic questions only"}
          </button>
        </div>
      </div>

      <div className="space-y-6">
        <div>
          <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-3">INTERVIEW TYPE</div>
          <div className="flex flex-wrap gap-2">
            {presets.types.map((t) => (
              <button key={t} onClick={() => setConfig({ ...config, interview_type: t })}
                className={`px-4 py-2 text-sm border capitalize transition-all ${config.interview_type === t ? "border-white bg-white text-black" : "border-white/10 text-zinc-400 hover:border-white/30 hover:text-white"}`}
                data-testid={`vi-type-${t}`}>
                {t.replace(/_/g, " ")}
              </button>
            ))}
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-3">DIFFICULTY</div>
            <div className="flex flex-wrap gap-2">
              {presets.difficulties.map((d) => (
                <button key={d} onClick={() => setConfig({ ...config, difficulty: d })}
                  className={`px-3 py-1.5 text-xs uppercase font-mono tracking-widest border ${config.difficulty === d ? "border-blue-400 text-blue-300" : "border-white/10 text-zinc-500 hover:text-white"}`}
                  data-testid={`vi-diff-${d}`}>{d}</button>
              ))}
            </div>
          </div>
          <div>
            <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-3">INTERVIEWER PERSONA</div>
            <div className="flex flex-wrap gap-2">
              {presets.personalities.map((p) => (
                <button key={p.key} onClick={() => setConfig({ ...config, personality: p.key })}
                  title={p.desc}
                  className={`px-3 py-1.5 text-xs border ${config.personality === p.key ? "border-blue-400 text-blue-300" : "border-white/10 text-zinc-500 hover:text-white"}`}
                  data-testid={`vi-pers-${p.key}`}>{p.label}</button>
              ))}
            </div>
          </div>
        </div>

        <div>
          <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-3">VOICE</div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-2">
            {presets.voices.map((v) => (
              <button key={v.key} onClick={() => setConfig({ ...config, voice: v.key })}
                className={`text-left p-4 border transition-all ${config.voice === v.key ? "border-blue-400 bg-blue-500/[0.04]" : "border-white/10 hover:border-white/30"}`}
                data-testid={`vi-voice-${v.key}`}>
                <div className="text-sm text-white">{v.label}</div>
                <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mt-1">{v.gender}</div>
              </button>
            ))}
          </div>
        </div>
      </div>

      <button onClick={start} disabled={starting}
        className="bg-white text-black font-semibold text-sm px-6 py-3 inline-flex items-center gap-2 hover:bg-zinc-200 transition-colors disabled:opacity-50"
        data-testid="vi-start-button">
        {starting ? <CircleNotch size={16} className="animate-spin" /> : <Microphone size={16} weight="bold" />}
        {starting ? "Connecting to interviewer..." : "Begin interview"}
      </button>
    </div>
  );
};

/* ============================================================ */
/* =============== LIVE SCREEN — enterprise UI ================ */
/* ============================================================ */
const LiveScreen = ({ doc, setDoc }) => {
  const [aiSpeaking, setAiSpeaking] = useState(false);
  const [aiStatus, setAiStatus] = useState("ready"); // ready | speaking | listening | analyzing
  const [busy, setBusy] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [showCode, setShowCode] = useState(doc.interview_type === "coding");
  const [code, setCode] = useState("# write your solution here\n");
  const [language, setLanguage] = useState("python");
  const [webcamOn, setWebcamOn] = useState(false);
  const [emotions, setEmotions] = useState(null);
  const [timer, setTimer] = useState(0);
  const [livePartial, setLivePartial] = useState("");
  const sessionToken = (document.cookie.match(/session_token=([^;]+)/) || [])[1] || "";
  const lastSpokenRef = useRef(null);
  const lastTurnRef = useRef(0);

  const turns = doc.turns || [];
  const currentTurn = turns[turns.length - 1];
  const completedAnswers = turns.filter((t) => t.a).length;
  const totalExpected = 6;

  const liveSTT = useLiveSTT(doc.interview_id, sessionToken);

  // pipe partial transcript into UI
  useEffect(() => {
    setLivePartial(liveSTT.interim);
    if (liveSTT.finalText) setTranscript(liveSTT.finalText);
    setAiStatus(liveSTT.recording ? "listening" : aiSpeaking ? "speaking" : "ready");
  }, [liveSTT.interim, liveSTT.finalText, liveSTT.recording, aiSpeaking]);

  const videoRef = useWebcamEmotion(webcamOn, (ex) => {
    setEmotions(ex);
    api.post("/voice-interview/emotion", {
      interview_id: doc.interview_id, turn_index: Math.max(0, turns.length - 1), emotions: ex,
    }).catch(() => {});
  });

  // session timer
  useEffect(() => {
    const i = setInterval(() => setTimer((t) => t + 1), 1000);
    return () => clearInterval(i);
  }, []);

  // speak new question once
  const speak = useCallback(async (text) => {
    if (!text || lastSpokenRef.current === text) return;
    lastSpokenRef.current = text;
    setAiSpeaking(true); setAiStatus("speaking");
    const b64 = await tryBackendTTS(text, doc.voice);
    if (b64) await playB64Mp3(b64);
    else await browserTTS(text, doc.voice);
    setAiSpeaking(false); setAiStatus("ready");
  }, [doc.voice]);

  useEffect(() => {
    if (currentTurn?.q && !currentTurn.a) speak(currentTurn.q);
    // eslint-disable-next-line
  }, [currentTurn?.q]);

  const submit = async () => {
    if (!transcript.trim()) { toast.error("Speak or type your answer first"); return; }
    setBusy(true); setAiStatus("analyzing");
    try {
      await api.post("/voice-interview/answer", {
        interview_id: doc.interview_id,
        transcript: transcript.trim(),
        code: showCode ? code : null,
        language: showCode ? language : null,
      });
      const fresh = await api.get(`/voice-interview/${doc.interview_id}`);
      setDoc(fresh.data);
      setTranscript(""); setLivePartial("");
      liveSTT.setFinalText("");
      if (fresh.data.report) toast.success("Interview complete · report ready");
    } catch { toast.error("Failed to submit"); }
    finally { setBusy(false); setAiStatus("ready"); }
  };

  const fmtTime = (s) => `${String(Math.floor(s/60)).padStart(2,"0")}:${String(s%60).padStart(2,"0")}`;

  if (doc.report) return <Report report={doc.report} interviewId={doc.interview_id} onReset={() => setDoc(null)} />;

  return (
    <div className="space-y-4 -mx-6 lg:-mx-10 -mt-8" data-testid="vi-live-root">
      {/* TOP HEADER */}
      <div className="border-b border-white/[0.06] bg-zinc-950/40 backdrop-blur-xl">
        <div className="px-6 lg:px-10 py-3 flex items-center justify-between">
          {/* left */}
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-9 h-9 bg-blue-500/[0.08] border border-blue-500/20 flex items-center justify-center">
                <User size={16} weight="duotone" className="text-blue-300" />
              </div>
              <div>
                <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">
                  {doc.personality?.replace(/_/g, " ")} · {doc.interview_type}
                </div>
                <div className="text-sm font-medium">{doc.role} Interview</div>
              </div>
            </div>
          </div>

          {/* center: timer + status */}
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2 text-sm font-mono">
              <Clock size={14} className="text-zinc-500" />
              <span className="text-zinc-300 tabular-nums">{fmtTime(timer)}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className={`block w-1.5 h-1.5 rounded-full ${
                aiStatus === "listening" ? "bg-emerald-400 animate-pulse" :
                aiStatus === "speaking" ? "bg-blue-400 animate-pulse" :
                aiStatus === "analyzing" ? "bg-amber-400 animate-pulse" : "bg-zinc-600"
              }`} />
              <span className="text-[10px] font-mono uppercase tracking-widest text-zinc-400">
                AI · {aiStatus}
              </span>
            </div>
            <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 hidden md:block">
              QUESTION {Math.min(turns.length, totalExpected)} / {totalExpected}
            </div>
          </div>

          {/* right: webcam + waveform */}
          <div className="flex items-center gap-3">
            <button onClick={() => setWebcamOn((v) => !v)}
              className={`p-2 border ${webcamOn ? "border-blue-400 text-blue-300" : "border-white/10 text-zinc-500 hover:text-white"}`}
              data-testid="vi-webcam-toggle"
              aria-label="toggle webcam">
              {webcamOn ? <VideoCamera size={14} /> : <VideoCameraSlash size={14} />}
            </button>
            <div className="hidden md:block">
              <Waveform32 active={aiSpeaking || liveSTT.recording} />
            </div>
          </div>
        </div>

        {/* progress */}
        <div className="h-px bg-white/[0.04]">
          <motion.div
            className="h-full bg-blue-400"
            initial={{ width: 0 }}
            animate={{ width: `${(completedAnswers / totalExpected) * 100}%` }}
            transition={{ duration: 0.4 }}
          />
        </div>
      </div>

      {/* MAIN GRID */}
      <div className="px-6 lg:px-10 grid lg:grid-cols-12 gap-6">
        {/* Center: Transcript */}
        <div className="lg:col-span-8 space-y-4">
          {/* Q&A log */}
          <div className="bg-zinc-950/30 border border-white/[0.06] rounded-sm">
            <div className="border-b border-white/[0.06] px-5 py-3 flex items-center justify-between">
              <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 flex items-center gap-2">
                <span className="block w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                LIVE TRANSCRIPT · DEEPGRAM
              </div>
              <button onClick={() => speak(currentTurn?.q)} disabled={!currentTurn?.q}
                className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 hover:text-white flex items-center gap-1"
                data-testid="vi-replay-question">
                <SpeakerHigh size={12} /> REPLAY
              </button>
            </div>
            <div className="p-6 space-y-5 max-h-[420px] overflow-y-auto">
              <AnimatePresence>
                {turns.map((t, i) => (
                  <motion.div key={i} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
                    <div className="text-[10px] font-mono uppercase tracking-widest text-blue-400 mb-1.5">
                      INTERVIEWER · Q{i + 1}
                    </div>
                    <p className="text-base text-zinc-100 leading-relaxed">{t.q}</p>
                    {t.a && (
                      <div className="mt-4 pl-4 border-l border-white/10">
                        <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-1.5">YOU</div>
                        <p className="text-sm text-zinc-400 leading-relaxed">{t.a}</p>
                      </div>
                    )}
                  </motion.div>
                ))}
                {livePartial && (
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="pl-4 border-l border-emerald-400/40">
                    <div className="text-[10px] font-mono uppercase tracking-widest text-emerald-400 mb-1.5">YOU · LIVE</div>
                    <p className="text-sm text-zinc-300 leading-relaxed italic">{livePartial}<span className="inline-block w-1.5 h-3 bg-emerald-400 ml-1 animate-pulse" /></p>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>

          {/* Code panel */}
          {showCode && (
            <div className="border border-white/[0.06] rounded-sm bg-zinc-950/40">
              <div className="flex justify-between items-center px-4 py-2 border-b border-white/[0.06]">
                <div className="flex items-center gap-3">
                  <Code size={14} className="text-blue-400" />
                  <span className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">CODING WORKSPACE</span>
                </div>
                <select value={language} onChange={(e) => setLanguage(e.target.value)}
                  className="bg-transparent border border-white/10 text-zinc-300 px-2 py-1 text-xs font-mono outline-none"
                  data-testid="vi-language-select">
                  {["python", "javascript", "java", "cpp", "go"].map((l) => <option key={l} value={l}>{l}</option>)}
                </select>
              </div>
              <Editor
                height="320px" theme="vs-dark" language={language} value={code}
                onChange={(v) => setCode(v || "")}
                options={{ fontSize: 13, minimap: { enabled: false }, scrollBeyondLastLine: false, fontFamily: "JetBrains Mono, monospace" }}
              />
            </div>
          )}

          {/* Answer input */}
          <div className={`border ${liveSTT.recording ? "border-emerald-400/50 shadow-[0_0_30px_rgba(52,211,153,0.15)]" : "border-white/[0.06]"} bg-zinc-950/40 transition-all`}>
            <textarea
              value={transcript + (livePartial ? ` ${livePartial}` : "")}
              onChange={(e) => { setTranscript(e.target.value); liveSTT.setFinalText(e.target.value); }}
              placeholder="Press the microphone to speak — or type your response here."
              rows={4}
              className="w-full bg-transparent p-4 text-sm text-zinc-100 outline-none resize-none placeholder:text-zinc-600"
              data-testid="vi-transcript-input"
            />
            <div className="flex items-center justify-between border-t border-white/[0.04] px-3 py-2">
              <div className="flex items-center gap-2">
                {!liveSTT.recording ? (
                  <button onClick={liveSTT.start}
                    className="px-3 py-1.5 text-xs border border-white/10 hover:border-emerald-400 hover:text-emerald-300 flex items-center gap-1.5 transition-colors"
                    data-testid="vi-record-button">
                    <Microphone size={12} /> RECORD
                  </button>
                ) : (
                  <button onClick={liveSTT.stop}
                    className="px-3 py-1.5 text-xs border border-emerald-400 text-emerald-300 flex items-center gap-1.5"
                    data-testid="vi-stop-button">
                    <Stop size={12} weight="fill" /> STOP · {fmtTime(timer % 600)}
                  </button>
                )}
                <button onClick={() => setShowCode((v) => !v)}
                  className="px-3 py-1.5 text-xs border border-white/10 hover:border-white/30 flex items-center gap-1.5 text-zinc-400 hover:text-white"
                  data-testid="vi-toggle-code">
                  <Code size={12} /> {showCode ? "HIDE CODE" : "CODE"}
                </button>
              </div>
              <button onClick={submit} disabled={busy || liveSTT.recording}
                className="bg-white text-black font-semibold text-xs px-4 py-1.5 flex items-center gap-1.5 hover:bg-zinc-200 transition-colors disabled:opacity-50"
                data-testid="vi-submit-button">
                {busy ? <CircleNotch size={12} className="animate-spin" /> : <PaperPlaneTilt size={12} weight="bold" />}
                {busy ? "ANALYZING..." : "SUBMIT"}
              </button>
            </div>
          </div>
        </div>

        {/* Right: AI analytics + Webcam */}
        <div className="lg:col-span-4 space-y-4">
          {/* Status card */}
          <div className="border border-white/[0.06] bg-zinc-950/40 p-5">
            <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-3 flex items-center gap-2">
              <Sparkle size={10} weight="fill" className="text-blue-400" />
              AI INTERVIEWER STATUS
            </div>
            <div className="space-y-3">
              {[
                ["LISTENING", aiStatus === "listening"],
                ["SPEAKING", aiStatus === "speaking"],
                ["PROCESSING", aiStatus === "analyzing"],
                ["EVALUATING", busy],
              ].map(([k, active]) => (
                <div key={k} className="flex items-center justify-between">
                  <span className={`text-xs font-mono ${active ? "text-white" : "text-zinc-600"}`}>{k}</span>
                  <span className={`block w-1.5 h-1.5 rounded-full ${active ? "bg-emerald-400 animate-pulse" : "bg-zinc-800"}`} />
                </div>
              ))}
            </div>
          </div>

          {/* Webcam preview */}
          {webcamOn && (
            <div className="border border-white/[0.06] bg-zinc-950/40">
              <div className="px-3 py-2 border-b border-white/[0.06] flex justify-between items-center">
                <span className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">WEBCAM · EMOTION</span>
                <button onClick={() => setWebcamOn(false)} className="text-zinc-500 hover:text-white"><X size={12} /></button>
              </div>
              <div className="relative">
                <video ref={videoRef} muted playsInline className="w-full aspect-video object-cover" />
                {emotions && (
                  <div className="absolute bottom-2 left-2 right-2 flex flex-wrap gap-1">
                    {Object.entries(emotions).sort((a,b)=>b[1]-a[1]).slice(0,3).map(([e, v]) => (
                      <span key={e} className="bg-black/70 backdrop-blur-md border border-white/10 px-2 py-0.5 text-[10px] font-mono">
                        {e} · {Math.round(v*100)}%
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Confidence metrics (interim) */}
          <div className="border border-white/[0.06] bg-zinc-950/40 p-5">
            <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-4 flex items-center gap-2">
              <ChartBar size={10} weight="duotone" className="text-blue-400" />
              SESSION ANALYTICS
            </div>
            <div className="space-y-3">
              {[
                ["QUESTIONS ANSWERED", `${completedAnswers}/${totalExpected}`],
                ["INTERVIEW DURATION", fmtTime(timer)],
                ["INTERVIEWER", doc.voice?.replace(/_/g, " ")],
                ["DIFFICULTY", doc.difficulty?.toUpperCase()],
              ].map(([k, v]) => (
                <div key={k}>
                  <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">{k}</div>
                  <div className="text-sm text-zinc-200 mt-0.5">{v}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-600 leading-relaxed px-2">
            Live transcription powered by Deepgram Nova-3 · WebSocket streaming. Evaluation via Gemini 2.5 Flash. All data stored in MongoDB Atlas.
          </div>
        </div>
      </div>
    </div>
  );
};

/* ============================================================ */
/* ====================== FINAL REPORT ======================== */
/* ============================================================ */
const Report = ({ report, interviewId, onReset }) => {
  const downloadPdf = async () => {
    try {
      const res = await fetch(`${API}/voice-interview/${interviewId}/pdf`, { method: "GET", credentials: "include" });
      if (!res.ok) throw new Error();
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url; a.download = "CareerPilot_Interview_Report.pdf"; a.click();
      URL.revokeObjectURL(url);
      toast.success("Report downloaded");
    } catch { toast.error("PDF download failed"); }
  };

  const scores = [
    ["TECHNICAL", report.technical_score],
    ["COMMUNICATION", report.communication_score],
    ["CONFIDENCE", report.confidence_score],
    ["PROBLEM-SOLVING", report.problem_solving_score],
    ["CLARITY", report.clarity_score],
  ];

  return (
    <div className="space-y-8" data-testid="vi-report">
      <div className="border border-white/[0.06] bg-gradient-to-br from-blue-500/[0.04] to-transparent p-10">
        <div className="flex items-center gap-4">
          <Trophy size={32} weight="duotone" className="text-blue-300" />
          <div>
            <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">INTERVIEW REPORT</div>
            <h2 className="font-display text-4xl font-black tracking-[-0.03em]">Overall {report.overall}/100</h2>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-5 gap-px bg-white/[0.06] border border-white/[0.06]">
        {scores.map(([k, v]) => (
          <div key={k} className="bg-[#0a0a0a] p-5">
            <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">{k}</div>
            <div className="font-display text-3xl font-black mt-2">{v ?? "—"}</div>
            <div className="h-[2px] bg-white/[0.04] mt-3 overflow-hidden">
              <motion.div initial={{ width: 0 }} animate={{ width: `${v || 0}%` }} transition={{ duration: 1, ease: "easeOut" }}
                className="h-full bg-blue-400" />
            </div>
          </div>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {[
          ["STRENGTHS", report.strengths],
          ["IMPROVEMENTS", report.improvements],
          ["RECOMMENDED TOPICS", report.recommended_topics],
          ["SUGGESTED PROJECTS", report.suggested_projects],
        ].map(([k, list]) => (
          <div key={k} className="border border-white/[0.06] bg-zinc-950/40 p-6">
            <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-3">{k}</div>
            <ul className="space-y-1.5 text-sm">
              {(list || []).map((s, i) => <li key={i} className="text-zinc-400">— {s}</li>)}
            </ul>
          </div>
        ))}
      </div>

      <p className="text-zinc-400 text-sm border-t border-white/[0.06] pt-6 max-w-3xl">{report.summary}</p>

      <div className="flex gap-3 flex-wrap">
        <button onClick={onReset}
          className="bg-white text-black font-semibold text-sm px-5 py-2.5 inline-flex items-center gap-2 hover:bg-zinc-200 transition-colors"
          data-testid="vi-new-button">
          <ArrowsClockwise size={14} weight="bold" /> New interview
        </button>
        <button onClick={downloadPdf}
          className="border border-white/10 hover:border-white/30 text-sm px-5 py-2.5 inline-flex items-center gap-2 text-zinc-300 hover:text-white transition-colors"
          data-testid="vi-pdf-button">
          <FilePdf size={14} weight="duotone" /> Download PDF
        </button>
      </div>
    </div>
  );
};

/* ---------- Main ---------- */
export default function VoiceInterview() {
  const [doc, setDoc] = useState(null);
  return doc ? <LiveScreen doc={doc} setDoc={setDoc} /> : <SetupScreen onStart={setDoc} />;
}
