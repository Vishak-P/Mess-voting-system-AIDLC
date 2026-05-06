/**
 * Utility helper functions.
 */
import { format, parseISO, isAfter } from "date-fns";

/**
 * Format a date string to a readable format.
 * @param {string} dateStr - ISO date string
 * @param {string} fmt - date-fns format string
 */
export const formatDate = (dateStr, fmt = "MMM d, yyyy") => {
  try {
    return format(parseISO(dateStr), fmt);
  } catch {
    return dateStr;
  }
};

/**
 * Format a datetime string.
 */
export const formatDateTime = (dateStr) => {
  try {
    return format(parseISO(dateStr), "MMM d, yyyy h:mm a");
  } catch {
    return dateStr;
  }
};

/**
 * Check if a deadline has passed.
 */
export const isDeadlinePassed = (deadline) => {
  try {
    return !isAfter(parseISO(deadline), new Date());
  } catch {
    return false;
  }
};

/**
 * Get meal type icon.
 */
export const getMealIcon = (mealType) => {
  const icons = {
    breakfast: "🌅",
    lunch: "☀️",
    dinner: "🌙",
  };
  return icons[mealType] || "🍽️";
};

/**
 * Get meal type color classes.
 */
export const getMealColor = (mealType) => {
  const colors = {
    breakfast: "bg-amber-100 text-amber-800 border-amber-200",
    lunch: "bg-blue-100 text-blue-800 border-blue-200",
    dinner: "bg-purple-100 text-purple-800 border-purple-200",
  };
  return colors[mealType] || "bg-gray-100 text-gray-800";
};

/**
 * Capitalize first letter.
 */
export const capitalize = (str) =>
  str ? str.charAt(0).toUpperCase() + str.slice(1) : "";

/**
 * Get error message from axios error.
 */
export const getErrorMessage = (error) => {
  return (
    error?.response?.data?.error ||
    error?.response?.data?.message ||
    error?.message ||
    "Something went wrong"
  );
};

/**
 * Group menus by date.
 */
export const groupMenusByDate = (menus) => {
  return menus.reduce((acc, menu) => {
    const date = menu.date;
    if (!acc[date]) acc[date] = [];
    acc[date].push(menu);
    return acc;
  }, {});
};

/**
 * Sort meal types in order: breakfast, lunch, dinner.
 */
export const sortMeals = (meals) => {
  const order = { breakfast: 0, lunch: 1, dinner: 2 };
  return [...meals].sort((a, b) => order[a.meal_type] - order[b.meal_type]);
};
