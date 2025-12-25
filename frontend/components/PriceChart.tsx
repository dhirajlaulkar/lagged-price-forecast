"use client";
import React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

interface PriceChartProps {
    data: any[]; // Array of objects with Date, Actual_Price, Predicted_Price
}

const PriceChart: React.FC<PriceChartProps> = ({ data }) => {
    // Assuming sorted data
    const labels = data.map(d => new Date(d.Date).toLocaleDateString());
    const actuals = data.map(d => d.Actual_Price);
    const predictions = data.map(d => d.Predicted_Price);

    const chartData = {
        labels,
        datasets: [
            {
                label: 'Actual Price',
                data: actuals,
                borderColor: '#000000',
                backgroundColor: '#000000',
                borderWidth: 2,
                tension: 0.1,
                pointRadius: 0,
                pointHoverRadius: 4
            },
            {
                label: 'Predicted Price',
                data: predictions,
                borderColor: '#FF5733',
                backgroundColor: '#FF5733',
                borderWidth: 2,
                borderDash: [5, 5], // Dashed line for prediction
                tension: 0.1,
                pointRadius: 0,
                pointHoverRadius: 4
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top' as const,
                labels: {
                    font: {
                        family: 'monospace',
                        weight: 'bold' as const
                    },
                    color: '#000'
                }
            },
            title: {
                display: false,
            },
            tooltip: {
                backgroundColor: '#000',
                titleFont: { family: 'monospace' },
                bodyFont: { family: 'monospace' },
                padding: 10,
                corderRadius: 0,
                displayColors: true,
            }
        },
        scales: {
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    font: { family: 'monospace' },
                    color: '#666'
                }
            },
            y: {
                grid: {
                    color: '#e5e7eb',
                    lineWidth: 1
                },
                border: {
                    dash: [4, 4]
                },
                ticks: {
                    font: { family: 'monospace' },
                    color: '#666'
                }
            }
        },
        interaction: {
            mode: 'index' as const,
            intersect: false,
        },
    };

    return <div className="h-full w-full"><Line options={options} data={chartData} /></div>;
};

export default PriceChart;
