/**
 * App root - sets up routing, auth context, and toast notifications.
 */
import React from "react";
import { BrowserRouter, Routes, Route, Navigate, Outlet } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import { PageLoader } from "./components/Loader";

// Pages (lazy-loaded for performance)
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import DashboardPage from "./pages/DashboardPage";
import VotingPage from "./pages/VotingPage";
import ResultsPage from "./pages/ResultsPage";
import AdminPanel from "./pages/AdminPanel";

// ---- Route guards ----

/** Redirect to dashboard if already logged in */
const PublicRoute = () => {
  const { user } = useAuth();
  if (user) return <Navigate to="/dashboard" replace />;
  return <Outlet />;
};

/** Require authentication */
const PrivateRoute = () => {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main>
        <Outlet />
      </main>
    </div>
  );
};

/** Require admin role */
const AdminRoute = () => {
  const { user, isAdmin } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  if (!isAdmin) return <Navigate to="/dashboard" replace />;
  return <Outlet />;
};

// ---- App ----
const AppRoutes = () => {
  return (
    <Routes>
      {/* Public routes */}
      <Route element={<PublicRoute />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Route>

      {/* Protected routes */}
      <Route element={<PrivateRoute />}>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/menu" element={<VotingPage />} />
        <Route path="/results" element={<ResultsPage />} />
        <Route path="/results/:menu_id" element={<ResultsPage />} />

        {/* Admin only */}
        <Route element={<AdminRoute />}>
          <Route path="/admin" element={<AdminPanel />} />
        </Route>
      </Route>

      {/* Default redirect */}
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
};

const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 3500,
            style: { fontSize: "14px", maxWidth: "380px" },
            success: { iconTheme: { primary: "#10b981", secondary: "#fff" } },
            error: { iconTheme: { primary: "#ef4444", secondary: "#fff" } },
          }}
        />
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
