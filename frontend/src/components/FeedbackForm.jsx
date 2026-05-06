/**
 * FeedbackForm — post-meal star rating + optional comment.
 * Shown on the ResultsPage after the voting deadline has passed.
 */
import React, { useState } from "react";
import api from "../utils/api";
import { getErrorMessage } from "../utils/helpers";
import { Spinner } from "./Loader";
import toast from "react-hot-toast";
import { FiStar } from "react-icons/fi";

const FeedbackForm = ({ menuId, onSubmitted }) => {
  const [rating, setRating] = useState(0);
  const [hovered, setHovered] = useState(0);
  const [comment, setComment] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!rating) { toast.error("Please select a star rating"); return; }
    setLoading(true);
    try {
      await api.post("/feedback", { menu_id: menuId, rating, comment: comment.trim() });
      toast.success("Feedback submitted! Thank you 🙏");
      setSubmitted(true);
      onSubmitted && onSubmitted();
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="card bg-green-50 border border-green-200 text-center py-6">
        <p className="text-2xl mb-2">✅</p>
        <p className="font-medium text-green-800">Feedback submitted!</p>
        <p className="text-sm text-green-600 mt-1">Thank you for your response.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 className="text-base font-semibold text-gray-900 mb-4">Rate this meal</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Star rating */}
        <div>
          <label className="label">Your Rating *</label>
          <div className="flex gap-1" role="group" aria-label="Star rating">
            {[1, 2, 3, 4, 5].map((star) => (
              <button
                key={star}
                type="button"
                onClick={() => setRating(star)}
                onMouseEnter={() => setHovered(star)}
                onMouseLeave={() => setHovered(0)}
                aria-label={`${star} star${star > 1 ? "s" : ""}`}
                aria-pressed={rating === star}
                className="text-2xl transition-transform hover:scale-110 focus:outline-none focus:ring-2 focus:ring-amber-400 rounded"
              >
                <FiStar
                  className={`${
                    star <= (hovered || rating)
                      ? "text-amber-400 fill-amber-400"
                      : "text-gray-300"
                  } transition-colors`}
                  size={28}
                />
              </button>
            ))}
            {rating > 0 && (
              <span className="ml-2 text-sm text-gray-600 self-center">
                {["", "Poor", "Fair", "Good", "Very Good", "Excellent"][rating]}
              </span>
            )}
          </div>
        </div>

        {/* Comment */}
        <div>
          <label className="label" htmlFor="feedback-comment">
            Comment <span className="text-gray-400 font-normal">(optional)</span>
          </label>
          <textarea
            id="feedback-comment"
            className="input resize-none"
            rows={3}
            maxLength={1000}
            placeholder="Share your thoughts about the meal..."
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            data-testid="feedback-comment-input"
          />
          <p className="text-xs text-gray-400 mt-1 text-right">{comment.length}/1000</p>
        </div>

        <button
          type="submit"
          disabled={!rating || loading}
          className="btn-primary w-full flex items-center justify-center gap-2"
          data-testid="feedback-submit-button"
        >
          {loading ? <><Spinner size="sm" /> Submitting...</> : "Submit Feedback"}
        </button>
      </form>
    </div>
  );
};

export default FeedbackForm;
