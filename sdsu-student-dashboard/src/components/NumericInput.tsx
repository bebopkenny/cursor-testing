'use client';

import React, { useState } from 'react';
import { NumericInputProps } from '@/types';

const NumericInput: React.FC<NumericInputProps> = ({
  label,
  question,
  value,
  onChange,
  min = 1,
  max = 5,
  disabled = false,
}) => {
  const [error, setError] = useState<string>('');
  const [touched, setTouched] = useState<boolean>(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = parseInt(e.target.value);
    setTouched(true);

    // Validation
    if (isNaN(newValue)) {
      setError('Please enter a valid number');
      return;
    }

    if (newValue < min || newValue > max) {
      setError(`Please enter a value between ${min} and ${max}`);
      return;
    }

    setError('');
    onChange(newValue);
  };

  const handleBlur = () => {
    setTouched(true);
  };

  const isValid = !error && value >= min && value <= max;
  const showError = touched && error;

  return (
    <div className="flex flex-col space-y-3 p-4 bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200">
      {/* Label and Question */}
      <div className="space-y-1">
        <label className="block text-sm font-semibold text-gray-700">
          {label}
        </label>
        <p className="text-sm text-gray-600 leading-relaxed">
          {question}
        </p>
      </div>

      {/* Input with scale indicators */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
          <span>Strongly Disagree ({min})</span>
          <span>Strongly Agree ({max})</span>
        </div>
        
        <input
          type="number"
          min={min}
          max={max}
          value={value || ''}
          onChange={handleChange}
          onBlur={handleBlur}
          disabled={disabled}
          className={`w-full px-4 py-3 text-center text-lg font-medium border-2 rounded-md transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 ${
            showError
              ? 'border-red-500 bg-red-50'
              : isValid && touched
              ? 'border-green-500 bg-green-50'
              : 'border-gray-300 bg-white hover:border-gray-400'
          } ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
          placeholder={`${min}-${max}`}
        />

        {/* Scale visualization */}
        <div className="flex justify-between items-center">
          {Array.from({ length: max - min + 1 }, (_, i) => min + i).map((num) => (
            <button
              key={num}
              type="button"
              onClick={() => !disabled && onChange(num)}
              disabled={disabled}
              className={`w-8 h-8 rounded-full text-sm font-medium transition-all duration-200 ${
                value === num
                  ? 'bg-blue-500 text-white shadow-md'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              } ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
            >
              {num}
            </button>
          ))}
        </div>
      </div>

      {/* Error message */}
      {showError && (
        <div className="flex items-center space-x-2 text-red-600">
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          <span className="text-sm">{error}</span>
        </div>
      )}

      {/* Success indicator */}
      {isValid && touched && !error && (
        <div className="flex items-center space-x-2 text-green-600">
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
          <span className="text-sm">Valid response</span>
        </div>
      )}
    </div>
  );
};

export default NumericInput;