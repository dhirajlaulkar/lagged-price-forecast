import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtext?: string;
  trend?: 'up' | 'down' | 'neutral';
  color?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, subtext, trend, color = "bg-white" }) => {
  return (
    <div className={`${color} border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] p-6 rounded-lg`}>
      <h3 className="text-sm font-bold uppercase tracking-wider text-gray-600 mb-2">{title}</h3>
      <div className="flex items-end justify-between">
        <div className="text-3xl font-black text-black">
          {value}
        </div>
        {trend && (
          <div className="flex items-center">
            {trend === 'up' && <TrendingUp className="w-6 h-6 text-green-600" />}
            {trend === 'down' && <TrendingDown className="w-6 h-6 text-red-600" />}
            {trend === 'neutral' && <Minus className="w-6 h-6 text-gray-600" />}
          </div>
        )}
      </div>
      {subtext && <p className="text-sm font-medium text-gray-500 mt-2">{subtext}</p>}
    </div>
  );
};

export default MetricCard;
