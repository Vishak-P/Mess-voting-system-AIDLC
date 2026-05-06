/**
 * StatCard - summary statistic card for the dashboard.
 */
import React from "react";

const StatCard = ({ title, value, icon, color = "blue", trend }) => {
  const colorMap = {
    blue:   { bg: "bg-blue-50",   icon: "bg-blue-100 text-blue-600",   text: "text-blue-600" },
    green:  { bg: "bg-green-50",  icon: "bg-green-100 text-green-600",  text: "text-green-600" },
    amber:  { bg: "bg-amber-50",  icon: "bg-amber-100 text-amber-600",  text: "text-amber-600" },
    purple: { bg: "bg-purple-50", icon: "bg-purple-100 text-purple-600", text: "text-purple-600" },
  };
  const c = colorMap[color] || colorMap.blue;

  return (
    <div className={`card ${c.bg} border-0`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-1">{value ?? "—"}</p>
          {trend && (
            <p className={`text-xs mt-1 font-medium ${c.text}`}>{trend}</p>
          )}
        </div>
        <div className={`w-12 h-12 rounded-xl flex items-center justify-center text-xl ${c.icon}`}>
          {icon}
        </div>
      </div>
    </div>
  );
};

export default StatCard;
