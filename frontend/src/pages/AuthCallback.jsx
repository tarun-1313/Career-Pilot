import React, { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { exchangeSession } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";

// REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
export default function AuthCallback() {
  const navigate = useNavigate();
  const { setUser } = useAuth();
  const processed = useRef(false);

  useEffect(() => {
    if (processed.current) return;
    processed.current = true;

    const hash = window.location.hash || "";
    const params = new URLSearchParams(hash.replace(/^#/, ""));
    const sessionId = params.get("session_id");
    if (!sessionId) {
      navigate("/login", { replace: true });
      return;
    }
    (async () => {
      try {
        const user = await exchangeSession(sessionId);
        setUser(user);
        // clear hash
        window.history.replaceState(null, "", window.location.pathname);
        navigate(user.onboarded ? "/dashboard" : "/onboarding", { replace: true, state: { user } });
      } catch (e) {
        console.error("auth callback failed", e);
        navigate("/login", { replace: true });
      }
    })();
  }, [navigate, setUser]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-base">
      <div className="text-center">
        <div className="dot-loader mb-4"><span/><span/><span/></div>
        <p className="overline">Signing you in</p>
      </div>
    </div>
  );
}
