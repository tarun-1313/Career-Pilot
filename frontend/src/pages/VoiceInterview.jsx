import React, { useEffect, useRef, useState } from "react";
import { api } from "@/lib/api";
import { toast } from "sonner";
import Editor from "@monaco-editor/react";
import {
  Microphone, MicrophoneSlash, PaperPlaneTilt, Trophy, SpeakerHigh,
  ArrowsClockwise, Sparkle, Code, User, Stop,
} from "@phosphor-icons/react";

/* ---------- helpers ---------- */
const tryBackendTTS = async (text, voice) => {
  try {
    const r = await api.post("/voice/tts", { text, voice });
    return r.data.audio_b64;
  } catch (e) { return null; }
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
    utter.rate = 1.0;
    utter.pitch = 1.0;
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

/* ---------- Waveform animation ---------- */
const Waveform = ({ active }) => (
  <div className="flex items-end gap-1 h-12">
    {[...Array(16)].map((_, i) => (
      <span
        key={i}
        className="w-1.5 bg-[var(--accent)] inline-block"
        style={{
          height: active ? `${20 + Math.abs(Math.sin((Date.now() / 200) + i)) * 80}%` : "10%",
          animation: active ? `pulseBar 0.${(i % 5) + 3}s ease-in-out infinite alternate` : "none",
        }}
      />
    ))}
    <style>{`@keyframes pulseBar { from{height:10%} to{height:90%} }`}</style>
  </div>
);

/* ---------- Setup screen ---------- */
const SetupScreen = ({ onStart }) => {
  const [presets, setPresets] = useState(null);
  const [config, setConfig] = useState({
    role: "AI Engineer",
    interview_type: "technical",
    difficulty: "intermediate",
    personality: "friendly",
    voice: "technical_male",
    use_resume: true,
  });
  const [starting, setStarting] = useState(false);

  useEffect(() => { api.get("/voice-interview/presets").then((r) => setPresets(r.data)); }, []);

  const start = async () => {
    setStarting(true);
    try {
      const r = await api.post("/voice-interview/start", config);
      onStart(r.data);
    } catch (e) { toast.error("Could not start interview"); }
    finally { setStarting(false); }
  };

  if (!presets) return <div className="dot-loader"><span/><span/><span/></div>;

  return (
    <div className="space-y-8 max-w-5xl">
      <div>
        <div className="overline mb-3">VOICE INTERVIEW COPILOT</div>
        <h1 className="font-display text-4xl lg:text-5xl font-black tracking-display">
          Real-time AI <span className="text-accent">voice interviews</span>.
        </h1>
        <p className="text-secondary mt-2">Speak. Get evaluated. Ship. Powered by ElevenLabs + Deepgram + Gemini.</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <div className="flat-card p-6">
          <div className="overline mb-3">ROLE</div>
          <input value={config.role} onChange={(e) => setConfig({ ...config, role: e.target.value })}
            className="w-full bg-elevated border border-default px-3 py-2.5 text-sm outline-none focus:border-[var(--accent)]"
            data-testid="vi-role-input"/>
        </div>

        <div className="flat-card p-6">
          <div className="overline mb-3">USE MY RESUME</div>
          <button onClick={() => setConfig({ ...config, use_resume: !config.use_resume })}
            className={`px-4 py-2 text-sm border ${config.use_resume ? "border-[var(--accent)] text-accent bg-elevated" : "border-default text-secondary"}`}
            data-testid="vi-resume-toggle">
            {config.use_resume ? "Yes — use resume questions" : "No — generic questions"}
          </button>
        </div>

        <div className="flat-card p-6 lg:col-span-2">
          <div className="overline mb-3">INTERVIEW TYPE</div>
          <div className="flex flex-wrap gap-2">
            {presets.types.map((t) => (
              <button key={t} onClick={() => setConfig({ ...config, interview_type: t })}
                className={`px-4 py-2 text-sm border capitalize ${config.interview_type === t ? "border-[var(--accent)] text-accent bg-elevated" : "border-default text-secondary"}`}
                data-testid={`vi-type-${t}`}>
                {t.replace(/_/g, " ")}
              </button>
            ))}
          </div>
        </div>

        <div className="flat-card p-6">
          <div className="overline mb-3">DIFFICULTY</div>
          <div className="flex flex-wrap gap-2">
            {presets.difficulties.map((d) => (
              <button key={d} onClick={() => setConfig({ ...config, difficulty: d })}
                className={`px-3 py-1.5 text-xs border uppercase font-mono ${config.difficulty === d ? "border-[var(--accent)] text-accent" : "border-default text-secondary"}`}
                data-testid={`vi-diff-${d}`}>{d}</button>
            ))}
          </div>
        </div>

        <div className="flat-card p-6">
          <div className="overline mb-3">PERSONALITY</div>
          <div className="flex flex-wrap gap-2">
            {presets.personalities.map((p) => (
              <button key={p.key} onClick={() => setConfig({ ...config, personality: p.key })}
                title={p.desc}
                className={`px-3 py-1.5 text-xs border ${config.personality === p.key ? "border-[var(--accent)] text-accent" : "border-default text-secondary"}`}
                data-testid={`vi-pers-${p.key}`}>{p.label}</button>
            ))}
          </div>
        </div>

        <div className="flat-card p-6 lg:col-span-2">
          <div className="overline mb-3">INTERVIEWER VOICE</div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-2">
            {presets.voices.map((v) => (
              <button key={v.key} onClick={() => setConfig({ ...config, voice: v.key })}
                className={`text-left p-3 border ${config.voice === v.key ? "border-[var(--accent)] bg-elevated" : "border-default"}`}
                data-testid={`vi-voice-${v.key}`}>
                <div className="text-sm">{v.label}</div>
                <div className="overline">{v.gender}</div>
              </button>
            ))}
          </div>
        </div>
      </div>

      <button onClick={start} disabled={starting} className="btn-yellow" data-testid="vi-start-button">
        <Microphone size={18} weight="bold" /> {starting ? "Connecting..." : "Begin voice interview"}
      </button>
    </div>
  );
};

/* ---------- Live interview screen ---------- */
const LiveScreen = ({ doc, setDoc }) => {
  const [recording, setRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [confidence, setConfidence] = useState(null);
  const [aiSpeaking, setAiSpeaking] = useState(false);
  const [busy, setBusy] = useState(false);
  const [showCode, setShowCode] = useState(doc.interview_type === "coding");
  const [code, setCode] = useState("# write your solution here\n");
  const [language, setLanguage] = useState("python");
  const mediaRef = useRef(null);
  const chunksRef = useRef([]);
  const lastSpokenRef = useRef(null);

  const turns = doc.turns || [];
  const currentTurn = turns[turns.length - 1];

  const speak = async (text) => {
    if (!text || lastSpokenRef.current === text) return;
    lastSpokenRef.current = text;
    setAiSpeaking(true);
    const b64 = await tryBackendTTS(text, doc.voice);
    if (b64) await playB64Mp3(b64);
    else await browserTTS(text, doc.voice);
    setAiSpeaking(false);
  };

  useEffect(() => {
    if (currentTurn?.q && !currentTurn.a) speak(currentTurn.q);
    // eslint-disable-next-line
  }, [currentTurn?.q]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mr = new MediaRecorder(stream, { mimeType: "audio/webm" });
      chunksRef.current = [];
      mr.ondataavailable = (e) => e.data.size > 0 && chunksRef.current.push(e.data);
      mr.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop());
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        const fd = new FormData();
        fd.append("file", blob, "answer.webm");
        try {
          const r = await api.post("/voice/stt", fd, { headers: { "Content-Type": "multipart/form-data" } });
          setTranscript((t) => (t ? t + " " : "") + r.data.transcript);
          setConfidence(r.data.confidence);
        } catch { toast.error("Transcription failed"); }
      };
      mr.start();
      mediaRef.current = mr;
      setRecording(true);
    } catch { toast.error("Mic permission denied"); }
  };

  const stopRecording = () => {
    mediaRef.current?.stop();
    setRecording(false);
  };

  const submit = async () => {
    if (!transcript.trim()) { toast.error("Speak or type your answer first"); return; }
    setBusy(true);
    try {
      const r = await api.post("/voice-interview/answer", {
        interview_id: doc.interview_id,
        transcript: transcript.trim(),
        confidence,
        code: showCode ? code : null,
        language: showCode ? language : null,
      });
      // refresh doc
      const fresh = await api.get(`/voice-interview/${doc.interview_id}`);
      setDoc(fresh.data);
      setTranscript("");
      setConfidence(null);
      if (r.data.report) toast.success("Interview complete · report ready");
    } catch { toast.error("Failed to submit"); }
    finally { setBusy(false); }
  };

  return (
    <div className="space-y-6" data-testid="vi-live-root">
      {/* AI avatar */}
      <div className="flat-card p-8 grid md:grid-cols-2 gap-8 items-center">
        <div className="flex items-center gap-6">
          <div className={`w-24 h-24 bg-elevated flex items-center justify-center border ${aiSpeaking ? "border-[var(--accent)]" : "border-default"}`}>
            <User size={48} weight="duotone" className={aiSpeaking ? "text-[var(--accent)]" : "text-secondary"} />
          </div>
          <div>
            <div className="overline">{doc.personality} · {doc.difficulty}</div>
            <h2 className="font-display text-2xl font-extrabold mt-1">{doc.role}</h2>
            <div className="overline mt-1">{doc.interview_type}</div>
          </div>
        </div>
        <div className="flex flex-col items-end">
          <Waveform active={aiSpeaking || recording} />
          <div className="overline mt-3">
            {aiSpeaking ? "INTERVIEWER SPEAKING" : recording ? "LISTENING" : "READY"}
          </div>
        </div>
      </div>

      {/* Q&A log */}
      <div className="flat-card p-8 space-y-5 max-h-[420px] overflow-y-auto">
        {turns.map((t, i) => (
          <div key={i} className="space-y-3">
            <div className="border-l-2 border-[var(--accent)] pl-4">
              <div className="overline mb-1">Q{i + 1} · INTERVIEWER</div>
              <div className="whitespace-pre-wrap">{t.q}</div>
              {t.q === currentTurn?.q && !currentTurn?.a && (
                <button onClick={() => speak(t.q)} className="btn-ghost mt-3 text-xs" data-testid="vi-replay-question">
                  <SpeakerHigh size={14} /> Replay
                </button>
              )}
            </div>
            {t.a && (
              <div className="border-l-2 border-zinc-700 pl-4 ml-2">
                <div className="overline mb-1">A{i + 1} · YOU {t.metrics?.confidence ? `· ${t.metrics.confidence}% confident` : ""}</div>
                <div className="text-secondary whitespace-pre-wrap">{t.a}</div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Recording / answer area */}
      {!doc.report && (
        <div className="flat-card p-6 space-y-4">
          <div className="flex items-center gap-3 justify-between">
            <div className="overline">YOUR ANSWER</div>
            <div className="flex gap-2">
              <button onClick={() => setShowCode((v) => !v)} className="btn-ghost text-xs" data-testid="vi-toggle-code">
                <Code size={14} /> {showCode ? "Hide code" : "Show code editor"}
              </button>
              {!recording ? (
                <button onClick={startRecording} className="btn-yellow text-xs" data-testid="vi-record-button">
                  <Microphone size={14} weight="bold" /> Record
                </button>
              ) : (
                <button onClick={stopRecording} className="btn-yellow text-xs" data-testid="vi-stop-button">
                  <Stop size={14} weight="fill" /> Stop
                </button>
              )}
            </div>
          </div>
          <textarea
            value={transcript}
            onChange={(e) => setTranscript(e.target.value)}
            placeholder="Press Record to speak — or type your answer here..."
            rows={4}
            className="w-full bg-elevated border border-default p-3 text-sm outline-none focus:border-[var(--accent)]"
            data-testid="vi-transcript-input"
          />
          {confidence !== null && (
            <div className="flex items-center gap-3 text-xs font-mono">
              <span className="overline">CONFIDENCE</span>
              <div className="flex-1 h-1 bg-elevated"><div className="h-full bg-accent-yellow" style={{ width: `${confidence}%` }} /></div>
              <span className="text-accent">{confidence}%</span>
            </div>
          )}

          {showCode && (
            <div className="border border-default">
              <div className="flex justify-between p-2 border-b border-default bg-elevated">
                <select value={language} onChange={(e) => setLanguage(e.target.value)}
                  className="bg-base border border-default px-2 py-1 text-xs font-mono"
                  data-testid="vi-language-select">
                  {["python", "javascript", "java", "cpp", "go"].map((l) => <option key={l} value={l}>{l}</option>)}
                </select>
                <span className="overline self-center">CODING SCRATCHPAD</span>
              </div>
              <Editor
                height="260px"
                theme="vs-dark"
                language={language}
                value={code}
                onChange={(v) => setCode(v || "")}
                options={{ fontSize: 13, minimap: { enabled: false }, scrollBeyondLastLine: false }}
              />
            </div>
          )}

          <div className="flex justify-end">
            <button onClick={submit} disabled={busy} className="btn-yellow" data-testid="vi-submit-button">
              <PaperPlaneTilt size={16} weight="bold" /> {busy ? "Submitting..." : "Submit answer"}
            </button>
          </div>
        </div>
      )}

      {/* Report */}
      {doc.report && <Report report={doc.report} onReset={() => setDoc(null)} />}
    </div>
  );
};

/* ---------- Final report ---------- */
const Report = ({ report, onReset }) => {
  const scores = [
    ["TECHNICAL", report.technical_score],
    ["COMMUNICATION", report.communication_score],
    ["CONFIDENCE", report.confidence_score],
    ["PROBLEM-SOLVING", report.problem_solving_score],
    ["CLARITY", report.clarity_score],
  ];
  return (
    <div className="flat-card p-10 space-y-8" data-testid="vi-report">
      <div className="flex items-center gap-4">
        <Trophy size={36} weight="duotone" className="text-[var(--accent)]" />
        <div>
          <div className="overline">FINAL REPORT</div>
          <h2 className="font-display text-4xl font-black">Overall {report.overall}/100</h2>
        </div>
      </div>
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-3">
        {scores.map(([k, v]) => (
          <div key={k} className="border border-default p-4">
            <div className="overline">{k}</div>
            <div className="font-display text-3xl font-black mt-2">{v ?? "—"}</div>
            <div className="h-1 bg-elevated mt-2"><div className="h-full bg-accent-yellow" style={{ width: `${v || 0}%` }} /></div>
          </div>
        ))}
      </div>
      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <div className="overline mb-2">STRENGTHS</div>
          <ul className="text-sm space-y-1 text-secondary">
            {(report.strengths || []).map((s, i) => <li key={i}>• {s}</li>)}
          </ul>
        </div>
        <div>
          <div className="overline mb-2">IMPROVEMENTS</div>
          <ul className="text-sm space-y-1 text-secondary">
            {(report.improvements || []).map((s, i) => <li key={i}>• {s}</li>)}
          </ul>
        </div>
        <div>
          <div className="overline mb-2">RECOMMENDED TOPICS</div>
          <ul className="text-sm space-y-1 text-secondary">
            {(report.recommended_topics || []).map((s, i) => <li key={i}>• {s}</li>)}
          </ul>
        </div>
        <div>
          <div className="overline mb-2">SUGGESTED PROJECTS</div>
          <ul className="text-sm space-y-1 text-secondary">
            {(report.suggested_projects || []).map((s, i) => <li key={i}>• {s}</li>)}
          </ul>
        </div>
      </div>
      <p className="text-secondary text-sm border-t border-default pt-6">{report.summary}</p>
      <button onClick={onReset} className="btn-yellow" data-testid="vi-new-button">
        <ArrowsClockwise size={16} weight="bold" /> New interview
      </button>
    </div>
  );
};

/* ---------- Main ---------- */
export default function VoiceInterview() {
  const [doc, setDoc] = useState(null);
  return doc ? <LiveScreen doc={doc} setDoc={setDoc} /> : <SetupScreen onStart={setDoc} />;
}
