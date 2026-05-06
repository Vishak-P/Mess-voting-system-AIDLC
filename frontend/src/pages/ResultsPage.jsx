/**
 * ResultsPage — voting results viewer.
 * - ResultsList: all menus with links to individual results
 * - ResultDetail: per-menu results with chart, ranked list, feedback form
 * BR-04: students see results only after deadline.
 */
import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell,
} from "recharts";
import { useAuth } from "../context/AuthContext";
import api from "../utils/api";
import {
  getErrorMessage, formatDate, getMealIcon, capitalize,
  getMealColor, isDeadlinePassed,
} from "../utils/helpers";
import { CardLoader } from "../components/Loader";
import FeedbackForm from "../components/FeedbackForm";
import toast from "react-hot-toast";
import { FiArrowLeft, FiTrendingUp, FiCheckCircle, FiLock } from "react-icons/fi";

const COLORS = ["#3b82f6", "#f59e0b", "#10b981", "#8b5cf6", "#ef4444"];

// ---- Per-menu result detail ----
const ResultDetail = ({ menuId }) => {
  const { isAdmin } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);
  const [myFeedback, setMyFeedback] = useState(null);

  const fetchResults = async () => {
    try {
      const { data: res } = await api.get(`/results/${menuId}`);
      setData(res);
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  const fetchMyFeedback = async () => {
    try {
      const { data: res } = await api.get(`/feedback/${menuId}`);
      if (res.user_submitted) setMyFeedback(res.feedback[0]);
    } catch {
      // ignore — feedback may not exist yet
    }
  };

  useEffect(() => {
    if (menuId) {
      fetchResults();
      fetchMyFeedback();
    }
  }, [menuId]); // eslint-disable-line react-hooks/exhaustive-deps

  if (loading) return <div className="max-w-2xl mx-auto px-4 py-8"><CardLoader count={3} /></div>;
  if (!data) return <div className="max-w-2xl mx-auto px-4 py-8 text-center"><p className="text-gray-500">Results not found.</p></div>;

  const { menu, results, total_votes, user_voted, user_voted_option_id } = data;
  const winner = results[0];
  const deadlinePassed = isDeadlinePassed(menu.deadline);

  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 py-8">
      <Link to="/results" className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700 mb-6">
        <FiArrowLeft size={14} /> Back to all results
      </Link>

      {/* Header */}
      <div className="card mb-6">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-2xl">{getMealIcon(menu.meal_type)}</span>
              <span className={`badge border ${getMealColor(menu.meal_type)}`}>
                {capitalize(menu.meal_type)}
              </span>
              {menu.is_locked && (
                <span className="badge bg-red-100 text-red-700 border border-red-200 flex items-center gap-1">
                  <FiLock size={10} /> Locked
                </span>
              )}
              {user_voted && (
                <span className="badge bg-green-100 text-green-700 border border-green-200 flex items-center gap-1">
                  <FiCheckCircle size={10} /> Voted
                </span>
              )}
            </div>
            <h1 className="text-xl font-bold text-gray-900">
              {formatDate(menu.date, "EEEE, MMMM d, yyyy")}
            </h1>
          </div>
          <div className="text-right">
            <p className="text-2xl font-bold text-blue-600">{total_votes}</p>
            <p className="text-xs text-gray-500">total votes</p>
          </div>
        </div>
      </div>

      {/* Winner highlight */}
      {winner && total_votes > 0 && (
        <div className="card bg-gradient-to-r from-amber-50 to-yellow-50 border border-amber-200 mb-6">
          <div className="flex items-center gap-3">
            <span className="text-3xl">🏆</span>
            <div>
              <p className="text-xs font-medium text-amber-700 uppercase tracking-wide">Leading Dish</p>
              <p className="text-lg font-bold text-gray-900">{winner.dish_name}</p>
              <p className="text-sm text-amber-700">{winner.vote_count} votes · {winner.percentage}%</p>
            </div>
          </div>
        </div>
      )}

      {/* Bar chart */}
      {total_votes > 0 && (
        <div className="card mb-6">
          <h3 className="text-sm font-semibold text-gray-700 mb-4 flex items-center gap-2">
            <FiTrendingUp className="text-blue-500" /> Vote Distribution
          </h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={results} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="dish_name" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip formatter={(v) => [v, "Votes"]} />
              <Bar dataKey="vote_count" radius={[4, 4, 0, 0]}>
                {results.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Results list */}
      <div className="card mb-6">
        <h3 className="text-sm font-semibold text-gray-700 mb-4">All Options</h3>
        <div className="space-y-3">
          {results.map((opt, i) => (
            <div key={opt.id} className={`relative overflow-hidden rounded-lg border p-3 ${
              user_voted_option_id === opt.id ? "border-blue-300 bg-blue-50" : "border-gray-200 bg-gray-50"
            }`}>
              <div
                className="absolute inset-0 opacity-10"
                style={{ width: `${opt.percentage}%`, backgroundColor: COLORS[i % COLORS.length] }}
              />
              <div className="relative flex items-center justify-between">
                <div className="flex items-center gap-2">
                  {i === 0 && total_votes > 0 && <span className="text-sm">🥇</span>}
                  {i === 1 && total_votes > 0 && <span className="text-sm">🥈</span>}
                  {i === 2 && total_votes > 0 && <span className="text-sm">🥉</span>}
                  <span className="font-medium text-sm text-gray-900">{opt.dish_name}</span>
                  {user_voted_option_id === opt.id && (
                    <span className="text-xs text-blue-600 font-medium">← Your vote</span>
                  )}
                </div>
                <div className="text-right">
                  <span className="font-bold text-gray-900 text-sm">{opt.vote_count}</span>
                  <span className="text-gray-500 text-xs ml-1">({opt.percentage}%)</span>
                </div>
              </div>
            </div>
          ))}
          {results.length === 0 && (
            <p className="text-gray-500 text-sm text-center py-4">No votes yet.</p>
          )}
        </div>
      </div>

      {/* Feedback section — only after deadline, only for students */}
      {deadlinePassed && !isAdmin && (
        <div className="mb-6">
          {myFeedback ? (
            <div className="card bg-green-50 border border-green-200">
              <p className="text-sm font-medium text-green-800 mb-2">Your Feedback</p>
              <div className="flex items-center gap-1 mb-1">
                {[1,2,3,4,5].map((s) => (
                  <span key={s} className={`text-lg ${s <= myFeedback.rating ? "text-amber-400" : "text-gray-300"}`}>★</span>
                ))}
              </div>
              {myFeedback.comment && (
                <p className="text-sm text-gray-700 mt-1">"{myFeedback.comment}"</p>
              )}
            </div>
          ) : !feedbackSubmitted ? (
            <FeedbackForm menuId={menu.id} onSubmitted={() => setFeedbackSubmitted(true)} />
          ) : null}
        </div>
      )}
    </div>
  );
};

// ---- List of all menus ----
const ResultsList = () => {
  const [menus, setMenus] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/menus").then(({ data }) => {
      setMenus([...data.menus].reverse());
    }).catch((err) => {
      toast.error(getErrorMessage(err));
    }).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="max-w-2xl mx-auto px-4 py-8"><CardLoader count={5} /></div>;

  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Voting Results</h1>
      <div className="space-y-3">
        {menus.map((menu) => (
          <Link
            key={menu.id}
            to={`/results/${menu.id}`}
            className="card flex items-center justify-between hover:shadow-md transition-shadow group"
          >
            <div className="flex items-center gap-3">
              <span className="text-xl">{getMealIcon(menu.meal_type)}</span>
              <div>
                <p className="font-medium text-gray-900 group-hover:text-blue-600 transition-colors">
                  {formatDate(menu.date, "EEEE, MMM d")}
                </p>
                <p className="text-sm text-gray-500 capitalize">{menu.meal_type}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className={`badge border ${getMealColor(menu.meal_type)}`}>
                {capitalize(menu.meal_type)}
              </span>
              {menu.is_locked && <span className="badge bg-red-100 text-red-700">Locked</span>}
              <span className="text-gray-400 group-hover:text-blue-500 transition-colors">→</span>
            </div>
          </Link>
        ))}
        {menus.length === 0 && (
          <div className="card text-center py-12">
            <p className="text-gray-500">No menus available yet.</p>
          </div>
        )}
      </div>
    </div>
  );
};

// ---- Router ----
const ResultsPage = () => {
  const { menu_id } = useParams();
  return menu_id ? <ResultDetail menuId={menu_id} /> : <ResultsList />;
};

export default ResultsPage;
