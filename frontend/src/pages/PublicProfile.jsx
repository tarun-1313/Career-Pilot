import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "@/lib/api";
import { GithubLogo, ArrowUpRight, MapPin } from "@phosphor-icons/react";

export default function PublicProfile() {
  const { slug } = useParams();
  const [doc, setDoc] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    api.get(`/public/${slug}`).then((r) => setDoc(r.data)).catch((e) => setErr(e?.response?.data?.detail || "Not found"));
  }, [slug]);

  if (err) return (
    <div className="min-h-screen bg-base flex items-center justify-center text-center">
      <div>
        <div className="overline mb-3">404</div>
        <h1 className="font-display text-4xl font-black">Profile not found</h1>
        <Link to="/" className="overline mt-6 inline-block text-accent">← back home</Link>
      </div>
    </div>
  );
  if (!doc) return <div className="min-h-screen bg-base flex items-center justify-center"><div className="dot-loader"><span/><span/><span/></div></div>;

  return (
    <div className="min-h-screen bg-base text-white">
      <header className="glass-header sticky top-0 z-30 py-4">
        <div className="max-w-5xl mx-auto px-6 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <span className="block w-3 h-3 bg-accent-yellow"></span>
            <span className="font-display text-lg font-extrabold tracking-display">CareerPilot AI</span>
          </Link>
          <div className="overline">@{doc.slug}</div>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-6 py-12 lg:py-16 space-y-10">
        {/* hero */}
        <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
          {doc.picture && <img src={doc.picture} alt="" className="w-24 h-24 object-cover" />}
          <div>
            <h1 className="font-display text-5xl lg:text-6xl font-black tracking-display">{doc.name}</h1>
            {doc.headline && <div className="text-lg text-secondary mt-2">{doc.headline}</div>}
          </div>
        </div>

        {doc.bio && (
          <div className="flat-card p-8">
            <p className="text-lg leading-relaxed">{doc.bio}</p>
          </div>
        )}

        {/* skills */}
        {doc.skills?.length > 0 && (
          <div className="flat-card p-8">
            <div className="overline mb-4">SKILLS</div>
            <div className="flex flex-wrap gap-2">
              {doc.skills.map((s, i) => (
                <span key={i} className="bg-elevated border border-default px-3 py-1.5 text-xs font-mono">{s}</span>
              ))}
            </div>
          </div>
        )}

        {/* careers */}
        {doc.top_careers?.length > 0 && (
          <div className="flat-card p-8">
            <div className="overline mb-4">AI-MATCHED CAREER DIRECTIONS</div>
            <div className="space-y-3">
              {doc.top_careers.map((c, i) => (
                <div key={i}>
                  <div className="flex justify-between text-sm">
                    <span>{c.name}</span>
                    <span className="font-mono text-accent">{c.match}%</span>
                  </div>
                  <div className="h-1 bg-elevated mt-1"><div className="h-full bg-accent-yellow" style={{ width: `${c.match}%` }} /></div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* portfolio */}
        {doc.portfolio?.repos?.length > 0 && (
          <div className="flat-card p-8">
            <div className="flex items-center justify-between mb-4">
              <div className="overline">GITHUB · {doc.portfolio.score ? `SCORE ${doc.portfolio.score}` : ""}</div>
              {doc.github_url && (
                <a href={doc.github_url} target="_blank" rel="noreferrer" className="overline text-accent flex items-center gap-1">
                  OPEN <ArrowUpRight size={12} />
                </a>
              )}
            </div>
            <div className="grid md:grid-cols-2 gap-3">
              {doc.portfolio.repos.map((r, i) => (
                <a key={i} href={r.url} target="_blank" rel="noreferrer" className="flat-card p-5 hover-lift">
                  <div className="overline"><GithubLogo size={10} className="inline mr-1" /> {r.language || "—"}</div>
                  <div className="font-display font-extrabold mt-2">{r.name}</div>
                  <div className="text-xs text-secondary mt-1 line-clamp-2">{r.description}</div>
                </a>
              ))}
            </div>
          </div>
        )}

        <footer className="text-center pt-8 border-t border-default">
          <div className="overline">CRAFTED WITH CAREERPILOT AI</div>
          <Link to="/" className="text-xs text-accent mt-2 inline-block">Build your own →</Link>
        </footer>
      </div>
    </div>
  );
}
