/**
 * VoteModal — cast or change a vote on a menu.
 * Pre-selects the existing vote when changing (US-12).
 */
import React, { useState } from "react";
import { FiX } from "react-icons/fi";
import VoteButton from "./VoteButton";
import { getMealIcon, capitalize, formatDate } from "../utils/helpers";
import { Spinner } from "./Loader";

const VoteModal = ({ menu, existingVoteOptionId, onClose, onSubmit, loading }) => {
  // Pre-select existing vote if changing (US-12)
  const initialOption = existingVoteOptionId
    ? menu.options?.find((o) => o.id === existingVoteOptionId) ?? null
    : null;

  const [selectedOption, setSelectedOption] = useState(initialOption);
  const isChanging = existingVoteOptionId != null;

  const handleSubmit = () => {
    if (!selectedOption) return;
    onSubmit(menu.id, selectedOption.id);
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
      onClick={(e) => e.target === e.currentTarget && onClose()}
      role="dialog"
      aria-modal="true"
      aria-labelledby="vote-modal-title"
    >
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-100">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xl">{getMealIcon(menu.meal_type)}</span>
              <h2 id="vote-modal-title" className="text-lg font-semibold text-gray-900">
                {isChanging ? "Change Vote" : "Vote"} for {capitalize(menu.meal_type)}
              </h2>
            </div>
            <p className="text-sm text-gray-500">{formatDate(menu.date, "EEEE, MMMM d, yyyy")}</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition-colors"
            aria-label="Close"
          >
            <FiX size={18} />
          </button>
        </div>

        {/* Options */}
        <div className="p-6 space-y-3">
          {isChanging && (
            <div className="p-3 bg-amber-50 border border-amber-200 rounded-lg text-sm text-amber-800 mb-2">
              You already voted. Select a different dish to change your vote.
            </div>
          )}
          {!isChanging && (
            <p className="text-sm text-gray-600 mb-2">
              Select your preferred dish. You can change your vote before the deadline.
            </p>
          )}
          {menu.options?.map((opt) => (
            <VoteButton
              key={opt.id}
              dish={opt}
              isSelected={selectedOption?.id === opt.id}
              onSelect={setSelectedOption}
              disabled={loading}
            />
          ))}
        </div>

        {/* Footer */}
        <div className="flex gap-3 p-6 pt-0">
          <button onClick={onClose} className="btn-secondary flex-1" disabled={loading}>
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={!selectedOption || loading || selectedOption?.id === existingVoteOptionId}
            className="btn-primary flex-1 flex items-center justify-center gap-2"
            data-testid="vote-modal-submit"
          >
            {loading ? (
              <><Spinner size="sm" /> Submitting...</>
            ) : isChanging ? (
              "Update Vote"
            ) : (
              "Submit Vote"
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default VoteModal;
