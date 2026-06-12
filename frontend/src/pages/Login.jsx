import React from "react";
import { Link } from "react-router-dom";
import { GoogleLogo, ArrowLeft } from "@phosphor-icons/react";

// REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
export default function Login() {
  const handleGoogle = () => {
    const redirectUrl = window.location.origin + "/auth/callback";
    window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
  };

  return (
    <div className="min-h-screen bg-base text-white grid lg:grid-cols-2">
      {/* left */}
      <div className="relative hidden lg:block noise overflow-hidden">
        <div
          className="absolute inset-0 opacity-40"
          style={{
            backgroundImage: `url(https://images.pexels.com/photos/13129482/pexels-photo-13129482.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940)`,
            backgroundSize: "cover", backgroundPosition: "center",
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-br from-[#0c0c0c]/40 via-[#0c0c0c]/70 to-[#0c0c0c]" />
        <div className="relative h-full p-12 flex flex-col">
          <Link to="/" className="flex items-center gap-2" data-testid="login-logo">
            <span className="block w-3 h-3 bg-accent-yellow"></span>
            <span className="font-display text-lg font-extrabold tracking-display">CareerPilot AI</span>
          </Link>
          <div className="mt-auto">
            <div className="overline mb-4">FOR AMBITIOUS PEOPLE</div>
            <h2 className="font-display text-5xl font-black tracking-display leading-tight">
              Your career,<br/><span className="text-accent">compiled.</span>
            </h2>
            <p className="mt-6 text-secondary max-w-md">
              One sign-in. Twelve AI agents. A career operating system that actually ships.
            </p>
          </div>
        </div>
      </div>

      {/* right */}
      <div className="flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          <Link to="/" className="overline flex items-center gap-2 mb-10" data-testid="back-home">
            <ArrowLeft size={14} /> BACK
          </Link>
          <div className="overline mb-3">AUTHENTICATE</div>
          <h1 className="font-display text-4xl lg:text-5xl font-black tracking-display mb-3">
            Sign in to your console.
          </h1>
          <p className="text-secondary mb-10">
            One click. Google handles the heavy lifting. We handle your career.
          </p>

          <button
            onClick={handleGoogle}
            data-testid="google-login-button"
            className="w-full flex items-center justify-center gap-3 bg-white text-black font-bold py-4 hover:bg-[#f4f4f5] transition-colors rounded-none"
          >
            <GoogleLogo size={20} weight="bold" />
            Continue with Google
          </button>

          <div className="mt-8 text-xs text-muted font-mono leading-relaxed">
            By continuing, you agree to our zero-tracking philosophy. We don't sell data —
            we sell outcomes.
          </div>

          <div className="mt-12 pt-8 border-t border-default text-xs text-muted font-mono">
            EMERGENT-MANAGED GOOGLE AUTH · 7-DAY SESSION
          </div>
        </div>
      </div>
    </div>
  );
}
