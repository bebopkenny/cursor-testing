'use client';

import React from 'react';
import { Pie, Bar, Doughnut } from 'react-chartjs-2';
import { ChartComponentProps } from '@/types';
import { pieChartOptions, barChartOptions, chartColors } from './ChartConfig';

const SurveyChart: React.FC<ChartComponentProps> = ({
  title,
  data,
  type = 'pie',
}) => {
  // Ensure colors are applied to the data
  const chartData = {
    ...data,
    datasets: data.datasets.map((dataset) => ({
      ...dataset,
      backgroundColor: dataset.backgroundColor || chartColors.primary,
      borderColor: dataset.borderColor || '#ffffff',
      borderWidth: dataset.borderWidth || 2,
    })),
  };

  const renderChart = () => {
    switch (type) {
      case 'bar':
        return (
          <div className="h-64 md:h-80">
            <Bar data={chartData} options={barChartOptions} />
          </div>
        );
      case 'doughnut':
        return (
          <div className="h-64 md:h-80">
            <Doughnut data={chartData} options={pieChartOptions} />
          </div>
        );
      case 'pie':
      default:
        return (
          <div className="h-64 md:h-80">
            <Pie data={chartData} options={pieChartOptions} />
          </div>
        );
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 hover:shadow-lg transition-shadow duration-200">
      {/* Chart Title */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-2">{title}</h3>
        <div className="h-1 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full w-16"></div>
      </div>

      {/* Chart Container */}
      <div className="relative">
        {renderChart()}
      </div>

      {/* Data Summary */}
      <div className="mt-6 pt-4 border-t border-gray-100">
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {data.labels.map((label, index) => {
            const value = data.datasets[0]?.data[index] || 0;
            const total = data.datasets[0]?.data.reduce((sum, val) => sum + val, 0) || 1;
            const percentage = ((value / total) * 100).toFixed(1);
            const color = chartColors.primary[index % chartColors.primary.length];

            return (
              <div key={label} className="flex items-center space-x-2">
                <div
                  className="w-3 h-3 rounded-full flex-shrink-0"
                  style={{ backgroundColor: color }}
                ></div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-700 truncate">
                    {label}
                  </p>
                  <p className="text-xs text-gray-500">
                    {value} ({percentage}%)
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default SurveyChart;