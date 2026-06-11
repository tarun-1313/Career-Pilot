import React, { useEffect, useState } from "react";
import { recommendCareers, listCareers } from "@/lib/api";
import { toast } from "sonner";
import { Sparkle, TrendUp, CurrencyInr, Lightning } from "@phosphor-icons/react";

export default function Careers() {
  const [careers, setCareers] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => { listCareers().then((d) => setCareers(d.careers || [])); }, []);

  const generate = async () => {
    setLoading(true);
    try {
      const r = await recommendCareers();
      setCareers(r.careers || []);
      toast.success("Career matches generated");
    } catch (e) {
      toast.error("Generation failed. Complete your profile first?");
    } finally { setLoading(false); }
  };

  return (
    <div className="space-y-8" data-testid="careers-root">
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-4">
        <div>
          <div className="overline mb-3">CAREER PATHS</div>
          <h1 className="font-display text-4xl lg:text-5xl font-black tracking-display">
            Your top <span className="text-accent">5 matches</span>.
          </h1>
          <p className="text-secondary mt-2">Cross-referenced against your skills, interests, and current market signals.</p>
        </div>
        <button onClick={generate} disabled={loading} className="btn-yellow" data-testid="generate-careers-button">
          <Sparkle size={16} weight="bold" /> {loading ? "Thinking..." : "Regenerate"}
        </button>
      </div>

      {careers.length === 0 && !loading && (
        <div className="flat-card p-12 text-center text-secondary">
          No matches yet. Make sure your profile + skills are filled, then click <strong className="text-white">Regenerate</strong>.
        </div>
      )}

      {loading && (
        <div className="flat-card p-12 flex items-center gap-4">
          <div className="dot-loader"><span/><span/><span/></div>
          <div className="overline">CROSS-REFERENCING YOUR PROFILE WITH MARKET · ~20S</div>
        </div>
      )}

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {careers.map((c, i) => (
          <div key={i} className="flat-card hover-lift p-8">
            <div className="flex justify-between items-start">
              <div>
                <div className="overline">RANK #{i + 1}</div>
                <h3 className="font-display text-2xl font-extrabold mt-2">{c.name}</h3>
              </div>
              <div className="text-right">
                <div className="font-display text-3xl font-black text-accent">{c.match_score}%</div>
                <div className="overline">MATCH</div>
              </div>
            </div>
            <div className="h-1 bg-elevated mt-4 mb-6">
              <div className="h-full bg-accent-yellow" style={{ width: `${c.match_score}%` }} />
            </div>
            <p className="text-sm text-secondary mb-6">{c.description}</p>

            <div className="grid grid-cols-3 gap-3 mb-6">
              <div>
                <div className="overline">SALARY</div>
                <div className="text-xs mt-1 font-mono">{c.salary_range_inr}</div>
              </div>
              <div>
                <div className="overline">DEMAND</div>
                <div className="text-xs mt-1 font-mono">{c.demand_level}</div>
              </div>
              <div>
                <div className="overline">GROWTH</div>
                <div className="text-xs mt-1 font-mono">{c.growth_potential}</div>
              </div>
            </div>

            <div>
              <div className="overline mb-2">KEY SKILLS</div>
              <div className="flex flex-wrap gap-1.5">
                {(c.key_skills || []).slice(0, 6).map((k, j) => (
                  <span key={j} className="bg-elevated border border-default px-2 py-1 text-xs font-mono">{k}</span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
