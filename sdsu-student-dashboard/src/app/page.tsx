'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import NumericInput from '@/components/NumericInput';
import SurveyChart from '@/components/SurveyChart';
import { SurveyResponse, ChartData } from '@/types';
import {
  surveyCategories,
  convertSurveyToChartData,
  calculateOverallScore,
  getSatisfactionLevel,
  getRatingDescription,
} from '@/utils/surveyUtils';

export default function Dashboard() {
  const [responses, setResponses] = useState<SurveyResponse>({
    mentalHealthRating: 0,
    counselingServicesUsage: 0,
    conflictAvoidance: 0,
    senseOfBelonging: 0,
    roomSwitchRequests: 0,
  });

  const [showCharts, setShowCharts] = useState(false);
  const [chartData, setChartData] = useState<Record<keyof SurveyResponse, ChartData>>({} as Record<keyof SurveyResponse, ChartData>);

  // Update chart data when responses change
  useEffect(() => {
    const hasValidResponses = Object.values(responses).some(val => val > 0);
    if (hasValidResponses) {
      setChartData(convertSurveyToChartData(responses));
      setShowCharts(true);
    } else {
      setShowCharts(false);
    }
  }, [responses]);

  const handleResponseChange = (category: keyof SurveyResponse, value: number) => {
    setResponses(prev => ({
      ...prev,
      [category]: value,
    }));
  };

  const overallScore = calculateOverallScore(responses);
  const satisfactionLevel = getSatisfactionLevel(overallScore);
  const completedResponses = Object.values(responses).filter(val => val > 0).length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Navigation Header */}
      <header className="bg-white shadow-md border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  SDSU Student Experience Dashboard
                </h1>
                <p className="text-sm text-gray-600">Living Experiences & Mental Health Survey</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="hidden sm:block text-sm text-gray-600">
                Progress: {completedResponses}/5 completed
              </div>
              <div className="hidden sm:block w-24 h-2 bg-gray-200 rounded-full">
                <div 
                  className="h-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full transition-all duration-300"
                  style={{ width: `${(completedResponses / 5) * 100}%` }}
                ></div>
              </div>
              <Link 
                href="/login"
                className="text-sm text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md transition-colors duration-200"
              >
                Sign In
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Introduction Section */}
        <div className="mb-8 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Help Us Understand Your Experience
          </h2>
          <p className="text-gray-600 max-w-3xl mx-auto">
            Your responses will help SDSU improve student living experiences, mental health support, 
            and campus community building. Please rate each area on a scale from 1 to 5.
          </p>
        </div>

        {/* Overall Score Card */}
        {overallScore > 0 && (
          <div className="mb-8">
            <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
              <div className="text-center">
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Overall Experience Score</h3>
                <div className="flex items-center justify-center space-x-4">
                  <div className="text-4xl font-bold text-blue-600">{overallScore}</div>
                  <div className="text-left">
                    <div className={`text-lg font-semibold ${satisfactionLevel.color}`}>
                      {satisfactionLevel.level}
                    </div>
                    <div className="text-sm text-gray-600 max-w-xs">
                      {satisfactionLevel.description}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Survey Input Section */}
        <div className="mb-12">
          <h3 className="text-xl font-semibold text-gray-800 mb-6">Survey Questions</h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {surveyCategories.map((category) => (
              <NumericInput
                key={category.id}
                label={category.label}
                question={category.question}
                value={responses[category.id]}
                onChange={(value) => handleResponseChange(category.id, value)}
                min={1}
                max={5}
              />
            ))}
          </div>
        </div>

        {/* Response Summary */}
        {completedResponses > 0 && (
          <div className="mb-8">
            <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Your Responses Summary</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {surveyCategories.map((category) => {
                  const value = responses[category.id];
                  return (
                    <div key={category.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-700 truncate">
                          {category.label}
                        </p>
                        <p className="text-xs text-gray-500">
                          {value > 0 ? getRatingDescription(value) : 'Not answered'}
                        </p>
                      </div>
                      <div className={`text-lg font-bold px-3 py-1 rounded-full ${
                        value > 0 ? 'bg-blue-100 text-blue-700' : 'bg-gray-200 text-gray-500'
                      }`}>
                        {value > 0 ? value : '-'}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {/* Visualization Section */}
        {showCharts && (
          <div>
            <h3 className="text-xl font-semibold text-gray-800 mb-6">
              Data Visualization - Response Distribution
            </h3>
            <p className="text-gray-600 mb-8 text-center">
              These charts show how your responses compare to simulated student population distributions.
            </p>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
              {surveyCategories.map((category) => {
                const value = responses[category.id];
                if (value === 0) return null;

                return (
                  <SurveyChart
                    key={category.id}
                    title={`${category.label} (Your Rating: ${value})`}
                    data={chartData[category.id]}
                    type="pie"
                  />
                );
              })}
            </div>
          </div>
        )}

        {/* Call to Action */}
        {completedResponses === 0 && (
          <div className="text-center py-12">
            <div className="max-w-md mx-auto">
              <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Ready to Share Your Experience?
              </h3>
              <p className="text-gray-600">
                Start by answering any of the survey questions above to see your data visualized and contribute to improving student life at SDSU.
              </p>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-50 border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-sm text-gray-600">
            <p>&copy; 2024 San Diego State University Student Experience Dashboard</p>
            <p className="mt-1">
              Your privacy is important to us. All responses are anonymized and used solely for improving campus services.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
