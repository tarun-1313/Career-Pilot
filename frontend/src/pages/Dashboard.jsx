import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getProgress, getLatestResume, listCareers, getRoadmap } from "@/lib/api";
import {
  Compass, FileText, Path, ChartBar, Briefcase, ArrowRight, Sparkle,
} from "@phosphor-icons/react";
import { useAuth } from "@/context/AuthContext";

const Stat = ({ label, value, suffix }) => (
  <div className="flat-card p-6">
    <div className="overline">{label}</div>
    <div className="font-display text-4xl font-black tracking-display mt-2">
      {value}<span className="text-secondary text-2xl">{suffix}</span>
    </div>
  </div>
);

const QuickLink = ({ to, icon: Icon, title, desc, testid }) => (
  <Link to={to} data-testid={testid} className="flat-card hover-lift p-6 group">
    <Icon size={22} weight="duotone" className="text-[var(--accent)] mb-4" />
    <div className="font-display text-lg font-extrabold">{title}</div>
    <div className="text-sm text-secondary mt-1">{desc}</div>
    <div className="mt-4 flex items-center gap-1 text-xs font-mono text-secondary group-hover:text-white">
      OPEN <ArrowRight size={12} />
    </div>
  </Link>
);

export default function Dashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [resume, setResume] = useState(null);
  const [careers, setCareers] = useState([]);
  const [roadmap, setRoadmap] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const [p, r, c, rm] = await Promise.all([
          getProgress(), getLatestResume(), listCareers(), getRoadmap(),
        ]);
        setStats(p); setResume(r); setCareers(c.careers || []); setRoadmap(rm);
      } catch (e) { console.error(e); }
    })();
  }, []);

  return (
    <div className="space-y-10" data-testid="dashboard-root">
      {/* hero */}
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-4">
        <div>
          <div className="overline mb-3 flex items-center gap-2">
            <Sparkle size={12} weight="fill" /> DASHBOARD
          </div>
          <h1 className="font-display text-4xl lg:text-5xl font-black tracking-display">
            Welcome back, <span className="text-accent">{(user?.name || "").split(" ")[0]}</span>.
          </h1>
          <p className="text-secondary mt-2">Here's your career console — live and shipping.</p>
        </div>
        <Link to="/careers" className="btn-yellow text-sm" data-testid="dashboard-generate">
          <Compass size={16} weight="bold" /> Generate Recommendations
        </Link>
      </div>

      {/* stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Stat label="ATS SCORE" value={stats?.ats_score ?? 0} suffix="/100" />
        <Stat label="ROADMAP DONE" value={stats?.roadmap_percent ?? 0} suffix="%" />
        <Stat label="INTERVIEWS" value={stats?.interviews_taken ?? 0} />
        <Stat label="SKILLS TRACKED" value={stats?.skills_count ?? 0} />
      </div>

      {/* quick links */}
      <div>
        <div className="overline mb-4">JUMP IN</div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <QuickLink to="/resume" icon={FileText} title="Upload Resume" desc="Get ATS score + AI rewrite tips" testid="ql-resume" />
          <QuickLink to="/careers" icon={Compass} title="Career Paths" desc="AI-matched top 5 careers" testid="ql-careers" />
          <QuickLink to="/skills" icon={ChartBar} title="Skill Gap" desc="What you're missing, prioritized" testid="ql-skills" />
          <QuickLink to="/roadmap" icon={Path} title="Roadmap" desc="Month-by-month plan" testid="ql-roadmap" />
        </div>
      </div>

      {/* career snapshot */}
      <div className="grid lg:grid-cols-2 gap-6">
        <div className="flat-card p-8">
          <div className="overline mb-4">TOP CAREER MATCHES</div>
          {careers.length === 0 ? (
            <div className="text-secondary text-sm">
              No recommendations yet.{" "}
              <Link to="/careers" className="text-accent">Generate now →</Link>
            </div>
          ) : (
            <div className="space-y-4">
              {careers.slice(0, 4).map((c, i) => (
                <div key={i}>
                  <div className="flex justify-between mb-1 text-sm">
                    <span>{c.name}</span>
                    <span className="font-mono text-accent">{c.match_score}%</span>
                  </div>
                  <div className="h-1 bg-elevated">
                    <div className="h-full bg-accent-yellow" style={{ width: `${c.match_score}%` }} />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="flat-card p-8">
          <div className="overline mb-4">CURRENT ROADMAP</div>
          {!roadmap?.data?.months ? (
            <div className="text-secondary text-sm">
              No roadmap yet.{" "}
              <Link to="/roadmap" className="text-accent">Create one →</Link>
            </div>
          ) : (
            <div>
              <div className="font-display text-2xl font-extrabold mb-3">
                {roadmap.target_role}
              </div>
              <div className="space-y-2">
                {(roadmap.data.months || []).slice(0, 3).map((m, i) => (
                  <div key={i} className="border-l-2 border-default pl-4 py-1">
                    <div className="overline">MONTH {m.month}</div>
                    <div className="text-sm">{m.title}</div>
                  </div>
                ))}
              </div>
              <Link to="/roadmap" className="btn-ghost text-xs mt-6" data-testid="dashboard-view-roadmap">
                View full roadmap <ArrowRight size={12} />
              </Link>
            </div>
          )}
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <QuickLink to="/jobs" icon={Briefcase} title="Live Jobs Feed" desc="Personalized matches across India + remote" testid="ql-jobs" />
        <QuickLink to="/interview" icon={Compass} title="Run a Mock Interview" desc="Technical · HR · Behavioural" testid="ql-interview" />
      </div>
    </div>
  );
}
