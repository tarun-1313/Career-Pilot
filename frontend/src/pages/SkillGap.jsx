import React, { useState } from "react";
import { skillGap } from "@/lib/api";
import { toast } from "sonner";
import { Target, Lightning } from "@phosphor-icons/react";

const priorityColor = { high: "border-red-500 text-red-400", medium: "border-orange-500 text-orange-400", low: "border-zinc-500 text-zinc-400" };

export default function SkillGap() {
  const [role, setRole] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    setLoading(true);
    try { setData(await skillGap(role)); }
    catch { toast.error("Analysis failed"); }
    finally { setLoading(false); }
  };

  return (
    <div className="space-y-8" data-testid="skillgap-root">
      <div>
        <div className="overline mb-3">SKILL GAP</div>
        <h1 className="font-display text-4xl lg:text-5xl font-black tracking-display">
          What you're <span className="text-accent">missing</span> — ranked.
        </h1>
        <p className="text-secondary mt-2">Tell us the role you're targeting. We'll diff your skills against the market.</p>
      </div>

      <div className="flat-card p-6 flex flex-col md:flex-row gap-3">
        <input
          value={role}
          onChange={(e) => setRole(e.target.value)}
          placeholder="e.g. Senior ML Engineer at a foundation-model lab"
          className="flex-1 bg-elevated border border-default px-3 py-2.5 text-sm outline-none focus:border-[var(--accent)]"
          data-testid="skillgap-role-input"
        />
        <button onClick={run} disabled={loading} className="btn-yellow" data-testid="skillgap-analyze-button">
          <Target size={16} weight="bold" /> {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      {loading && !data && (
        <div className="flat-card p-12 flex items-center gap-4">
          <div className="dot-loader"><span/><span/><span/></div>
          <div className="overline">DIFFING YOUR SKILLS AGAINST THE ROLE · ~15S</div>
        </div>
      )}

      {data && (
        <div className="grid lg:grid-cols-2 gap-6">
          <div className="flat-card p-8">
            <div className="overline mb-3">YOU HAVE</div>
            <div className="flex flex-wrap gap-2">
              {(data.current_skills || []).map((s, i) => (
                <span key={i} className="bg-elevated border border-default px-3 py-1.5 text-xs font-mono">{s}</span>
              ))}
            </div>
          </div>
          <div className="flat-card p-8">
            <div className="overline mb-3">ROLE NEEDS</div>
            <div className="flex flex-wrap gap-2">
              {(data.required_skills || []).map((s, i) => (
                <span key={i} className="bg-elevated border border-default px-3 py-1.5 text-xs font-mono">{s}</span>
              ))}
            </div>
          </div>

          <div className="flat-card p-8 lg:col-span-2">
            <div className="overline mb-4">MISSING — PRIORITIZED</div>
            <div className="space-y-3">
              {(data.missing_skills || []).map((m, i) => (
                <div key={i} className="border border-default p-5">
                  <div className="flex justify-between items-start gap-4">
                    <div>
                      <div className="font-display text-lg font-extrabold">{m.name}</div>
                      <div className="text-sm text-secondary mt-1">{m.reason}</div>
                    </div>
                    <div className="text-right shrink-0">
                      <span className={`border px-2 py-0.5 text-xs font-mono uppercase ${priorityColor[m.priority] || ""}`}>{m.priority}</span>
                      <div className="text-xs text-muted mt-2 font-mono">~{m.estimated_weeks} wks · {m.difficulty}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
