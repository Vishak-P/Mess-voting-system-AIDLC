/**
 * VoteButton - a selectable dish option button used in the voting modal.
 */
import React from "react";
import { FiCheckCircle, FiCircle } from "react-icons/fi";

const VoteButton = ({ dish, isSelected, onSelect, disabled }) => {
  return (
    <button
      onClick={() => !disabled && onSelect(dish)}
      disabled={disabled}
      className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl border-2 text-left transition-all duration-150 ${
        isSelected
          ? "border-blue-500 bg-blue-50 shadow-sm"
          : "border-gray-200 bg-white hover:border-blue-300 hover:bg-blue-50/50"
      } ${disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
      aria-pressed={isSelected}
    >
      <span className={`flex-shrink-0 ${isSelected ? "text-blue-600" : "text-gray-400"}`}>
        {isSelected ? <FiCheckCircle size={20} /> : <FiCircle size={20} />}
      </span>
      <span className={`font-medium text-sm ${isSelected ? "text-blue-800" : "text-gray-700"}`}>
        {dish.dish_name}
      </span>
    </button>
  );
};

export default VoteButton;
