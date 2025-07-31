import { SurveyResponse, ChartData, SurveyCategory } from '@/types';
import { chartColors } from '@/components/ChartConfig';

// Convert single rating to distribution data for visualization
export const convertRatingToChartData = (
  rating: number,
  total: number = 100
): ChartData => {
  // Simulate distribution based on the rating
  // This is a simplified approach - in real app, you'd have actual aggregated data
  const distributions = {
    1: { stronglyDisagree: 80, disagree: 15, neutral: 3, agree: 1, stronglyAgree: 1 },
    2: { stronglyDisagree: 45, disagree: 35, neutral: 15, agree: 3, stronglyAgree: 2 },
    3: { stronglyDisagree: 15, disagree: 20, neutral: 30, agree: 25, stronglyAgree: 10 },
    4: { stronglyDisagree: 5, disagree: 10, neutral: 15, agree: 40, stronglyAgree: 30 },
    5: { stronglyDisagree: 2, disagree: 3, neutral: 10, agree: 25, stronglyAgree: 60 },
  };

  const dist = distributions[rating as keyof typeof distributions] || distributions[3];

  return {
    labels: ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
    datasets: [
      {
        data: [
          Math.round((dist.stronglyDisagree * total) / 100),
          Math.round((dist.disagree * total) / 100),
          Math.round((dist.neutral * total) / 100),
          Math.round((dist.agree * total) / 100),
          Math.round((dist.stronglyAgree * total) / 100),
        ],
        backgroundColor: chartColors.primary,
      },
    ],
  };
};

// Convert all survey responses to chart data
export const convertSurveyToChartData = (responses: SurveyResponse): Record<keyof SurveyResponse, ChartData> => {
  return {
    mentalHealthRating: convertRatingToChartData(responses.mentalHealthRating),
    counselingServicesUsage: convertRatingToChartData(responses.counselingServicesUsage),
    conflictAvoidance: convertRatingToChartData(responses.conflictAvoidance),
    senseOfBelonging: convertRatingToChartData(responses.senseOfBelonging),
    roomSwitchRequests: convertRatingToChartData(responses.roomSwitchRequests),
  };
};

// Survey category definitions
export const surveyCategories: SurveyCategory[] = [
  {
    id: 'mentalHealthRating',
    label: 'Mental Health Rating',
    question: 'How would you rate your overall mental health and well-being?',
    description: 'Self-reported mental health status and general well-being assessment',
  },
  {
    id: 'counselingServicesUsage',
    label: 'Counseling Services Usage',
    question: 'How frequently do you utilize campus counseling and mental health services?',
    description: 'Usage frequency of campus mental health resources and support services',
  },
  {
    id: 'conflictAvoidance',
    label: 'Conflict Avoidance',
    question: 'How often do you avoid conflicts or difficult conversations with roommates?',
    description: 'Tendency to avoid interpersonal conflicts in living situations',
  },
  {
    id: 'senseOfBelonging',
    label: 'Sense of Belonging',
    question: 'How strong is your sense of belonging and connection to the campus community?',
    description: 'Feeling of integration and acceptance within the university environment',
  },
  {
    id: 'roomSwitchRequests',
    label: 'Room Switch Requests',
    question: 'How likely are you to request a room or roommate change this academic year?',
    description: 'Likelihood of requesting housing changes due to living situation issues',
  },
];

// Get rating description based on numeric value
export const getRatingDescription = (rating: number): string => {
  const descriptions = {
    1: 'Strongly Disagree / Very Poor',
    2: 'Disagree / Poor',
    3: 'Neutral / Average',
    4: 'Agree / Good',
    5: 'Strongly Agree / Excellent',
  };
  
  return descriptions[rating as keyof typeof descriptions] || 'No rating selected';
};

// Calculate overall satisfaction score
export const calculateOverallScore = (responses: SurveyResponse): number => {
  const values = Object.values(responses).filter(val => val > 0);
  if (values.length === 0) return 0;
  
  return Math.round((values.reduce((sum, val) => sum + val, 0) / values.length) * 100) / 100;
};

// Get satisfaction level based on score
export const getSatisfactionLevel = (score: number): {
  level: string;
  color: string;
  description: string;
} => {
  if (score >= 4.5) {
    return {
      level: 'Excellent',
      color: 'text-green-600',
      description: 'Outstanding experience with strong satisfaction across all areas',
    };
  } else if (score >= 3.5) {
    return {
      level: 'Good',
      color: 'text-blue-600',
      description: 'Generally positive experience with room for improvement',
    };
  } else if (score >= 2.5) {
    return {
      level: 'Average',
      color: 'text-yellow-600',
      description: 'Mixed experience with some challenges in key areas',
    };
  } else if (score >= 1.5) {
    return {
      level: 'Poor',
      color: 'text-orange-600',
      description: 'Significant challenges affecting overall experience',
    };
  } else {
    return {
      level: 'Critical',
      color: 'text-red-600',
      description: 'Serious concerns requiring immediate attention and support',
    };
  }
};