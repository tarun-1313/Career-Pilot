import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion, useMotionValue, useTransform, animate } from "framer-motion";
import {
  ArrowUpRight, Sparkle, Lightning, Brain, ChartLineUp, Target,
  RocketLaunch, Compass, GithubLogo, ChatCircleDots, CircleNotch,
  Microphone, Robot, GraduationCap, Briefcase, Cpu, ShieldCheck, FlowArrow,
  WaveSawtooth, Play, CheckCircle, ArrowRight,
} from "@phosphor-icons/react";

/* ============ Animated counter ============ */
const Counter = ({ to, suffix = "", duration = 1.4 }) => {
  const mv = useMotionValue(0);
  const rounded = useTransform(mv, (v) => Math.floor(v));
  const [n, setN] = useState(0);
  useEffect(() => {
    const c = animate(mv, to, { duration, ease: "easeOut" });
    const u = rounded.on("change", setN);
    return () => { c.stop(); u(); };
    // eslint-disable-next-line
  }, [to]);
  return <span>{n}{suffix}</span>;
};

/* ============ Floating notification card ============ */
const FloatNote = ({ icon: Icon, label, value, delay = 0, x, y }) => (
  <motion.div
    initial={{ opacity: 0, y: 20, scale: 0.9 }}
    animate={{ opacity: 1, y: 0, scale: 1 }}
    transition={{ duration: 0.8, delay, ease: [0.16, 1, 0.3, 1] }}
    style={{ left: x, top: y }}
    className="absolute hidden lg:flex items-center gap-3 backdrop-blur-xl bg-white/[0.04] border border-white/[0.08] px-4 py-3 z-30 shadow-2xl"
  >
    <div className="w-9 h-9 bg-[var(--accent)]/10 border border-[var(--accent)]/30 flex items-center justify-center">
      <Icon size={16} weight="duotone" className="text-[var(--accent)]" />
    </div>
    <div>
      <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">{label}</div>
      <div className="text-sm font-medium text-white whitespace-nowrap">{value}</div>
    </div>
    <span className="block w-1.5 h-1.5 rounded-full bg-[var(--accent)] animate-pulse" />
  </motion.div>
);

