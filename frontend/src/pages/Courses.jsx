import React, { useState } from "react";
import { searchCourses } from "@/lib/api";
import { toast } from "sonner";
import { MagnifyingGlass, Play } from "@phosphor-icons/react";

export default function Courses() {
  const [q, setQ] = useState("LangGraph multi-agent");
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    setLoading(true);
    try {
      const r = await searchCourses(q);
      setItems(r.results || []);
    } catch { toast.error("Search failed"); }
    finally { setLoading(false); }
  };

  return (
    <div className="space-y-8" data-testid="courses-root">
      <div>
        <div className="overline mb-3">COURSES & RESOURCES</div>
        <h1 className="font-display text-4xl lg:text-5xl font-black tracking-display">
          Curated <span className="text-accent">learning</span>, on-demand.
        </h1>
        <p className="text-secondary mt-2">Pulled live from YouTube — ranked by relevance.</p>
      </div>

      <div className="flat-card p-6 flex flex-col md:flex-row gap-3">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && run()}
          placeholder="Search a topic, e.g. LangChain RAG"
          className="flex-1 bg-elevated border border-default px-3 py-2.5 text-sm outline-none focus:border-[var(--accent)]"
          data-testid="courses-search-input"
        />
        <button onClick={run} disabled={loading} className="btn-yellow" data-testid="courses-search-button">
          <MagnifyingGlass size={16} weight="bold" /> {loading ? "Searching..." : "Search"}
        </button>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {items.map((c) => (
          <a key={c.id} href={c.url} target="_blank" rel="noreferrer" className="flat-card hover-lift block overflow-hidden">
            <div className="relative">
              <img src={c.thumbnail} alt="" className="w-full aspect-video object-cover" />
              <div className="absolute inset-0 bg-black/30 opacity-0 hover:opacity-100 transition-opacity flex items-center justify-center">
                <Play size={36} weight="fill" className="text-[var(--accent)]" />
              </div>
            </div>
            <div className="p-5">
              <div className="overline">{c.provider} · {c.channel}</div>
              <div className="font-display text-base font-extrabold mt-2 line-clamp-2">{c.title}</div>
              <div className="text-xs text-secondary mt-2 line-clamp-2">{c.description}</div>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}
