/**
 * Loading spinner components.
 */
import React from "react";

export const Spinner = ({ size = "md", className = "" }) => {
  const sizes = { sm: "w-4 h-4", md: "w-8 h-8", lg: "w-12 h-12" };
  return (
    <div
      className={`${sizes[size]} border-2 border-blue-200 border-t-blue-600 rounded-full animate-spin ${className}`}
      role="status"
      aria-label="Loading"
    />
  );
};

export const PageLoader = () => (
  <div className="min-h-screen flex items-center justify-center bg-gray-50">
    <div className="text-center">
      <Spinner size="lg" className="mx-auto mb-4" />
      <p className="text-gray-500 text-sm">Loading...</p>
    </div>
  </div>
);

export const CardLoader = ({ count = 3 }) => (
  <div className="space-y-4">
    {Array.from({ length: count }).map((_, i) => (
      <div key={i} className="card animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-1/3 mb-3" />
        <div className="h-3 bg-gray-200 rounded w-2/3 mb-2" />
        <div className="h-3 bg-gray-200 rounded w-1/2" />
      </div>
    ))}
  </div>
);

export default Spinner;
