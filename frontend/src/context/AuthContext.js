/**
 * Authentication context.
 * Provides user state, login, logout, and register functions.
 */
import React, { createContext, useContext, useState, useCallback } from "react";
import api from "../utils/api";
import { getErrorMessage } from "../utils/helpers";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    try {
      const stored = localStorage.getItem("user");
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  });

  const [loading, setLoading] = useState(false);

  const login = useCallback(async (email, password) => {
    setLoading(true);
    try {
      const { data } = await api.post("/login", { email, password });
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));
      setUser(data.user);
      return { success: true, user: data.user };
    } catch (error) {
      return { success: false, error: getErrorMessage(error) };
    } finally {
      setLoading(false);
    }
  }, []);

  const register = useCallback(async (name, email, password, role = "student") => {
    setLoading(true);
    try {
      const { data } = await api.post("/register", { name, email, password, role });
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));
      setUser(data.user);
      return { success: true, user: data.user };
    } catch (error) {
      return { success: false, error: getErrorMessage(error) };
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setUser(null);
  }, []);

  const isAdmin = user?.role === "admin";
  const isStudent = user?.role === "student";

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, isAdmin, isStudent }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
