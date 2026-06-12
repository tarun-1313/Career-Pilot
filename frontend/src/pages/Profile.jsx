import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { updateProfile } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { toast } from "sonner";
import { FloppyDisk, Plus, X } from "@phosphor-icons/react";

const Field = ({ label, children, testid }) => (
  <label className="block">
    <div className="overline mb-2">{label}</div>
    {children}
  </label>
);

const TagInput = ({ value, onChange, placeholder, testid }) => {
  const [t, setT] = useState("");
  const add = () => {
    const v = t.trim();
    if (!v) return;
    if (!value.includes(v)) onChange([...value, v]);
    setT("");
  };
  return (
    <div>
      <div className="flex gap-2">
        <input
          value={t}
          onChange={(e) => setT(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), add())}
          placeholder={placeholder}
          data-testid={testid}
          className="flex-1 bg-elevated border border-default px-3 py-2.5 text-sm outline-none focus:border-[var(--accent)]"
        />
        <button onClick={add} type="button" className="btn-ghost px-3" aria-label="add tag">
          <Plus size={16} />
        </button>
      </div>
      <div className="flex flex-wrap gap-2 mt-3">
        {value.map((s, i) => (
          <span key={i} className="bg-elevated border border-default px-3 py-1.5 text-xs font-mono flex items-center gap-2">
            {s}
            <button onClick={() => onChange(value.filter((x) => x !== s))} aria-label="remove">
              <X size={12} />
            </button>
          </span>
        ))}
      </div>
    </div>
  );
};

export default function Profile({ onboarding = false }) {
  const { user, refresh } = useAuth();
  const navigate = useNavigate();
  const [f, setF] = useState({
    name: "", education: "", degree: "", graduation_year: "",
    skills: [], interests: [], career_goals: "", preferred_industry: "",
    preferred_location: "", expected_salary: "", github_url: "", portfolio_url: "",
  });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (user) {
      setF((prev) => ({
        ...prev,
        name: user.name || "",
        education: user.education || "",
        degree: user.degree || "",
        graduation_year: user.graduation_year || "",
        skills: user.skills || [],
        interests: user.interests || [],
        career_goals: user.career_goals || "",
        preferred_industry: user.preferred_industry || "",
        preferred_location: user.preferred_location || "",
        expected_salary: user.expected_salary || "",
        github_url: user.github_url || "",
        portfolio_url: user.portfolio_url || "",
      }));
    }
  }, [user]);

  const save = async () => {
    setSaving(true);
    try {
      const body = { ...f };
      body.graduation_year = body.graduation_year ? Number(body.graduation_year) : null;
      await updateProfile(body);
      await refresh();
      toast.success("Profile saved");
      if (onboarding) navigate("/dashboard");
    } catch (e) {
      toast.error("Could not save profile");
    } finally { setSaving(false); }
  };

  const input = "w-full bg-elevated border border-default px-3 py-2.5 text-sm outline-none focus:border-[var(--accent)]";

  return (
    <div className="max-w-4xl space-y-8" data-testid="profile-root">
      <div>
        <div className="overline mb-3">{onboarding ? "ONBOARDING" : "ACCOUNT"}</div>
        <h1 className="font-display text-4xl lg:text-5xl font-black tracking-display">
          {onboarding ? "Tell us about you." : "Your profile."}
        </h1>
        <p className="text-secondary mt-2">The more we know, the sharper your matches.</p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <Field label="NAME">
          <input className={input} value={f.name} onChange={(e) => setF({ ...f, name: e.target.value })} data-testid="profile-name" />
        </Field>
        <Field label="EDUCATION">
          <input className={input} placeholder="IIT Madras" value={f.education} onChange={(e) => setF({ ...f, education: e.target.value })} data-testid="profile-education" />
        </Field>
        <Field label="DEGREE">
          <input className={input} placeholder="B.Tech CSE" value={f.degree} onChange={(e) => setF({ ...f, degree: e.target.value })} data-testid="profile-degree" />
        </Field>
        <Field label="GRADUATION YEAR">
          <input type="number" className={input} value={f.graduation_year} onChange={(e) => setF({ ...f, graduation_year: e.target.value })} data-testid="profile-gradyear" />
        </Field>
      </div>

      <Field label="SKILLS">
        <TagInput value={f.skills} onChange={(v) => setF({ ...f, skills: v })} placeholder="Add a skill and press Enter" testid="profile-skill-input" />
      </Field>

      <Field label="INTERESTS">
        <TagInput value={f.interests} onChange={(v) => setF({ ...f, interests: v })} placeholder="AI, LLMs, Web3, Robotics…" testid="profile-interest-input" />
      </Field>

      <div className="grid md:grid-cols-2 gap-6">
        <Field label="CAREER GOAL">
          <input className={input} placeholder="Senior ML Engineer at a foundation-model lab" value={f.career_goals} onChange={(e) => setF({ ...f, career_goals: e.target.value })} data-testid="profile-goal" />
        </Field>
        <Field label="PREFERRED INDUSTRY">
          <input className={input} placeholder="AI / FinTech / Healthcare" value={f.preferred_industry} onChange={(e) => setF({ ...f, preferred_industry: e.target.value })} data-testid="profile-industry" />
        </Field>
        <Field label="PREFERRED LOCATION">
          <input className={input} placeholder="Bengaluru / Remote" value={f.preferred_location} onChange={(e) => setF({ ...f, preferred_location: e.target.value })} data-testid="profile-location" />
        </Field>
        <Field label="EXPECTED SALARY">
          <input className={input} placeholder="18-25 LPA" value={f.expected_salary} onChange={(e) => setF({ ...f, expected_salary: e.target.value })} data-testid="profile-salary" />
        </Field>
        <Field label="GITHUB URL">
          <input className={input} placeholder="https://github.com/yourname" value={f.github_url} onChange={(e) => setF({ ...f, github_url: e.target.value })} data-testid="profile-github" />
        </Field>
        <Field label="PORTFOLIO URL">
          <input className={input} placeholder="https://yourname.dev" value={f.portfolio_url} onChange={(e) => setF({ ...f, portfolio_url: e.target.value })} data-testid="profile-portfolio" />
        </Field>
      </div>

      <button onClick={save} disabled={saving} className="btn-yellow" data-testid="profile-save-button">
        <FloppyDisk size={18} weight="bold" /> {saving ? "Saving..." : "Save profile"}
      </button>
    </div>
  );
}
