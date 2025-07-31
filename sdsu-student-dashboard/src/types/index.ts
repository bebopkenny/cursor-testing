// Survey response types
export interface SurveyResponse {
  mentalHealthRating: number;
  counselingServicesUsage: number;
  conflictAvoidance: number;
  senseOfBelonging: number;
  roomSwitchRequests: number;
}

// Chart data interface
export interface ChartData {
  labels: string[];
  datasets: {
    data: number[];
    backgroundColor: string[];
    borderColor?: string[];
    borderWidth?: number;
  }[];
}

// Survey category interface
export interface SurveyCategory {
  id: keyof SurveyResponse;
  label: string;
  question: string;
  description: string;
}

// Numeric input component props
export interface NumericInputProps {
  label: string;
  question: string;
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
  disabled?: boolean;
}

// Chart component props
export interface ChartComponentProps {
  title: string;
  data: ChartData;
  type?: 'pie' | 'bar' | 'doughnut';
}