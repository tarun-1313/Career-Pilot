import React, { useEffect, useState } from "react";
import { getTrends, predictSalary } from "@/lib/api";
import { TrendUp, CurrencyInr } from "@phosphor-icons/react";
import {
  BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip, Cell,
} from "recharts";

const TooltipBox = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-surface border border-default px-3 py-2 text-xs font-mono">
      <div className="text-accent">{payload[0].payload.name || payload[0].payload.role}</div>
      <div>{payload[0].value}</div>
    </div>
  );
};

export default function Trends() {
  const [data, setData] = useState(null);
  const [loadingTrends, setLoadingTrends] = useState(true);
  const [salary, setSalary] = useState(null);
  const [role, setRole] = useState("AI Engineer");
  const [exp, setExp] = useState(2);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    getTrends().then((d) => { setData(d); setLoadingTrends(false); }).catch(() => setLoadingTrends(false));
  }, []);

  const runSalary = async () => {
    setBusy(true);
    try { setSalary(await predictSalary({ role, experience_years: Number(exp), location: "India", skills: [] })); }
    finally { setBusy(false); }
  };

  return (
    <div className="space-y-10" data-testid="trends-root">
      <div>
        <div className="overline mb-3">INDUSTRY TRENDS · 2026</div>
        <h1 className="font-display text-4xl lg:text-5xl font-black tracking-display">
          Where the <span className="text-accent">market</span> is going.
        </h1>
      </div>

      {loadingTrends && (
        <div className="flat-card p-12 flex items-center gap-4">
          <div className="dot-loader"><span/><span/><span/></div>
          <div className="overline">FETCHING LIVE MARKET SIGNALS · ~15S</div>
        </div>
      )}

      {data && (
        <>
          <div className="grid lg:grid-cols-2 gap-6">
            <div className="flat-card p-8">
              <div className="overline mb-4">TRENDING TECH (MOMENTUM)</div>
              <div style={{ width: "100%", height: 320 }}>
                <ResponsiveContainer>
                  <BarChart data={data.trending_tech || []} layout="vertical" margin={{ left: 20 }}>
                    <XAxis type="number" stroke="#71717a" fontSize={11} />
                    <YAxis type="category" dataKey="name" stroke="#a1a1aa" fontSize={11} width={160}
                           tick={{ fill: "#a1a1aa" }} interval={0} />
                    <Tooltip content={<TooltipBox />} cursor={{ fill: "rgba(255,255,255,0.04)" }} />
                    <Bar dataKey="momentum">
                      {(data.trending_tech || []).map((_, i) => (
                        <Cell key={i} fill="#E6FF00" />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="flat-card p-8">
              <div className="overline mb-4">HIGH DEMAND ROLES</div>
              <div className="space-y-3">
                {(data.high_demand_roles || []).map((r, i) => (
                  <div key={i} className="border-l-2 border-[var(--accent)] pl-4">
                    <div className="flex justify-between">
                      <div className="font-display font-extrabold">{r.role}</div>
                      <div className="font-mono text-accent text-sm">{r.demand}%</div>
                    </div>
                    <div className="text-xs text-secondary mt-1">Growth · {r.growth}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="flat-card p-8">
              <div className="overline mb-4">SALARY SHIFTS</div>
              <div className="space-y-2">
                {(data.salary_shifts || []).map((s, i) => (
                  <div key={i} className="flex justify-between items-center text-sm border-b border-default py-2 last:border-0">
                    <span>{s.role}</span>
                    <span className={`font-mono ${s.change_pct >= 0 ? "text-accent" : "text-red-400"}`}>
                      {s.change_pct >= 0 ? "+" : ""}{s.change_pct}%
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="flat-card p-8">
              <div className="overline mb-4">AI FOCUS AREAS</div>
              <div className="flex flex-wrap gap-2">
                {(data.ai_focus_areas || []).map((a, i) => (
                  <span key={i} className="bg-elevated border border-default px-3 py-1.5 text-xs font-mono">{a}</span>
                ))}
              </div>
            </div>
          </div>

          <div className="flat-card p-8">
            <div className="overline mb-4 flex items-center gap-2"><CurrencyInr size={12} weight="bold" /> SALARY PREDICTOR</div>
            <div className="grid md:grid-cols-3 gap-3 mb-4">
              <input value={role} onChange={(e) => setRole(e.target.value)} placeholder="Role" className="bg-elevated border border-default px-3 py-2.5 text-sm outline-none focus:border-[var(--accent)]" data-testid="salary-role-input"/>
              <input type="number" value={exp} onChange={(e) => setExp(e.target.value)} placeholder="Years" className="bg-elevated border border-default px-3 py-2.5 text-sm outline-none focus:border-[var(--accent)]" data-testid="salary-exp-input"/>
              <button onClick={runSalary} disabled={busy} className="btn-yellow" data-testid="salary-predict-button">
                <TrendUp size={16} weight="bold" /> {busy ? "Predicting..." : "Predict"}
              </button>
            </div>
            {salary && (
              <div className="grid md:grid-cols-3 gap-4">
                {[
                  ["INDIA", salary.india_range_inr],
                  ["REMOTE (USD)", salary.remote_range_usd],
                  ["INTERNATIONAL (USD)", salary.international_range_usd],
                ].map(([k, v]) => (
                  <div key={k} className="border border-default p-5">
                    <div className="overline">{k}</div>
                    <div className="font-display text-2xl font-black mt-2">{v}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}
