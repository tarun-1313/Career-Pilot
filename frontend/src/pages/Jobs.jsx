import React, { useState } from "react";
import { searchJobs } from "@/lib/api";
import { toast } from "sonner";
import { MagnifyingGlass, MapPin, Briefcase, ArrowUpRight } from "@phosphor-icons/react";

export default function Jobs() {
  const [q, setQ] = useState("AI Engineer");
  const [loc, setLoc] = useState("India");
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    setLoading(true);
    try { setItems((await searchJobs(q, loc)).results || []); }
    catch { toast.error("Search failed"); }
    finally { setLoading(false); }
  };

  return (
    <div className="space-y-8" data-testid="jobs-root">
      <div>
        <div className="overline mb-3">LIVE JOBS</div>
        <h1 className="font-display text-4xl lg:text-5xl font-black tracking-display">
          Jobs that <span className="text-accent">match you</span>.
        </h1>
        <p className="text-secondary mt-2">Real-time feed from JSearch / Adzuna with personalized match scores.</p>
      </div>

      <div className="flat-card p-6 grid md:grid-cols-3 gap-3">
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Role" className="bg-elevated border border-default px-3 py-2.5 text-sm outline-none focus:border-[var(--accent)]" data-testid="jobs-role-input" />
        <input value={loc} onChange={(e) => setLoc(e.target.value)} placeholder="Location" className="bg-elevated border border-default px-3 py-2.5 text-sm outline-none focus:border-[var(--accent)]" data-testid="jobs-location-input" />
        <button onClick={run} disabled={loading} className="btn-yellow" data-testid="jobs-search-button">
          <MagnifyingGlass size={16} weight="bold" /> {loading ? "Searching..." : "Find jobs"}
        </button>
      </div>

      <div className="space-y-4">
        {items.map((j) => (
          <a key={j.id || j.url} href={j.url} target="_blank" rel="noreferrer"
             className="flat-card hover-lift p-6 flex flex-col md:flex-row md:items-center gap-6 group">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-3 mb-2">
                <span className="overline">{j.remote ? "REMOTE" : "ONSITE"}</span>
                <span className="text-muted text-xs font-mono">·</span>
                <span className="overline">{j.company}</span>
              </div>
              <h3 className="font-display text-xl font-extrabold group-hover:text-accent transition-colors">{j.title}</h3>
              <div className="flex flex-wrap gap-4 mt-3 text-xs text-secondary font-mono">
                <span className="flex items-center gap-1"><MapPin size={12} /> {j.location}</span>
                <span className="flex items-center gap-1"><Briefcase size={12} /> {j.salary}</span>
              </div>
              <p className="text-sm text-secondary mt-3 line-clamp-2">{j.description}</p>
            </div>
            <div className="text-right md:w-40 shrink-0">
              <div className="font-display text-4xl font-black text-accent">{j.match_score}%</div>
              <div className="overline">MATCH</div>
              <div className="mt-4 flex items-center justify-end gap-1 text-xs font-mono">
                APPLY <ArrowUpRight size={12} />
              </div>
            </div>
          </a>
        ))}
        {items.length === 0 && !loading && (
          <div className="text-center text-secondary py-12">Click <strong className="text-white">Find jobs</strong> to load real-time matches.</div>
        )}
      </div>
    </div>
  );
}
