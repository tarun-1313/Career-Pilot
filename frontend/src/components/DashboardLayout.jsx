import React, { useState } from "react";
import { Link, NavLink, useNavigate, Outlet } from "react-router-dom";
import {
  House, User, FileText, Compass, ChartBar, Path, GraduationCap,
  Briefcase, ChatCircleDots, Microphone, GithubLogo, TrendUp, SignOut, List, X,
  Robot, ShareNetwork,
} from "@phosphor-icons/react";
import { useAuth } from "@/context/AuthContext";

const nav = [
  { to: "/dashboard", label: "Overview", icon: House },
  { to: "/twin", label: "Career Twin", icon: Robot },
  { to: "/profile", label: "Profile", icon: User },
  { to: "/resume", label: "Resume / ATS", icon: FileText },
  { to: "/careers", label: "Career Paths", icon: Compass },
  { to: "/skills", label: "Skill Gap", icon: ChartBar },
  { to: "/roadmap", label: "Roadmap", icon: Path },
  { to: "/courses", label: "Courses", icon: GraduationCap },
  { to: "/jobs", label: "Jobs", icon: Briefcase },
  { to: "/voice-interview", label: "Voice Interview", icon: Microphone },
  { to: "/interview", label: "Text Interview", icon: Microphone },
  { to: "/chat", label: "AI Mentor", icon: ChatCircleDots },
  { to: "/portfolio", label: "GitHub Analyzer", icon: GithubLogo },
  { to: "/trends", label: "Industry Trends", icon: TrendUp },
  { to: "/share", label: "Public Page", icon: ShareNetwork },
];

export default function DashboardLayout() {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  const handleLogout = async () => {
    await signOut();
    navigate("/", { replace: true });
  };

  return (
    <div className="min-h-screen bg-base text-white flex">
      {/* sidebar */}
      <aside
        className={`fixed lg:static top-0 left-0 h-screen w-64 bg-surface border-r border-default z-40 transform transition-transform ${
          open ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        }`}
      >
        <div className="px-6 py-6 border-b border-default flex items-center justify-between">
          <Link to="/dashboard" className="flex items-center gap-2" data-testid="sidebar-logo">
            <span className="block w-3 h-3 bg-accent-yellow"></span>
            <span className="font-display text-lg font-extrabold tracking-display">CareerPilot</span>
          </Link>
          <button className="lg:hidden text-white" onClick={() => setOpen(false)} aria-label="close">
            <X size={20} />
          </button>
        </div>
        <nav className="px-3 py-4 space-y-1 overflow-y-auto h-[calc(100vh-180px)]">
          {nav.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              onClick={() => setOpen(false)}
              data-testid={`nav-${label.toLowerCase().replace(/\s+/g, "-")}`}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 text-sm transition-colors ${
                  isActive
                    ? "bg-elevated text-white border-l-2 border-[var(--accent)]"
                    : "text-secondary hover:bg-elevated hover:text-white"
                }`
              }
            >
              <Icon size={18} weight="duotone" />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="absolute bottom-0 left-0 right-0 p-3 border-t border-default bg-surface">
          <div className="flex items-center gap-3 px-2 py-2">
            {user?.picture ? (
              <img src={user.picture} alt="" className="w-8 h-8 rounded-full" />
            ) : (
              <div className="w-8 h-8 bg-elevated flex items-center justify-center font-mono text-xs">
                {user?.name?.[0] || "U"}
              </div>
            )}
            <div className="flex-1 min-w-0">
              <div className="text-sm truncate">{user?.name}</div>
              <div className="text-xs text-muted truncate">{user?.email}</div>
            </div>
            <button
              onClick={handleLogout}
              data-testid="logout-button"
              className="text-secondary hover:text-white"
              aria-label="logout"
            >
              <SignOut size={18} />
            </button>
          </div>
        </div>
      </aside>

      {/* main */}
      <div className="flex-1 min-w-0">
        <header className="glass-header sticky top-0 z-30 px-6 lg:px-10 py-4 flex items-center justify-between">
          <button
            className="lg:hidden text-white"
            onClick={() => setOpen(true)}
            aria-label="open-menu"
            data-testid="open-menu-button"
          >
            <List size={22} />
          </button>
          <div className="overline">CareerPilot AI · Dashboard</div>
          <div className="hidden lg:flex items-center gap-3">
            <span className="text-xs text-muted font-mono">welcome back,</span>
            <span className="text-sm">{user?.name}</span>
          </div>
        </header>
        <main className="px-6 lg:px-10 py-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
