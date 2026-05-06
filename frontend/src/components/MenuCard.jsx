/**
 * MenuCard — displays a single menu with dish options and voting actions.
 * Shows "Vote Now" when not voted, "Change Vote" when voted + window still open.
 */
import React from "react";
import { Link } from "react-router-dom";
import { getMealIcon, getMealColor, capitalize, formatDate, isDeadlinePassed } from "../utils/helpers";
import { FiClock, FiLock, FiCheckCircle, FiRefreshCw } from "react-icons/fi";

const MenuCard = ({ menu, userVotedOptionId, onVoteClick, showVoteButton = true }) => {
  const deadlinePassed = isDeadlinePassed(menu.deadline);
  const isLocked = menu.is_locked || deadlinePassed;
  const hasVoted = userVotedOptionId != null;
  const canChangeVote = hasVoted && !isLocked && menu.voting_open;

  return (
    <div className="card hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <span className="text-xl">{getMealIcon(menu.meal_type)}</span>
            <span className={`badge border ${getMealColor(menu.meal_type)}`}>
              {capitalize(menu.meal_type)}
            </span>
            {isLocked && (
              <span className="badge bg-red-100 text-red-700 border border-red-200 flex items-center gap-1">
                <FiLock size={10} /> Locked
              </span>
            )}
            {hasVoted && (
              <span className="badge bg-green-100 text-green-700 border border-green-200 flex items-center gap-1">
                <FiCheckCircle size={10} /> Voted
              </span>
            )}
          </div>
          <p className="text-lg font-semibold text-gray-900">
            {formatDate(menu.date, "EEEE, MMM d")}
          </p>
        </div>
        <div className="text-right text-xs text-gray-500 flex-shrink-0 ml-2">
          <div className="flex items-center gap-1 justify-end">
            <FiClock size={11} />
            <span>Deadline</span>
          </div>
          <p className="font-medium text-gray-700">
            {formatDate(menu.deadline, "MMM d, h:mm a")}
          </p>
        </div>
      </div>

      {/* Dish options */}
      <div className="space-y-2 mb-4">
        {menu.options?.map((opt) => (
          <div
            key={opt.id}
            className={`flex items-center justify-between px-3 py-2.5 rounded-lg border transition-colors ${
              userVotedOptionId === opt.id
                ? "bg-blue-50 border-blue-300"
                : "bg-gray-50 border-gray-200"
            }`}
          >
            <div className="flex items-center gap-2">
              {userVotedOptionId === opt.id && (
                <FiCheckCircle className="text-blue-600 flex-shrink-0" size={14} />
              )}
              <span className="text-sm font-medium text-gray-800">{opt.dish_name}</span>
            </div>
            {opt.vote_count !== undefined && (
              <span className="text-xs text-gray-500 font-medium">
                {opt.vote_count} votes
              </span>
            )}
          </div>
        ))}
      </div>

      {/* Actions */}
      <div className="flex items-center gap-2">
        {showVoteButton && !isLocked && !hasVoted && (
          <button
            onClick={() => onVoteClick && onVoteClick(menu, null)}
            className="btn-primary text-sm flex-1"
            data-testid={`vote-button-${menu.id}`}
          >
            Vote Now
          </button>
        )}
        {showVoteButton && canChangeVote && (
          <button
            onClick={() => onVoteClick && onVoteClick(menu, userVotedOptionId)}
            className="btn-secondary text-sm flex-1 flex items-center justify-center gap-1"
            data-testid={`change-vote-button-${menu.id}`}
          >
            <FiRefreshCw size={12} /> Change Vote
          </button>
        )}
        <Link
          to={`/results/${menu.id}`}
          className="btn-secondary text-sm flex-1 text-center"
        >
          Results
        </Link>
      </div>
    </div>
  );
};

export default MenuCard;
