import React, { useEffect, useState } from "react";
import { api, API } from "@/lib/api";
import { toast } from "sonner";
import { Share, Globe, Copy, ArrowSquareOut } from "@phosphor-icons/react";

export default function ShareProfile() {
  const [profile, setProfile] = useState({ slug: "", headline: "", bio: "", show_portfolio: true, show_resume: false });
  const [saved, setSaved] = useState(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    api.get("/public-profile/me").then((r) => {
      if (r.data?.slug) { setProfile({ ...profile, ...r.data }); setSaved(r.data); }
    }).catch(() => {});
    // eslint-disable-next-line
  }, []);

  const publish = async () => {
    setSaving(true);
    try {
      const r = await api.post("/public-profile/publish", profile);
      setSaved(r.data);
      toast.success("Public profile published");
    } catch (e) { toast.error(e?.response?.data?.detail || "Could not publish"); }
    finally { setSaving(false); }
  };

  const publicUrl = saved?.slug ? `${window.location.origin}/u/${saved.slug}` : "";

  return (
    <div className="space-y-8" data-testid="share-root">
      <div>
        <div className="overline mb-3 flex items-center gap-2"><Globe size={12} weight="fill" /> SHAREABLE CAREER PAGE</div>
        <h1 className="font-display text-4xl lg:text-5xl font-black tracking-display">
          Your <span className="text-accent">public</span> career page.
        </h1>
        <p className="text-secondary mt-2">A live link recruiters can share. Built from your profile, GitHub, and AI-matched careers.</p>
      </div>

      <div className="flat-card p-8 space-y-5 max-w-3xl">
        <div>
          <div className="overline mb-2">PUBLIC SLUG</div>
          <div className="flex items-center gap-2 font-mono text-sm">
            <span className="text-muted">{window.location.host}/u/</span>
            <input
              value={profile.slug}
              onChange={(e) => setProfile({ ...profile, slug: e.target.value })}
              placeholder="your-name"
              className="flex-1 bg-elevated border border-default px-3 py-2.5 text-sm outline-none focus:border-[var(--accent)]"
              data-testid="share-slug-input"
            />
          </div>
        </div>
        <div>
          <div className="overline mb-2">HEADLINE</div>
          <input value={profile.headline || ""} onChange={(e) => setProfile({ ...profile, headline: e.target.value })}
            placeholder="AI Engineer · LangGraph · LLMs"
            className="w-full bg-elevated border border-default px-3 py-2.5 text-sm outline-none focus:border-[var(--accent)]"
            data-testid="share-headline-input"/>
        </div>
        <div>
          <div className="overline mb-2">BIO</div>
          <textarea value={profile.bio || ""} onChange={(e) => setProfile({ ...profile, bio: e.target.value })} rows={3}
            placeholder="One short paragraph about what you build and where you're heading."
            className="w-full bg-elevated border border-default p-3 text-sm outline-none focus:border-[var(--accent)]"
            data-testid="share-bio-input"/>
        </div>
        <div className="flex gap-3">
          <button onClick={() => setProfile({ ...profile, show_portfolio: !profile.show_portfolio })}
            className={`px-3 py-2 text-xs border ${profile.show_portfolio ? "border-[var(--accent)] text-accent bg-elevated" : "border-default text-secondary"}`}
            data-testid="share-toggle-portfolio">
            {profile.show_portfolio ? "Showing GitHub" : "Hiding GitHub"}
          </button>
        </div>
        <button onClick={publish} disabled={saving || !profile.slug} className="btn-yellow" data-testid="share-publish-button">
          <Share size={16} weight="bold" /> {saving ? "Publishing..." : "Publish public page"}
        </button>
      </div>

      {publicUrl && (
        <div className="flat-card p-8 max-w-3xl">
          <div className="overline mb-3">YOUR LIVE URL</div>
          <div className="flex items-center justify-between gap-3 bg-elevated border border-default px-3 py-3">
            <span className="font-mono text-sm truncate">{publicUrl}</span>
            <div className="flex gap-2 shrink-0">
              <button onClick={() => { navigator.clipboard.writeText(publicUrl); toast.success("Copied"); }}
                className="btn-ghost text-xs" data-testid="share-copy-button">
                <Copy size={14} /> Copy
              </button>
              <a href={publicUrl} target="_blank" rel="noreferrer" className="btn-yellow text-xs" data-testid="share-open-button">
                <ArrowSquareOut size={14} weight="bold" /> Open
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
