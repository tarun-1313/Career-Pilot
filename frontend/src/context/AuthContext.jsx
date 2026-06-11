import React, { createContext, useContext, useEffect, useState, useCallback } from "react";
import { fetchMe, logout as apiLogout } from "@/lib/api";

const AuthCtx = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    try {
      const u = await fetchMe();
      setUser(u);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    // CRITICAL: skip /me check if returning from OAuth callback — AuthCallback handles it.
    if (window.location.hash?.includes("session_id=")) {
      setLoading(false);
      return;
    }
    // Skip auth probe on public profile route to avoid benign 401 in console.
    if (window.location.pathname.startsWith("/u/")) {
      setLoading(false);
      return;
    }
    refresh();
  }, [refresh]);

  const signOut = async () => {
    try { await apiLogout(); } catch {}
    setUser(null);
  };

  return (
    <AuthCtx.Provider value={{ user, setUser, loading, refresh, signOut }}>
      {children}
    </AuthCtx.Provider>
  );
};

export const useAuth = () => useContext(AuthCtx);
