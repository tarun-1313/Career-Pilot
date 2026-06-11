import React, { useEffect, useState } from "react";
import { uploadResume, getLatestResume, downloadRewrittenResume } from "@/lib/api";
import { toast } from "sonner";
import { CloudArrowUp, FileText, CheckCircle, Warning, DownloadSimple, Sparkle } from "@phosphor-icons/react";

export default function Resume() {
  const [doc, setDoc] = useState(null);
  const [loading, setLoading] = useState(false);
  const [rewriting, setRewriting] = useState(false);

  useEffect(() => { getLatestResume().then(setDoc).catch(() => {}); }, []);

  const onUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setLoading(true);
    try {
      const res = await uploadResume(file);
      setDoc(res);
      toast.success(`ATS score: ${res.ats_score}/100`);
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Upload failed");
    } finally { setLoading(false); }
  };

  const rewrite = async () => {
    setRewriting(true);
    try {
      await downloadRewrittenResume();
      toast.success("ATS-optimized resume downloaded");
    } catch { toast.error("Rewrite failed"); }
    finally { setRewriting(false); }
  };

  const parsed = doc?.parsed || {};

  return (
    <div className="space-y-8" data-testid="resume-root">
      <div>
        <div className="overline mb-3">RESUME ANALYZER</div>
        <h1 className="font-display text-4xl lg:text-5xl font-black tracking-display">
          ATS-grade resume <span className="text-accent">in 10 seconds</span>.
        </h1>
        <p className="text-secondary mt-2">Drop your PDF or DOCX. We score it, extract everything, and tell you what to fix.</p>
      </div>

      <label className="flat-card p-12 border-dashed flex flex-col items-center justify-center text-center cursor-pointer hover:border-[var(--accent)] transition-colors" data-testid="resume-upload-area">
        <CloudArrowUp size={48} weight="duotone" className="text-[var(--accent)] mb-4" />
        <div className="font-display text-xl font-extrabold">
          {loading ? "Analyzing..." : "Drop your resume here"}
        </div>
        <div className="text-secondary text-sm mt-1">PDF or DOCX · max 5 MB</div>
        <input type="file" accept=".pdf,.docx" className="hidden" onChange={onUpload} data-testid="resume-file-input" />
      </label>

      {doc && doc.parsed && (
        <div className="grid lg:grid-cols-3 gap-6">
          <div className="flat-card p-8 lg:col-span-1">
            <div className="overline">ATS SCORE</div>
            <div className="font-display text-7xl font-black tracking-display mt-3 text-accent">
              {doc.ats_score}
            </div>
            <div className="text-xs text-muted font-mono">/ 100</div>
            <div className="mt-6 h-2 bg-elevated">
              <div className="h-full bg-accent-yellow" style={{ width: `${doc.ats_score}%` }} />
            </div>
            <div className="overline mt-6">FILE</div>
            <div className="text-sm mt-1 flex items-center gap-2"><FileText size={14} /> {doc.filename}</div>
          </div>

          <div className="flat-card p-8 lg:col-span-2 space-y-6">
            <div>
              <div className="overline mb-3 flex items-center gap-2"><CheckCircle size={12} className="text-[var(--accent)]" /> STRENGTHS</div>
              <ul className="space-y-2 text-sm">
                {(parsed.strengths || []).map((s, i) => <li key={i} className="text-secondary">• {s}</li>)}
              </ul>
            </div>
            <div>
              <div className="overline mb-3 flex items-center gap-2"><Warning size={12} className="text-[var(--accent)]" /> IMPROVEMENTS</div>
              <ul className="space-y-2 text-sm">
                {(parsed.improvements || []).map((s, i) => <li key={i} className="text-secondary">• {s}</li>)}
              </ul>
            </div>
          </div>

          <div className="flat-card p-8 lg:col-span-3">
            <div className="overline mb-4">EXTRACTED SKILLS</div>
            <div className="flex flex-wrap gap-2">
              {(parsed.skills || []).map((s, i) => (
                <span key={i} className="bg-elevated border border-default px-3 py-1.5 text-xs font-mono">{s}</span>
              ))}
            </div>
            {parsed.missing_keywords?.length > 0 && (
              <>
                <div className="overline mt-8 mb-4">MISSING KEYWORDS (ATS)</div>
                <div className="flex flex-wrap gap-2">
                  {parsed.missing_keywords.map((s, i) => (
                    <span key={i} className="border border-[var(--accent)] text-accent px-3 py-1.5 text-xs font-mono">{s}</span>
                  ))}
                </div>
              </>
            )}
          </div>

          <div className="flat-card p-8 lg:col-span-3">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <div className="overline mb-2 flex items-center gap-2"><Sparkle size={12} weight="fill" /> AI RESUME REWRITER</div>
                <h3 className="font-display text-xl font-extrabold">Download an ATS-optimized .docx</h3>
                <p className="text-sm text-secondary mt-1">We integrate the missing keywords, strengthen verbs, and quantify achievements — truthfully.</p>
              </div>
              <button onClick={rewrite} disabled={rewriting} className="btn-yellow" data-testid="resume-rewrite-button">
                <DownloadSimple size={16} weight="bold" /> {rewriting ? "Rewriting..." : "Generate & Download"}
              </button>
            </div>
          </div>

          {parsed.experience?.length > 0 && (
            <div className="flat-card p-8 lg:col-span-3">
              <div className="overline mb-4">EXPERIENCE</div>
              <div className="space-y-4">
                {parsed.experience.map((e, i) => (
                  <div key={i} className="border-l-2 border-[var(--accent)] pl-4">
                    <div className="font-display text-lg font-extrabold">{e.role}</div>
                    <div className="text-sm text-secondary">{e.company} · {e.duration}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
