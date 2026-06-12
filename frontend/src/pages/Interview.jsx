import React, { useState } from "react";
import { startInterview, answerInterview } from "@/lib/api";
import { toast } from "sonner";
import { Microphone, PaperPlaneTilt, Trophy } from "@phosphor-icons/react";

const types = [
  { id: "technical", label: "Technical" },
  { id: "hr", label: "HR" },
  { id: "behavioral", label: "Behavioural" },
  { id: "system_design", label: "System Design" },
];

export default function Interview() {
  const [role, setRole] = useState("AI Engineer");
  const [type, setType] = useState("technical");
  const [doc, setDoc] = useState(null);
  const [answer, setAnswer] = useState("");
  const [busy, setBusy] = useState(false);

  const start = async () => {
    setBusy(true);
    try {
      const d = await startInterview(role, type);
      setDoc(d);
    } catch { toast.error("Could not start interview"); }
    finally { setBusy(false); }
  };

  const send = async () => {
    if (!answer.trim() || busy) return;
    setBusy(true);
    try {
      const r = await answerInterview(doc.interview_id, answer);
      setAnswer("");
      // refresh doc
      const newQa = [...(doc.qa || [])];
      if (newQa.length && newQa[newQa.length - 1].a === null) newQa[newQa.length - 1].a = answer.trim();
      if (!r.finished) newQa.push({ q: r.next_question, a: null });
      setDoc({ ...doc, qa: newQa, status: r.finished ? "completed" : "active", report: r.report });
    } catch { toast.error("Answer failed"); }
    finally { setBusy(false); }
  };

  return (
    <div className="space-y-8" data-testid="interview-root">
      <div>
        <div className="overline mb-3">MOCK INTERVIEW</div>
        <h1 className="font-display text-4xl lg:text-5xl font-black tracking-display">
          Practice. <span className="text-accent">Win.</span>
        </h1>
        <p className="text-secondary mt-2">5-question rounds graded across technical depth, communication, and confidence.</p>
      </div>

      {!doc && (
        <div className="flat-card p-8 space-y-5">
          <div>
            <div className="overline mb-2">ROLE</div>
            <input value={role} onChange={(e) => setRole(e.target.value)}
              className="w-full bg-elevated border border-default px-3 py-2.5 text-sm outline-none focus:border-[var(--accent)]"
              data-testid="interview-role-input"/>
          </div>
          <div>
            <div className="overline mb-2">TYPE</div>
            <div className="flex flex-wrap gap-2">
              {types.map((t) => (
                <button key={t.id} onClick={() => setType(t.id)}
                  data-testid={`interview-type-${t.id}`}
                  className={`px-4 py-2 text-sm border ${type === t.id ? "border-[var(--accent)] text-accent bg-elevated" : "border-default text-secondary"}`}>
                  {t.label}
                </button>
              ))}
            </div>
          </div>
          <button onClick={start} disabled={busy} className="btn-yellow" data-testid="interview-start-button">
            <Microphone size={16} weight="bold" /> {busy ? "Starting..." : "Start interview"}
          </button>
        </div>
      )}

      {doc && doc.status !== "completed" && (
        <div className="space-y-4">
          {(doc.qa || []).map((qa, i) => (
            <div key={i} className="space-y-3">
              <div className="flat-card p-5 border-l-2 border-[var(--accent)]">
                <div className="overline mb-2">QUESTION {i + 1}</div>
                <div className="whitespace-pre-wrap">{qa.q}</div>
              </div>
              {qa.a && (
                <div className="flat-card p-5 bg-elevated">
                  <div className="overline mb-2">YOUR ANSWER</div>
                  <div className="whitespace-pre-wrap text-secondary">{qa.a}</div>
                </div>
              )}
            </div>
          ))}
          <div className="flex gap-3">
            <textarea value={answer} onChange={(e) => setAnswer(e.target.value)}
              placeholder="Type your answer..." rows={3}
              className="flex-1 bg-elevated border border-default p-3 text-sm outline-none focus:border-[var(--accent)]"
              data-testid="interview-answer-input"/>
            <button onClick={send} disabled={busy} className="btn-yellow self-end" data-testid="interview-answer-button">
              <PaperPlaneTilt size={16} weight="bold" /> {busy ? "..." : "Submit"}
            </button>
          </div>
        </div>
      )}

      {doc?.report && (
        <div className="flat-card p-10 space-y-6" data-testid="interview-report">
          <div className="flex items-center gap-4">
            <Trophy size={32} weight="duotone" className="text-[var(--accent)]" />
            <div>
              <div className="overline">FINAL REPORT</div>
              <h2 className="font-display text-3xl font-black">Overall {doc.report.overall}/100</h2>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-4">
            {[
              ["TECHNICAL", doc.report.technical_score],
              ["COMMUNICATION", doc.report.communication_score],
              ["CONFIDENCE", doc.report.confidence_score],
            ].map(([k, v]) => (
              <div key={k} className="border border-default p-5">
                <div className="overline">{k}</div>
                <div className="font-display text-3xl font-black mt-2">{v}</div>
                <div className="h-1 bg-elevated mt-3"><div className="h-full bg-accent-yellow" style={{ width: `${v}%` }} /></div>
              </div>
            ))}
          </div>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <div className="overline mb-2">STRENGTHS</div>
              <ul className="text-sm space-y-1 text-secondary">
                {(doc.report.strengths || []).map((s, i) => <li key={i}>• {s}</li>)}
              </ul>
            </div>
            <div>
              <div className="overline mb-2">IMPROVEMENTS</div>
              <ul className="text-sm space-y-1 text-secondary">
                {(doc.report.improvements || []).map((s, i) => <li key={i}>• {s}</li>)}
              </ul>
            </div>
          </div>
          <button onClick={() => setDoc(null)} className="btn-ghost" data-testid="interview-new-button">
            New interview
          </button>
        </div>
      )}
    </div>
  );
}
