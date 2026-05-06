/**
 * Dashboard page.
 * Admin: full analytics with charts.
 * Student: personal voting summary + today's menus.
 */
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line,
} from "recharts";
import { useAuth } from "../context/AuthContext";
import api from "../utils/api";
import { getErrorMessage, formatDate } from "../utils/helpers";
import StatCard from "../components/StatCard";
import ChartCard from "../components/ChartCard";
import { CardLoader } from "../components/Loader";
import toast from "react-hot-toast";

const COLORS = ["#3b82f6", "#f59e0b", "#10b981", "#8b5cf6", "#ef4444", "#06b6d4", "#f97316", "#84cc16"];

const DashboardPage = () => {
  const { user, isAdmin } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        if (isAdmin) {
          const { data } = await api.get("/dashboard/stats");
          setStats(data);
        } else {
          // Student: fetch today's menus + their votes
          const today = new Date().toISOString().split("T")[0];
          const [menusRes, votesRes] = await Promise.all([
            api.get(`/menus?date=${today}`),
            api.get("/my-votes"),
          ]);
          setStats({
            todayMenus: menusRes.data.menus,
            myVotes: votesRes.data.votes,
          });
        }
      } catch (err) {
        toast.error(getErrorMessage(err));
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, [isAdmin]);

  if (loading) return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="h-8 bg-gray-200 rounded w-48 mb-6 animate-pulse" />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {[...Array(4)].map((_, i) => <div key={i} className="card h-28 animate-pulse bg-gray-100" />)}
      </div>
      <CardLoader count={2} />
    </div>
  );

  // ---- ADMIN DASHBOARD ----
  if (isAdmin && stats) {
    const { summary, most_popular_dish, votes_per_day, dish_distribution, weekly_trends, meal_breakdown, recent_activity } = stats;

    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-gray-500 text-sm mt-1">Overview of voting activity</p>
        </div>

        {/* Summary cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <StatCard title="Total Votes" value={summary.total_votes} icon="🗳️" color="blue" />
          <StatCard title="Students" value={summary.total_students} icon="👥" color="green" />
          <StatCard title="Total Menus" value={summary.total_menus} icon="📋" color="amber" />
          <StatCard title="Active Menus" value={summary.active_menus} icon="✅" color="purple" />
        </div>

        {/* Most popular dish */}
        {most_popular_dish && (
          <div className="card bg-gradient-to-r from-blue-600 to-indigo-600 text-white mb-6 border-0">
            <p className="text-blue-100 text-sm font-medium mb-1">🏆 Most Popular Dish</p>
            <p className="text-2xl font-bold">{most_popular_dish.name}</p>
            <p className="text-blue-200 text-sm mt-1">{most_popular_dish.votes} total votes</p>
          </div>
        )}

        {/* Charts row 1 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <ChartCard title="Votes Per Day" subtitle="Last 14 days">
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={votes_per_day} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="date" tick={{ fontSize: 11 }} tickFormatter={(v) => v.slice(5)} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip formatter={(v) => [v, "Votes"]} labelFormatter={(l) => `Date: ${l}`} />
                <Bar dataKey="votes" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>

          <ChartCard title="Dish Distribution" subtitle="Top 10 dishes by votes">
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie
                  data={dish_distribution}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  nameKey="name"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  labelLine={false}
                >
                  {dish_distribution.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(v, n) => [v, n]} />
              </PieChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* Charts row 2 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <ChartCard title="Weekly Voting Trends" subtitle="Last 8 weeks">
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={weekly_trends} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="week" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip formatter={(v) => [v, "Votes"]} />
                <Line type="monotone" dataKey="votes" stroke="#8b5cf6" strokeWidth={2} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </ChartCard>

          <ChartCard title="Meal Type Breakdown" subtitle="Votes by meal">
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={meal_breakdown} layout="vertical" margin={{ top: 5, right: 10, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis type="number" tick={{ fontSize: 11 }} />
                <YAxis dataKey="meal" type="category" tick={{ fontSize: 11 }} />
                <Tooltip formatter={(v) => [v, "Votes"]} />
                <Bar dataKey="votes" fill="#10b981" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* Recent activity */}
        <div className="card">
          <h3 className="text-base font-semibold text-gray-900 mb-4">Recent Activity</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="text-left py-2 px-3 text-gray-500 font-medium">Student</th>
                  <th className="text-left py-2 px-3 text-gray-500 font-medium">Dish</th>
                  <th className="text-left py-2 px-3 text-gray-500 font-medium">Meal</th>
                  <th className="text-left py-2 px-3 text-gray-500 font-medium">Date</th>
                </tr>
              </thead>
              <tbody>
                {recent_activity.map((row, i) => (
                  <tr key={i} className="border-b border-gray-50 hover:bg-gray-50">
                    <td className="py-2 px-3 font-medium text-gray-900">{row.user}</td>
                    <td className="py-2 px-3 text-gray-700">{row.dish}</td>
                    <td className="py-2 px-3 capitalize text-gray-600">{row.meal}</td>
                    <td className="py-2 px-3 text-gray-500">{row.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  }

  // ---- STUDENT DASHBOARD ----
  const { todayMenus = [], myVotes = [] } = stats || {};
  const today = new Date().toISOString().split("T")[0];

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Welcome, {user?.name}! 👋</h1>
        <p className="text-gray-500 text-sm mt-1">Today is {formatDate(today, "EEEE, MMMM d, yyyy")}</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 gap-4 mb-8">
        <StatCard title="My Total Votes" value={myVotes.length} icon="🗳️" color="blue" />
        <StatCard title="Today's Menus" value={todayMenus.length} icon="📋" color="green" />
      </div>

      {/* Today's menus */}
      <div className="card mb-6">
        <h2 className="text-base font-semibold text-gray-900 mb-4">Today's Menu</h2>
        {todayMenus.length === 0 ? (
          <p className="text-gray-500 text-sm">No menus available for today.</p>
        ) : (
          <div className="space-y-3">
            {todayMenus.map((menu) => {
              const voted = myVotes.find((v) => v.menu_id === menu.id);
              return (
                <div key={menu.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900 capitalize">{menu.meal_type}</p>
                    <p className="text-xs text-gray-500">{menu.options?.length} options</p>
                  </div>
                  <div className="flex gap-2">
                    {voted ? (
                      <span className="badge bg-green-100 text-green-700">✓ Voted</span>
                    ) : menu.voting_open ? (
                      <Link to="/menu" className="btn-primary text-xs py-1.5 px-3">Vote</Link>
                    ) : (
                      <span className="badge bg-gray-100 text-gray-500">Closed</span>
                    )}
                    <Link to={`/results/${menu.id}`} className="btn-secondary text-xs py-1.5 px-3">Results</Link>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      <div className="flex gap-3">
        <Link to="/menu" className="btn-primary flex-1 text-center">View Weekly Menu</Link>
        <Link to="/results" className="btn-secondary flex-1 text-center">View Results</Link>
      </div>
    </div>
  );
};

export default DashboardPage;
