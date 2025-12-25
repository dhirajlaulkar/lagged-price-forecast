"use client";

import React, { useEffect, useState } from 'react';
import MetricCard from '../components/MetricCard';
import PriceChart from '../components/PriceChart';
import { Activity, AlertCircle, TrendingUp } from 'lucide-react';

export default function Dashboard() {
  const [metrics, setMetrics] = useState<any>(null);
  const [predictions, setPredictions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [metricsRes, predsRes] = await Promise.all([
          fetch('http://localhost:8000/metrics'),
          fetch('http://localhost:8000/predictions')
        ]);

        if (!metricsRes.ok || !predsRes.ok) throw new Error("Failed to fetch data from backend API");

        const metricsData = await metricsRes.json();
        const predsData = await predsRes.json();

        setMetrics(metricsData);
        setPredictions(predsData);
      } catch (err) {
        setError("Error connecting to backend API. Ensure api.py is running on port 8000.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return (
    <div className="min-h-screen bg-yellow-50 flex items-center justify-center">
      <div className="text-2xl font-black font-mono animate-pulse">LOADING MARKET DATA...</div>
    </div>
  );

  if (error) return (
    <div className="min-h-screen bg-yellow-50 flex items-center justify-center p-4">
      <div className="bg-red-100 border-2 border-red-500 text-red-700 p-6 rounded-lg max-w-lg shadow-[4px_4px_0px_0px_rgba(239,68,68,1)]">
        <h2 className="text-xl font-bold mb-2 flex items-center gap-2">
          <AlertCircle className="w-6 h-6" /> System Error
        </h2>
        <p className="font-mono">{error}</p>
      </div>
    </div>
  );

  return (
    <main className="min-h-screen bg-[#f0f0f0] p-4 md:p-8 font-mono">
      <header className="mb-8 border-b-4 border-black pb-4">
        <h1 className="text-4xl md:text-5xl font-black uppercase tracking-tighter text-black flex items-center gap-4">
          <Activity className="w-10 h-10 md:w-12 md:h-12" />
          Lagged Price Forecast
        </h1>
        <p className="text-gray-600 mt-2 font-bold pl-1">
          Predicting Stock Movement based on Previous Day Data
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <MetricCard
          title="Model Accuracy (R²)"
          value={`${(metrics.metrics.r2 * 100).toFixed(1)}%`}
          subtext="Variance explained by the model"
          trend={metrics.metrics.r2 > 0.5 ? 'up' : 'neutral'}
          color="bg-blue-100"
        />
        <MetricCard
          title="Mean Squared Error"
          value={metrics.metrics.mse.toFixed(2)}
          subtext="Average squared difference"
          color="bg-pink-100"
        />
        <MetricCard
          title="Directional Accuracy"
          value={`${metrics.metrics.directional_accuracy.toFixed(1)}%`}
          subtext="Correct trend predictions"
          trend={metrics.metrics.directional_accuracy > 50 ? 'up' : 'down'}
          color="bg-green-100"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

        <div className="lg:col-span-2 bg-white border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] rounded-lg p-6 h-[500px]">
          <h3 className="text-xl font-black uppercase mb-4 flex items-center gap-2">
            <TrendingUp className="w-6 h-6" /> Price Forecast
          </h3>
          <PriceChart data={predictions} />
        </div>

        <div className="space-y-6">

          <div className="bg-yellow-100 border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] rounded-lg p-6">
            <h3 className="text-xl font-black uppercase mb-4 border-b-2 border-black pb-2">
              Model Insights
            </h3>
            <ul className="space-y-4">
              {metrics.insights.map((insight: string, idx: number) => (
                <li key={idx} className="flex items-start gap-3 text-sm font-bold text-gray-800">
                  <span className="bg-black text-white rounded-full w-6 h-6 flex items-center justify-center shrink-0 text-xs mt-0.5">
                    {idx + 1}
                  </span>
                  {insight}
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-white border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] rounded-lg p-6">
            <h3 className="text-lg font-black uppercase mb-4">Feature Importance</h3>
            <div className="space-y-3">
              {metrics.coefficients.map((c: any) => (
                <div key={c.Feature} className="bg-gray-50 p-3 border border-gray-200 rounded">
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-xs font-bold uppercase text-gray-500">{c.Feature}</span>
                    <span className={`text-sm font-black ${c.Coefficient > 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {c.Coefficient > 0 ? '+' : ''}{c.Coefficient.toFixed(4)}
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 h-2 rounded-full overflow-hidden mb-2">
                    <div
                      className={`h-full ${c.Coefficient > 0 ? 'bg-green-500' : 'bg-red-500'}`}
                      style={{ width: `${Math.min(Math.abs(c.Coefficient) * 20, 100)}%` }} // Rough scaling for visual
                    ></div>
                  </div>
                  {c.Explanation && (
                    <p className="text-xs text-gray-600 italic">
                      {c.Explanation}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>
    </main>
  );
}
