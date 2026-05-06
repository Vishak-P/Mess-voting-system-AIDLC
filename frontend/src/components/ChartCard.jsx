/**
 * ChartCard - wrapper card for Recharts charts with title and optional subtitle.
 */
import React from "react";

const ChartCard = ({ title, subtitle, children, className = "" }) => {
  return (
    <div className={`card ${className}`}>
      <div className="mb-4">
        <h3 className="text-base font-semibold text-gray-900">{title}</h3>
        {subtitle && <p className="text-sm text-gray-500 mt-0.5">{subtitle}</p>}
      </div>
      <div className="w-full">{children}</div>
    </div>
  );
};

export default ChartCard;
