import React, { useEffect, useState } from "react";
import { generateRoadmap, getRoadmap, toggleMilestone } from "@/lib/api";
import { toast } from "sonner";
import { Path, CheckCircle, Circle, Sparkle } from "@phosphor-icons/react";

export default function Roadmap() {
  const [doc, setDoc] = useState(null);
  const [role, setRole] = useState("");
  const [months, setMonths] = useState(6);
  const [loading, setLoading] = useState(false);

  useEffect(() => { getRoadmap().then((d) => { setDoc(d); if (d?.target_role) setRole(d.target_role); }); }, []);

  const gen = async () => {
    setLoading(true);
    try { setDoc(await generateRoadmap(role, months)); toast.success("Roadmap generated"); }
    catch { toast.error("Generation failed"); }
    finally { setLoading(false); }
  };

  const toggle = async (key) => {
    const r = await toggleMilestone(key);
    setDoc({ ...doc, completed_milestones: r.completed_milestones });
  };

  const months_data = doc?.data?.months || [];
  const done = new Set(doc?.completed_milestones || []);

  return (
    <div className="space-y-8" data-testid="roadmap-root">
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-4">
        <div>
          <div className="overline mb-3">LEARNING ROADMAP</div>
          <h1 className="font-display text-4xl lg:text-5xl font-black tracking-display">
            Your <span className="text-accent">{months}-month</span> plan.
          </h1>
        </div>
        <div className="flex gap-3">
          <input
            value={role}
            onChange={(e) => setRole(e.target.value)}
            placeholder="Target role"
            className="bg-elevated border border-default px-3 py-2.5 text-sm outline-none focus:border-[var(--accent)]"
            data-testid="roadmap-role-input"
          />
          <select
            value={months}
            onChange={(e) => setMonths(Number(e.target.value))}
            className="bg-elevated border border-default px-3 py-2.5 text-sm"
            data-testid="roadmap-months-select"
          >
            {[3, 6, 9, 12].map((m) => <option key={m} value={m}>{m} mo</option>)}
          </select>
          <button onClick={gen} disabled={loading} className="btn-yellow" data-testid="roadmap-generate-button">
            <Sparkle size={16} weight="bold" /> {loading ? "Building..." : "Generate"}
          </button>
        </div>
      </div>

      {loading && (
        <div className="flat-card p-12 flex items-center gap-4">
          <div className="dot-loader"><span/><span/><span/></div>
          <div className="overline">BUILDING YOUR PERSONALIZED ROADMAP · ~25S</div>
        </div>
      )}

      {!loading && months_data.length === 0 && (
        <div className="flat-card p-12 text-center text-secondary">
          Set a target role and click <strong className="text-white">Generate</strong> to build your plan.
        </div>
      )}

      <div className="space-y-6">
        {months_data.map((m, i) => (
          <div key={i} className="flat-card p-8">
            <div className="flex items-center justify-between mb-6">
              <div>
                <div className="overline">MONTH {m.month}</div>
                <h2 className="font-display text-2xl font-extrabold mt-1">{m.title}</h2>
                <div className="text-sm text-secondary mt-1">{m.focus}</div>
              </div>
              <div className="text-xs font-mono text-muted">{(m.weekly_goals || []).length} tasks</div>
            </div>
            <div className="grid md:grid-cols-2 gap-3">
              {(m.weekly_goals || []).map((g, j) => {
                const key = `${m.month}-w-${j}`;
                const isDone = done.has(key);
                return (
                  <button
                    key={j}
                    onClick={() => toggle(key)}
                    data-testid={`milestone-${m.month}-${j}`}
                    className="flex items-start gap-3 border border-default hover:border-[var(--accent)] p-4 text-left transition-colors"
                  >
                    {isDone ? (
                      <CheckCircle size={20} weight="fill" className="text-[var(--accent)] shrink-0 mt-0.5" />
                    ) : (
                      <Circle size={20} className="text-zinc-500 shrink-0 mt-0.5" />
                    )}
                    <span className={`text-sm ${isDone ? "line-through text-muted" : ""}`}>{g}</span>
                  </button>
                );
              })}
            </div>
            {(m.projects?.length > 0 || m.certifications?.length > 0) && (
              <div className="grid md:grid-cols-2 gap-6 mt-6 pt-6 border-t border-default">
                {m.projects?.length > 0 && (
                  <div>
                    <div className="overline mb-2">PROJECTS</div>
                    <ul className="text-sm space-y-1">
                      {m.projects.map((p, k) => <li key={k} className="text-secondary">▸ {p}</li>)}
                    </ul>
                  </div>
                )}
                {m.certifications?.length > 0 && (
                  <div>
                    <div className="overline mb-2">CERTIFICATIONS</div>
                    <ul className="text-sm space-y-1">
                      {m.certifications.map((p, k) => <li key={k} className="text-secondary">▸ {p}</li>)}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
