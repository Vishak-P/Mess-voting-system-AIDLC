/**
 * Registration page.
 */
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import toast from "react-hot-toast";
import { Spinner } from "../components/Loader";

const RegisterPage = () => {
  const { register, loading } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "", confirm: "" });
  const [role, setRole] = useState("student");
  const [errors, setErrors] = useState({});

  const validate = () => {
    const errs = {};
    if (!form.name.trim()) errs.name = "Name is required";
    if (!form.email) errs.email = "Email is required";
    else if (!/\S+@\S+\.\S+/.test(form.email)) errs.email = "Invalid email";
    if (!form.password) errs.password = "Password is required";
    else if (form.password.length < 8) errs.password = "Minimum 8 characters";
    if (form.password !== form.confirm) errs.confirm = "Passwords do not match";
    return errs;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length) { setErrors(errs); return; }
    setErrors({});

    const result = await register(form.name, form.email, form.password, role);
    if (result.success) {
      toast.success("Account created! Welcome ");
      navigate(result.user.role === "admin" ? "/admin" : "/dashboard");
    } else {
      toast.error(result.error);
    }
  };

  const field = (id, label, type, placeholder, key) => (
    <div>
      <label className="label" htmlFor={id}>{label}</label>
      <input
        id={id}
        type={type}
        className={`input ${errors[key] ? "border-red-400 focus:ring-red-400" : ""}`}
        placeholder={placeholder}
        value={form[key]}
        onChange={(e) => setForm({ ...form, [key]: e.target.value })}
      />
      {errors[key] && <p className="text-red-500 text-xs mt-1">{errors[key]}</p>}
    </div>
  );

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="text-5xl mb-3"></div>
          <h1 className="text-2xl font-bold text-gray-900">Create Account</h1>
          <p className="text-gray-500 mt-1">Join the mess voting system</p>
        </div>

        <div className="card shadow-lg">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Register</h2>

          {/* Role toggle */}
          <div className="flex rounded-lg border border-gray-200 p-1 mb-5 bg-gray-50">
            <button
              type="button"
              onClick={() => setRole("student")}
              className={`flex-1 py-2 text-sm font-medium rounded-md transition-all ${
                role === "student"
                  ? "bg-white text-blue-600 shadow-sm border border-gray-200"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
               Register as Student
            </button>
            <button
              type="button"
              onClick={() => setRole("admin")}
              className={`flex-1 py-2 text-sm font-medium rounded-md transition-all ${
                role === "admin"
                  ? "bg-white text-indigo-600 shadow-sm border border-gray-200"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
               Register as Admin
            </button>
          </div>

          <form onSubmit={handleSubmit} noValidate className="space-y-4">
            {field("name", "Full Name", "text", "Your full name", "name")}
            {field("email", "Email address", "email", "you@example.com", "email")}
            {field("password", "Password", "password", "Min. 8 characters", "password")}
            {field("confirm", "Confirm Password", "password", "Repeat password", "confirm")}

            <button
              type="submit"
              className={`w-full mt-2 flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg font-medium text-white transition-colors ${
                role === "admin"
                  ? "bg-indigo-600 hover:bg-indigo-700"
                  : "bg-blue-600 hover:bg-blue-700"
              }`}
              disabled={loading}
            >
              {loading ? (
                <><Spinner size="sm" /> Creating account...</>
              ) : (
                `Create ${role === "admin" ? "Admin" : "Student"} Account`
              )}
            </button>
          </form>

          <p className="text-center text-sm text-gray-600 mt-4">
            Already have an account?{" "}
            <Link to="/login" className="text-blue-600 hover:underline font-medium">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