/* ============ Right-side AI dashboard mockup ============ */
const DashboardMock = () => (
  <div className="relative">
    {/* glow */}
    <div className="absolute -inset-8 bg-gradient-to-br from-[#D7FF00]/10 via-blue-500/5 to-transparent blur-3xl pointer-events-none" />

    <motion.div
      initial={{ opacity: 0, y: 40, rotateY: -8 }}
      animate={{ opacity: 1, y: 0, rotateY: 0 }}
      transition={{ duration: 0.9, ease: [0.16, 1, 0.3, 1], delay: 0.2 }}
      className="relative backdrop-blur-2xl bg-zinc-950/70 border border-white/[0.07]"
      style={{ perspective: "1000px" }}
    >
      {/* dashboard header */}
      <div className="flex items-center justify-between px-5 py-3 border-b border-white/[0.06]">
        <div className="flex items-center gap-2">
          <span className="block w-2.5 h-2.5 rounded-full bg-red-500/70" />
          <span className="block w-2.5 h-2.5 rounded-full bg-amber-500/70" />
          <span className="block w-2.5 h-2.5 rounded-full bg-[var(--accent)]/70" />
        </div>
        <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 flex items-center gap-2">
          <span className="block w-1.5 h-1.5 rounded-full bg-[var(--accent)] animate-pulse" />
          CAREERPILOT AI · LIVE SYSTEM
        </div>
        <div className="w-12" />
      </div>

      <div className="p-5 space-y-4">
        {/* AI match */}
        <div className="border border-white/[0.06] p-4">
          <div className="flex items-center justify-between mb-3">
            <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">AI CAREER MATCH</div>
            <Brain size={14} weight="duotone" className="text-[var(--accent)]" />
          </div>
          <div className="space-y-2.5">
            {[
              ["AI Engineer", 96],
              ["ML Engineer", 92],
              ["NLP Engineer", 88],
            ].map(([role, score], i) => (
              <div key={role}>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-zinc-300">{role}</span>
                  <span className="font-mono text-[var(--accent)]">{score}%</span>
                </div>
                <div className="h-[2px] bg-white/[0.04] overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${score}%` }}
                    transition={{ duration: 1.4, delay: 0.6 + i * 0.15, ease: [0.16, 1, 0.3, 1] }}
                    className="h-full bg-gradient-to-r from-[#D7FF00] to-[#aaff66]"
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Two-col panels */}
        <div className="grid grid-cols-2 gap-3">
          {/* Skill gap */}
          <div className="border border-white/[0.06] p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">SKILL GAP</div>
              <Target size={14} weight="duotone" className="text-blue-400" />
            </div>
            <div className="flex flex-wrap gap-1.5">
              {["Docker", "K8s", "AWS", "LangGraph"].map((s) => (
                <span key={s} className="text-[10px] font-mono px-2 py-0.5 border border-red-500/30 text-red-300/90">{s}</span>
              ))}
            </div>
          </div>

          {/* Roadmap */}
          <div className="border border-white/[0.06] p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">ROADMAP · Q1</div>
              <FlowArrow size={14} weight="duotone" className="text-purple-400" />
            </div>
            <div className="space-y-1.5 text-[11px]">
              {[
                ["M1", "Deep Learning"],
                ["M2", "LangGraph"],
                ["M3", "MLOps"],
              ].map(([m, t]) => (
                <div key={m} className="flex gap-2 items-center">
                  <span className="font-mono text-zinc-600 text-[9px]">{m}</span>
                  <span className="text-zinc-300">{t}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Voice interview tile */}
        <div className="border border-white/[0.06] p-4 bg-gradient-to-br from-[var(--accent)]/[0.04] to-transparent">
          <div className="flex items-center justify-between mb-3">
            <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 flex items-center gap-2">
              <span className="block w-1.5 h-1.5 rounded-full bg-[var(--accent)] animate-pulse" />
              VOICE INTERVIEW · ACTIVE
            </div>
            <Microphone size={14} weight="fill" className="text-[var(--accent)]" />
          </div>
          <div className="flex items-end gap-1 h-8 mb-2">
            {[...Array(28)].map((_, i) => (
              <motion.span
                key={i}
                animate={{ height: ["20%", "90%", "30%", "70%", "20%"] }}
                transition={{ duration: 1.2, repeat: Infinity, delay: i * 0.04, ease: "easeInOut" }}
                className="w-[3px] bg-gradient-to-t from-[var(--accent)]/30 to-[var(--accent)] inline-block"
              />
            ))}
          </div>
          <div className="flex justify-between text-[10px] font-mono">
            <span className="text-zinc-500">Confidence</span>
            <span className="text-[var(--accent)]">87%</span>
          </div>
        </div>

        {/* Live jobs feed */}
        <div className="border border-white/[0.06] p-4">
          <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-3">LIVE JOBS · 14 NEW</div>
          <div className="space-y-2">
            {[
              ["Google", "Senior AI Engineer", "₹42-58 LPA", 92],
              ["Anthropic", "ML Researcher", "$180-220k", 87],
              ["Perplexity", "LLM Engineer", "$160-200k", 84],
            ].map(([co, t, sal, m], i) => (
              <motion.div
                key={co}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 1 + i * 0.15 }}
                className="flex justify-between items-center text-[11px] py-1 border-b border-white/[0.04] last:border-0"
              >
                <div className="min-w-0">
                  <div className="text-zinc-300">{t}</div>
                  <div className="text-zinc-600 font-mono text-[10px]">{co} · {sal}</div>
                </div>
                <span className="font-mono text-[var(--accent)] text-[11px] shrink-0">{m}%</span>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </motion.div>

    {/* Floating notifications */}
    <FloatNote icon={Sparkle} label="OPPORTUNITY" value="14 new jobs matched" delay={1.0} x="-120px" y="40px" />
    <FloatNote icon={ChartLineUp} label="RESUME ATS" value="Score +12 → 94/100" delay={1.3} x="-90px" y="auto" />
    <div className="hidden lg:block absolute right-[-100px] top-[120px]">
      <FloatNote icon={Robot} label="CAREER TWIN" value="This week's brief ready" delay={1.6} x="0" y="0" />
    </div>
    <div className="hidden lg:block absolute right-[-130px] bottom-[60px]">
      <FloatNote icon={CheckCircle} label="MOCK INTERVIEW" value="Confidence improved" delay={1.9} x="0" y="0" />
    </div>
  </div>
);

/* ============ Section: Feature spotlights ============ */
const features = [
  { icon: Brain, title: "AI Career Matching", desc: "Five paths ranked by market signal, salary range, and skill fit — refreshed weekly.", k: "01" },
  { icon: Target, title: "Skill Gap Diff", desc: "Your skills vs the role — prioritized, time-estimated, and difficulty-tagged.", k: "02" },
  { icon: FlowArrow, title: "Personalized Roadmap", desc: "Month-by-month, week-by-week plan with togglable milestones.", k: "03" },
  { icon: ChartLineUp, title: "ATS Resume Engine", desc: "PDF/DOCX in, ATS score + AI-rewritten .docx out. Truthful. Quantified.", k: "04" },
  { icon: GithubLogo, title: "GitHub Audit", desc: "Repo-by-repo critique with portfolio score and concrete improvements.", k: "05" },
  { icon: Microphone, title: "Voice Mock Interview", desc: "ElevenLabs voice · Deepgram STT · Gemini eval. 5-axis scored reports.", k: "06" },
  { icon: Robot, title: "AI Career Twin", desc: "A persistent agent watching the market and your growth every week.", k: "07" },
  { icon: Briefcase, title: "Live Jobs Intel", desc: "Real jobs from JSearch & Adzuna with personalized match scores.", k: "08" },
  { icon: ChatCircleDots, title: "AI Mentor Chat", desc: "Streaming Gemini chat with semantic memory across sessions.", k: "09" },
];

const PillNav = ({ items }) => (
  <nav className="hidden md:flex items-center gap-1 text-sm">
    {items.map((it) => (
      <a key={it.href} href={it.href}
        className="px-4 py-2 text-zinc-400 hover:text-white transition-colors relative group">
        <span>{it.label}</span>
        <span className="absolute inset-x-3 -bottom-0.5 h-px bg-[var(--accent)] scale-x-0 group-hover:scale-x-100 transition-transform origin-left" />
      </a>
    ))}
  </nav>
);

export default function Landing() {
  return (
    <div className="min-h-screen bg-[#050505] text-white overflow-x-hidden">
      {/* Cinematic background */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute inset-0 grid-bg opacity-30" />
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1200px] h-[800px] bg-gradient-radial from-[#D7FF00]/[0.08] via-transparent to-transparent blur-3xl" />
        <div className="absolute top-[40%] -right-40 w-[600px] h-[600px] bg-blue-600/10 blur-[120px] rounded-full" />
        <div className="absolute bottom-0 -left-40 w-[600px] h-[600px] bg-purple-600/[0.08] blur-[120px] rounded-full" />
        <div className="absolute inset-0 noise" />
      </div>

      {/* Nav */}
      <header className="relative z-50">
        <motion.div
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6 }}
          className="sticky top-4 mx-auto max-w-6xl px-4"
        >
          <div className="flex items-center justify-between backdrop-blur-2xl bg-zinc-950/60 border border-white/[0.08] px-5 py-3 rounded-full shadow-xl shadow-black/40">
            <Link to="/" className="flex items-center gap-2.5" data-testid="landing-logo">
              <div className="relative">
                <span className="block w-2.5 h-2.5 bg-[var(--accent)] rounded-full" />
                <span className="absolute inset-0 bg-[var(--accent)] rounded-full blur-md opacity-60" />
              </div>
              <span className="font-display text-base font-extrabold tracking-tight">CareerPilot AI</span>
            </Link>
            <PillNav items={[
              { href: "#features", label: "Features" },
              { href: "#twin", label: "AI Career Twin" },
              { href: "#interview", label: "Mock Interviews" },
              { href: "#roadmap", label: "Roadmaps" },
              { href: "#jobs", label: "Jobs" },
            ]} />
            <div className="flex items-center gap-2">
              <Link to="/login" className="text-sm text-zinc-300 hover:text-white px-3 py-1.5" data-testid="header-signin">
                Sign In
              </Link>
              <Link to="/login"
                className="group bg-[var(--accent)] hover:bg-[#e6ff33] text-black text-sm font-bold px-4 py-2 rounded-full flex items-center gap-1.5 transition-all hover:shadow-[0_0_30px_rgba(215,255,0,0.4)]"
                data-testid="header-cta">
                Launch Console
                <ArrowUpRight size={14} weight="bold" className="group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
              </Link>
            </div>
          </div>
        </motion.div>
      </header>

      {/* HERO */}
      <section className="relative pt-20 lg:pt-28 pb-24 lg:pb-32">
        <div className="max-w-7xl mx-auto px-6 lg:px-10">
          <div className="grid lg:grid-cols-12 gap-12 lg:gap-16 items-center">
            {/* LEFT */}
            <div className="lg:col-span-6 relative z-10">
              <motion.div
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                className="inline-flex items-center gap-2 backdrop-blur-md bg-white/[0.03] border border-white/[0.08] px-3 py-1.5 mb-8"
              >
                <span className="block w-1.5 h-1.5 bg-[var(--accent)] rounded-full animate-pulse" />
                <span className="text-[11px] font-mono uppercase tracking-widest text-zinc-400">
                  AI CAREER OS · v2 RELEASED · FREE FOR ALL
                </span>
              </motion.div>

              <motion.h1
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7, delay: 0.1 }}
                className="font-display text-5xl sm:text-6xl lg:text-7xl xl:text-[5.5rem] font-black leading-[0.93] tracking-[-0.045em]"
              >
                Your AI-powered<br />
                career
                <span className="relative inline-block ml-3">
                  <span className="bg-gradient-to-br from-[#D7FF00] via-[#e6ff66] to-[#aaff33] bg-clip-text text-transparent">
                    operating system.
                  </span>
                  <span className="absolute inset-0 bg-gradient-to-br from-[#D7FF00] via-[#e6ff66] to-[#aaff33] bg-clip-text text-transparent blur-[12px] opacity-30">
                    operating system.
                  </span>
                </span>
              </motion.h1>

              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7, delay: 0.2 }}
                className="mt-8 text-lg lg:text-xl text-zinc-400 leading-relaxed max-w-xl"
              >
                CareerPilot AI analyzes your resume, audits your GitHub, tracks industry
                trends, and builds a personalized roadmap — with live job intelligence
                and voice-AI mock interviews.
              </motion.p>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7, delay: 0.3 }}
                className="mt-10 flex flex-wrap gap-3"
              >
                <Link to="/login"
                  data-testid="hero-cta-primary"
                  className="group relative bg-[var(--accent)] hover:bg-[#e6ff33] text-black font-bold px-6 py-3.5 rounded-full flex items-center gap-2 transition-all hover:shadow-[0_0_50px_rgba(215,255,0,0.5)]">
                  <RocketLaunch size={18} weight="bold" />
                  Launch Career Console
                  <ArrowRight size={16} weight="bold" className="group-hover:translate-x-1 transition-transform" />
                </Link>
                <a href="#features"
                  data-testid="hero-cta-secondary"
                  className="backdrop-blur-md bg-white/[0.03] border border-white/10 hover:border-white/30 hover:bg-white/[0.06] text-white px-6 py-3.5 rounded-full flex items-center gap-2 transition-all">
                  <Play size={14} weight="fill" />
                  Watch AI Demo
                </a>
              </motion.div>

              {/* trust strip */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.7, delay: 0.5 }}
                className="mt-14 grid grid-cols-3 gap-6 max-w-md"
              >
                {[
                  { v: <><Counter to={12} />K+</>, l: "Roadmaps generated" },
                  { v: <><Counter to={98} />%</>, l: "Match accuracy" },
                  { v: <>5.2×</>, l: "Faster job hunt" },
                ].map((s, i) => (
                  <div key={i}>
                    <div className="font-display text-2xl lg:text-3xl font-black tracking-tight">{s.v}</div>
                    <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mt-1">{s.l}</div>
                  </div>
                ))}
              </motion.div>
            </div>

            {/* RIGHT */}
            <div className="lg:col-span-6 relative">
              <DashboardMock />
            </div>
          </div>
        </div>
      </section>

      {/* Capability strip */}
      <section className="relative border-y border-white/[0.06] backdrop-blur-sm bg-zinc-950/40">
        <div className="max-w-7xl mx-auto px-6 lg:px-10 py-6 flex items-center gap-12 overflow-x-auto">
          <span className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 shrink-0">POWERED BY</span>
          {["Gemini 2.5 Flash", "ElevenLabs Voice", "Deepgram Nova-3", "Qdrant Vectors", "LangGraph Agents", "JSearch · Adzuna", "GitHub API"].map((t) => (
            <span key={t} className="text-sm text-zinc-400 whitespace-nowrap font-mono">{t}</span>
          ))}
        </div>
      </section>

      {/* FEATURES */}
      <section id="features" className="relative py-24 lg:py-32">
        <div className="max-w-7xl mx-auto px-6 lg:px-10">
          <div className="max-w-3xl mb-16">
            <div className="inline-flex items-center gap-2 text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-4">
              <span className="block w-3 h-px bg-[var(--accent)]" /> THE FULL CAREER STACK
            </div>
            <h2 className="font-display text-4xl lg:text-6xl font-black tracking-[-0.04em] leading-[1]">
              One console.<br />
              <span className="text-zinc-500">Every career decision.</span>
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-px bg-white/[0.05] border border-white/[0.05]">
            {features.map((f, i) => (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-80px" }}
                transition={{ duration: 0.5, delay: (i % 3) * 0.08 }}
                className="bg-[#0a0a0a] p-8 group hover:bg-zinc-950 transition-colors relative overflow-hidden"
                data-testid={`feature-${i}`}
              >
                <div className="absolute top-6 right-6 text-[10px] font-mono text-zinc-700 group-hover:text-[var(--accent)] transition-colors">
                  {f.k}
                </div>
                <div className="relative inline-flex items-center justify-center w-12 h-12 mb-6 bg-[var(--accent)]/[0.06] border border-[var(--accent)]/20">
                  <f.icon size={20} weight="duotone" className="text-[var(--accent)]" />
                  <div className="absolute inset-0 bg-[var(--accent)]/10 blur-xl opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
                <h3 className="font-display text-xl font-extrabold mb-2 tracking-tight">{f.title}</h3>
                <p className="text-sm text-zinc-400 leading-relaxed">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Career Twin spotlight */}
      <section id="twin" className="relative py-24 lg:py-32 border-t border-white/[0.05]">
        <div className="max-w-7xl mx-auto px-6 lg:px-10 grid lg:grid-cols-12 gap-12 items-center">
          <div className="lg:col-span-5">
            <div className="inline-flex items-center gap-2 text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-4">
              <Robot size={12} weight="fill" className="text-[var(--accent)]" /> AI CAREER TWIN
            </div>
            <h2 className="font-display text-4xl lg:text-5xl font-black tracking-[-0.04em] leading-[1.05] mb-6">
              A persistent agent<br />tracking the market<br /><span className="text-[var(--accent)]">and you</span>.
            </h2>
            <p className="text-lg text-zinc-400 leading-relaxed">
              Every week, your Career Twin reads the market, scans your progress, and ships a brief:
              what to learn, what to ignore, and where the next opportunity is hiding.
            </p>
          </div>
          <div className="lg:col-span-7">
            <div className="backdrop-blur-2xl bg-zinc-950/60 border border-white/[0.07] p-8 relative overflow-hidden">
              <div className="absolute -inset-1 bg-gradient-to-br from-[#D7FF00]/[0.06] to-transparent pointer-events-none" />
              <div className="relative">
                <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-4">WEEK OF 11 FEB · 2026</div>
                <p className="font-display text-2xl lg:text-3xl font-extrabold mb-6 leading-snug">
                  "Tarun — the LangGraph supervisor pattern is exploding. You're 3 weeks away from a real
                  agentic AI role."
                </p>
                <div className="grid sm:grid-cols-2 gap-4 mb-6">
                  {[
                    ["Market signals", "Anthropic shipped MCP v2 · 14% more agentic-AI postings"],
                    ["This week's focus", "Build a LangGraph supervisor with 3 worker agents"],
                  ].map(([k, v]) => (
                    <div key={k} className="border border-white/[0.06] p-4">
                      <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-2">{k}</div>
                      <div className="text-sm text-zinc-200">{v}</div>
                    </div>
                  ))}
                </div>
                <Link to="/login" className="inline-flex items-center gap-1.5 text-[var(--accent)] text-sm font-mono">
                  WAKE YOUR TWIN <ArrowRight size={12} />
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Mock interview spotlight */}
      <section id="interview" className="relative py-24 lg:py-32 border-t border-white/[0.05]">
        <div className="max-w-7xl mx-auto px-6 lg:px-10 grid lg:grid-cols-12 gap-12 items-center">
          <div className="lg:col-span-7 order-2 lg:order-1">
            <div className="backdrop-blur-2xl bg-zinc-950/60 border border-white/[0.07] p-8 relative">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-[var(--accent)]/[0.08] border border-[var(--accent)]/30 flex items-center justify-center">
                    <Microphone size={20} weight="duotone" className="text-[var(--accent)]" />
                  </div>
                  <div>
                    <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500">DANIEL · FAANG LEAD</div>
                    <div className="font-display text-lg font-extrabold">Senior ML Engineer interview</div>
                  </div>
                </div>
                <div className="text-[10px] font-mono text-[var(--accent)] flex items-center gap-2">
                  <span className="block w-1.5 h-1.5 rounded-full bg-[var(--accent)] animate-pulse" />
                  LIVE
                </div>
              </div>
              <div className="flex items-end gap-1 h-16 mb-6">
                {[...Array(48)].map((_, i) => (
                  <motion.span
                    key={i}
                    animate={{ height: [`${20 + (i*7)%70}%`, `${30 + (i*13)%60}%`, `${20 + (i*7)%70}%`] }}
                    transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.03, ease: "easeInOut" }}
                    className="flex-1 bg-gradient-to-t from-[var(--accent)]/30 to-[var(--accent)]"
                  />
                ))}
              </div>
              <div className="border-l-2 border-[var(--accent)] pl-4 mb-4">
                <div className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-1">Q3 · INTERVIEWER</div>
                <p className="text-zinc-200">How would you scale a LangGraph supervisor for 1M concurrent agent runs?</p>
              </div>
              <div className="grid grid-cols-5 gap-2">
                {[["Tech", 92], ["Comm", 88], ["Conf", 87], ["Solve", 94], ["Clarity", 90]].map(([k, v]) => (
                  <div key={k} className="text-center">
                    <div className="text-[10px] font-mono text-zinc-500">{k}</div>
                    <div className="font-display text-xl font-black text-[var(--accent)]">{v}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="lg:col-span-5 order-1 lg:order-2">
            <div className="inline-flex items-center gap-2 text-[10px] font-mono uppercase tracking-widest text-zinc-500 mb-4">
              <WaveSawtooth size={12} weight="fill" className="text-[var(--accent)]" /> VOICE MOCK INTERVIEWS
            </div>
            <h2 className="font-display text-4xl lg:text-5xl font-black tracking-[-0.04em] leading-[1.05] mb-6">
              Practice with a<br />real interviewer.<br /><span className="text-[var(--accent)]">Almost.</span>
            </h2>
            <p className="text-lg text-zinc-400 leading-relaxed mb-6">
              ElevenLabs voice · Deepgram real-time transcripts · Gemini evaluation · Monaco coding rounds.
              Six interviewer personalities, four difficulty levels, six interview types — including FAANG-strict.
            </p>
            <Link to="/login" className="inline-flex items-center gap-1.5 text-[var(--accent)] text-sm font-mono">
              START A MOCK <ArrowRight size={12} />
            </Link>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="relative py-32 lg:py-40 border-t border-white/[0.05]">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#D7FF00]/[0.02] to-transparent" />
        <div className="relative max-w-4xl mx-auto px-6 lg:px-10 text-center">
          <Lightning size={36} weight="fill" className="text-[var(--accent)] mx-auto mb-6" />
          <h2 className="font-display text-5xl lg:text-7xl font-black tracking-[-0.04em] leading-[1]">
            Stop guessing.<br />Start <span className="bg-gradient-to-br from-[#D7FF00] to-[#aaff33] bg-clip-text text-transparent">shipping</span>.
          </h2>
          <p className="mt-6 text-lg text-zinc-400 max-w-2xl mx-auto">
            Free forever. No credit card. Your career compiled in minutes.
          </p>
          <div className="mt-10">
            <Link to="/login" data-testid="footer-cta"
              className="group inline-flex items-center gap-2 bg-[var(--accent)] hover:bg-[#e6ff33] text-black font-bold px-7 py-4 rounded-full transition-all hover:shadow-[0_0_60px_rgba(215,255,0,0.5)]">
              <RocketLaunch size={20} weight="bold" /> Launch CareerPilot AI
              <ArrowRight size={18} weight="bold" className="group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>
        </div>
      </section>

      <footer className="relative border-t border-white/[0.05] py-10">
        <div className="max-w-7xl mx-auto px-6 lg:px-10 flex flex-col md:flex-row items-center justify-between gap-4 text-[10px] font-mono uppercase tracking-widest text-zinc-600">
          <div>© 2026 · CAREERPILOT AI · CRAFTED FOR AMBITIOUS PEOPLE</div>
          <div className="flex gap-6">
            <span className="flex items-center gap-2">
              <span className="block w-1.5 h-1.5 bg-[var(--accent)] rounded-full animate-pulse" />
              STATUS · ONLINE
            </span>
            <span>v2.0.0</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
