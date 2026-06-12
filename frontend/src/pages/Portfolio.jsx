import React, { useState } from "react";
import { analyzePortfolio } from "@/lib/api";
import { toast } from "sonner";
import { GithubLogo, Star, GitFork, MagnifyingGlass } from "@phosphor-icons/react";

export default function Portfolio() {
  const [url, setUrl] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    if (!url) return;
    setLoading(true);
    try { setData(await analyzePortfolio(url)); toast.success("Portfolio analyzed"); }
    catch (e) { toast.error(e?.response?.data?.detail || "Analysis failed"); }
    finally { setLoading(false); }
  };

  return (
    <div className="space-y-8" data-testid="portfolio-root">
      <div>
        <div className="overline mb-3">PORTFOLIO ANALYZER</div>
        <h1 className="font-display text-4xl lg:text-5xl font-black tracking-display">
          Your GitHub, <span className="text-accent">reviewed</span>.
        </h1>
        <p className="text-secondary mt-2">Real repos. Real critique. Ship better READMEs.</p>
      </div>

      <div className="flat-card p-6 flex flex-col md:flex-row gap-3">
        <input value={url} onChange={(e) => setUrl(e.target.value)}
          placeholder="https://github.com/yourname"
          className="flex-1 bg-elevated border border-default px-3 py-2.5 text-sm outline-none focus:border-[var(--accent)]"
          data-testid="portfolio-url-input"/>
        <button onClick={run} disabled={loading} className="btn-yellow" data-testid="portfolio-analyze-button">
          <MagnifyingGlass size={16} weight="bold" /> {loading ? "Auditing..." : "Audit"}
        </button>
      </div>

      {data && (
        <>
          <div className="flat-card p-8 flex flex-col md:flex-row items-start md:items-center gap-6">
            <img src={data.avatar} alt="" className="w-20 h-20" />
            <div className="flex-1">
              <div className="overline">{data.username}</div>
              <h2 className="font-display text-3xl font-extrabold">{data.name}</h2>
              <p className="text-sm text-secondary mt-1">{data.bio}</p>
              <div className="flex gap-6 mt-3 text-xs font-mono text-muted">
                <span>{data.public_repos} repos</span>
                <span>{data.followers} followers</span>
              </div>
            </div>
            <div className="text-right">
              <div className="font-display text-5xl font-black text-accent">{data.analysis?.score || "—"}</div>
              <div className="overline">PORTFOLIO SCORE</div>
            </div>
          </div>

          <div className="flat-card p-8">
            <div className="overline mb-3">AI SUMMARY</div>
            <p className="text-sm leading-relaxed">{data.analysis?.summary}</p>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="flat-card p-8">
              <div className="overline mb-3">STRENGTHS</div>
              <ul className="space-y-1 text-sm">
                {(data.analysis?.strengths || []).map((s, i) => <li key={i} className="text-secondary">• {s}</li>)}
              </ul>
            </div>
            <div className="flat-card p-8">
              <div className="overline mb-3">IMPROVEMENTS</div>
              <ul className="space-y-1 text-sm">
                {(data.analysis?.improvements || []).map((s, i) => <li key={i} className="text-secondary">• {s}</li>)}
              </ul>
            </div>
          </div>

          <div>
            <div className="overline mb-4">REPOSITORIES</div>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {(data.repos || []).map((r, i) => (
                <a key={i} href={r.url} target="_blank" rel="noreferrer" className="flat-card hover-lift p-5">
                  <div className="flex items-center gap-2 overline">
                    <GithubLogo size={12} /> {r.language || "—"}
                  </div>
                  <div className="font-display text-base font-extrabold mt-2 truncate">{r.name}</div>
                  <div className="text-xs text-secondary mt-1 line-clamp-2">{r.description || "—"}</div>
                  <div className="flex gap-4 mt-3 text-xs font-mono text-muted">
                    <span className="flex items-center gap-1"><Star size={12} /> {r.stars}</span>
                    <span className="flex items-center gap-1"><GitFork size={12} /> {r.forks}</span>
                  </div>
                </a>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
