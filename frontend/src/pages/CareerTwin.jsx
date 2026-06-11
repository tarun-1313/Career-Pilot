import React, { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Robot, Sparkle, Lightning, Quotes } from "@phosphor-icons/react";
import { toast } from "sonner";

export default function CareerTwin() {
  const [doc, setDoc] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  const load = async () => {
    setLoading(true);
    try { const r = await api.get("/career-twin"); setDoc(r.data); }
    finally { setLoading(false); }
  };

  const generate = async () => {
    setGenerating(true);
    try {
      const r = await api.post("/career-twin/brief");
      setDoc(r.data);
      toast.success("Weekly brief generated");
    } catch { toast.error("Could not generate brief"); }
    finally { setGenerating(false); }
  };

  useEffect(() => { load(); }, []);

  const b = doc?.brief;

  return (
    <div className="space-y-8" data-testid="twin-root">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <div className="overline mb-3 flex items-center gap-2">
            <Robot size={12} weight="fill" /> AI CAREER TWIN · WEEK OF {doc?.week_of || "—"}
          </div>
          <h1 className="font-display text-4xl lg:text-5xl font-black tracking-display">
            Your <span className="text-accent">persistent</span> agent.
          </h1>
          <p className="text-secondary mt-2">An always-on AI that watches the market and your growth — and tells you what to do next.</p>
        </div>
        <button onClick={generate} disabled={generating} className="btn-yellow" data-testid="twin-generate-button">
          <Sparkle size={16} weight="bold" /> {generating ? "Thinking..." : "Generate this week's brief"}
        </button>
      </div>

      {loading && <div className="flat-card p-12"><div className="dot-loader"><span/><span/><span/></div></div>}

      {!loading && !b && (
        <div className="flat-card p-12 text-center text-secondary">
          No brief yet. Click <strong className="text-white">Generate this week's brief</strong> to wake your Twin.
        </div>
      )}

      {b && (
        <>
          <div className="flat-card p-10">
            <div className="overline mb-3">GREETING</div>
            <p className="font-display text-2xl lg:text-3xl font-extrabold leading-snug">{b.greeting}</p>
          </div>

          <div className="grid lg:grid-cols-2 gap-6">
            <div className="flat-card p-8">
              <div className="overline mb-3 flex items-center gap-2"><Lightning size={12} weight="fill" /> THIS WEEK'S FOCUS</div>
              <p className="text-lg leading-relaxed">{b.this_week_focus}</p>
              <div className="overline mt-6 mb-2">RECOMMENDED ACTION</div>
              <p className="text-sm text-secondary">{b.recommended_action}</p>
            </div>

            <div className="flat-card p-8">
              <div className="overline mb-3">MARKET SIGNALS</div>
              <ul className="space-y-2 text-sm">
                {(b.market_signals || []).map((s, i) => <li key={i} className="border-l-2 border-[var(--accent)] pl-3 py-1">{s}</li>)}
              </ul>
            </div>

            <div className="flat-card p-8">
              <div className="overline mb-3">OPPORTUNITIES SPOTTED</div>
              <div className="space-y-3">
                {(b.opportunities || []).map((o, i) => (
                  <div key={i} className="border border-default p-4">
                    <div className="font-display font-extrabold">{o.title}</div>
                    <div className="text-xs text-secondary mt-1">{o.why_now}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="flat-card p-8">
              <div className="overline mb-3">SKILLS TO PRACTICE</div>
              <div className="flex flex-wrap gap-2">
                {(b.skills_to_practice || []).map((s, i) => (
                  <span key={i} className="bg-elevated border border-default px-3 py-1.5 text-xs font-mono">{s}</span>
                ))}
              </div>
            </div>
          </div>

          {b.motivation_quote && (
            <div className="flat-card p-10 text-center">
              <Quotes size={32} weight="fill" className="text-[var(--accent)] mx-auto mb-4" />
              <p className="font-display text-2xl lg:text-3xl font-extrabold leading-snug max-w-3xl mx-auto">
                {b.motivation_quote}
              </p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
