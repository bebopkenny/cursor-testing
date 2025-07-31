import boto3
import json
import logging
import time
from typing import Dict, List, Optional, Any
from sagemaker import Session
from sagemaker.huggingface import HuggingFaceModel
from sagemaker.predictor import Predictor
from sagemaker.serializers import JSONSerializer
from sagemaker.deserializers import JSONDeserializer
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SageMakerLLMClient:
    """Client for deploying and using LLMs on AWS SageMaker"""
    
    def __init__(self, region_name: str = 'us-east-1'):
        self.region_name = region_name
        self.session = Session()
        self.sm_client = boto3.client('sagemaker', region_name=region_name)
        self.runtime_client = boto3.client('sagemaker-runtime', region_name=region_name)
        self.role = self._get_or_create_role()
        self.endpoint_name = None
        self.predictor = None
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _get_or_create_role(self) -> str:
        """Get the SageMaker execution role"""
        try:
            # Try to get role from environment or use SageMaker default
            role = os.getenv('SAGEMAKER_ROLE')
            if role:
                return role
            
            # Use SageMaker session to get default role
            return self.session.get_execution_role()
        except Exception as e:
            self.logger.warning(f"Could not get execution role: {e}")
            # For demo purposes, return a placeholder
            return "arn:aws:iam::123456789012:role/SageMakerExecutionRole"
    
    def deploy_huggingface_model(self, 
                                model_id: str = "microsoft/DialoGPT-medium",
                                instance_type: str = "ml.g4dn.xlarge",
                                initial_instance_count: int = 1) -> str:
        """Deploy a HuggingFace model to SageMaker endpoint"""
        
        try:
            self.logger.info(f"Deploying model {model_id} to SageMaker...")
            
            # Create HuggingFace Model
            huggingface_model = HuggingFaceModel(
                transformers_version="4.26",
                pytorch_version="1.13",
                py_version="py39",
                env={
                    'HF_MODEL_ID': model_id,
                    'HF_TASK': 'text-generation'
                },
                role=self.role,
                sagemaker_session=self.session
            )
            
            # Generate unique endpoint name
            timestamp = int(time.time())
            self.endpoint_name = f"student-prediction-llm-{timestamp}"
            
            # Deploy model
            self.predictor = huggingface_model.deploy(
                initial_instance_count=initial_instance_count,
                instance_type=instance_type,
                endpoint_name=self.endpoint_name,
                serializer=JSONSerializer(),
                deserializer=JSONDeserializer()
            )
            
            self.logger.info(f"Model deployed successfully to endpoint: {self.endpoint_name}")
            return self.endpoint_name
            
        except Exception as e:
            self.logger.error(f"Failed to deploy model: {e}")
            # For demo purposes, create a mock endpoint
            self.endpoint_name = f"mock-student-prediction-llm-{int(time.time())}"
            self.logger.info(f"Using mock endpoint for demo: {self.endpoint_name}")
            return self.endpoint_name
    
    def predict_student_performance(self, student_features: Dict) -> Dict[str, Any]:
        """Use the LLM to predict student performance percentage"""
        
        # Create a structured prompt for the LLM
        prompt = self._create_prediction_prompt(student_features)
        
        try:
            if self.predictor:
                # Real SageMaker prediction
                response = self.predictor.predict({
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 100,
                        "temperature": 0.7,
                        "do_sample": True
                    }
                })
                
                # Extract prediction from response
                prediction_text = response[0].get('generated_text', '')
                performance_percentage = self._extract_percentage_from_response(prediction_text)
                
            else:
                # Mock prediction for demo
                performance_percentage = self._mock_prediction(student_features)
            
            # Create comprehensive response
            prediction_result = {
                'student_id': student_features['student_id'],
                'student_name': student_features['name'],
                'predicted_performance_percentage': performance_percentage,
                'confidence_score': self._calculate_confidence(student_features),
                'factors_analysis': self._analyze_factors(student_features),
                'recommendations': self._generate_recommendations(student_features, performance_percentage),
                'prompt_used': prompt
            }
            
            return prediction_result
            
        except Exception as e:
            self.logger.error(f"Prediction failed: {e}")
            # Return mock prediction on error
            return {
                'student_id': student_features['student_id'],
                'student_name': student_features['name'],
                'predicted_performance_percentage': self._mock_prediction(student_features),
                'confidence_score': 0.6,
                'factors_analysis': self._analyze_factors(student_features),
                'recommendations': ["Unable to generate recommendations due to prediction error"],
                'error': str(e)
            }
    
    def _create_prediction_prompt(self, student_features: Dict) -> str:
        """Create a structured prompt for student performance prediction"""
        
        prompt = f"""
You are an AI education analyst. Based on the following student data, predict their academic performance percentage for the next semester.

Student Information:
- ID: {student_features['student_id']}
- Name: {student_features['name']}
- Grade Level: {student_features['grade_level']}
- Age: {student_features['age']}
- Attendance Rate: {student_features['attendance_rate']}%
- Previous GPA: {student_features['previous_gpa']}
- Study Hours per Week: {student_features['study_hours_per_week']}
- Extracurricular Activities: {student_features['extracurricular_activities']}
- Parent Education Level: {student_features['parent_education_level']}
- Socioeconomic Status: {student_features['socioeconomic_status']}
- Current Average Grade: {student_features['current_average_grade']}%
- Total Assignments Completed: {student_features['total_assignments_completed']}

Please provide a predicted performance percentage (0-100%) for the next semester based on these factors.
Format your response as: "Predicted Performance: X%"
"""
        return prompt.strip()
    
    def _extract_percentage_from_response(self, response_text: str) -> float:
        """Extract percentage value from LLM response"""
        import re
        
        # Look for percentage pattern in response
        percentage_pattern = r'(\d+(?:\.\d+)?)\s*%'
        matches = re.findall(percentage_pattern, response_text)
        
        if matches:
            return float(matches[0])
        
        # If no percentage found, return a calculated estimate
        return self._mock_prediction({})
    
    def _mock_prediction(self, student_features: Dict) -> float:
        """Generate a mock prediction based on student features"""
        if not student_features:
            return 75.0
        
        # Simple algorithm based on key factors
        base_score = 50.0
        
        # Attendance impact (0-25 points)
        attendance_score = student_features.get('attendance_rate', 0.8) * 25
        
        # Previous GPA impact (0-25 points)
        gpa_score = (student_features.get('previous_gpa', 3.0) / 4.0) * 25
        
        # Study hours impact (0-20 points)
        study_hours = student_features.get('study_hours_per_week', 15)
        study_score = min(study_hours / 30.0 * 20, 20)
        
        # Current performance impact (0-30 points)
        current_grade = student_features.get('current_average_grade', 75)
        current_score = (current_grade / 100.0) * 30
        
        total_score = base_score + attendance_score + gpa_score + study_score + current_score
        
        # Ensure score is within bounds
        return max(0.0, min(100.0, round(total_score, 1)))
    
    def _calculate_confidence(self, student_features: Dict) -> float:
        """Calculate confidence score for the prediction"""
        confidence = 0.7  # Base confidence
        
        # Higher confidence with more complete data
        data_completeness = len([v for v in student_features.values() if v is not None]) / len(student_features)
        confidence += (data_completeness - 0.5) * 0.3
        
        return max(0.0, min(1.0, round(confidence, 2)))
    
    def _analyze_factors(self, student_features: Dict) -> List[str]:
        """Analyze key factors affecting student performance"""
        factors = []
        
        attendance = student_features.get('attendance_rate', 0)
        if attendance >= 0.9:
            factors.append("Excellent attendance rate supports strong performance")
        elif attendance < 0.8:
            factors.append("Low attendance rate may negatively impact performance")
        
        gpa = student_features.get('previous_gpa', 0)
        if gpa >= 3.5:
            factors.append("Strong academic history indicates continued success")
        elif gpa < 2.5:
            factors.append("Previous academic challenges may require additional support")
        
        study_hours = student_features.get('study_hours_per_week', 0)
        if study_hours >= 20:
            factors.append("High study time commitment shows dedication")
        elif study_hours < 10:
            factors.append("Limited study time may affect academic outcomes")
        
        return factors
    
    def _generate_recommendations(self, student_features: Dict, predicted_percentage: float) -> List[str]:
        """Generate recommendations based on prediction and features"""
        recommendations = []
        
        if predicted_percentage < 70:
            recommendations.append("Consider additional tutoring or academic support")
            recommendations.append("Increase study time and create a structured study schedule")
        
        attendance = student_features.get('attendance_rate', 1.0)
        if attendance < 0.85:
            recommendations.append("Focus on improving attendance rate")
        
        study_hours = student_features.get('study_hours_per_week', 15)
        if study_hours < 15:
            recommendations.append("Increase weekly study hours to at least 15-20 hours")
        
        if predicted_percentage >= 85:
            recommendations.append("Continue current study habits - excellent trajectory")
            recommendations.append("Consider advanced coursework or leadership opportunities")
        
        return recommendations
    
    def cleanup_endpoint(self):
        """Delete the SageMaker endpoint to avoid costs"""
        if self.endpoint_name and self.predictor:
            try:
                self.predictor.delete_endpoint()
                self.logger.info(f"Endpoint {self.endpoint_name} deleted successfully")
            except Exception as e:
                self.logger.error(f"Failed to delete endpoint: {e}")

if __name__ == "__main__":
    # Demo usage
    client = SageMakerLLMClient()
    
    # Sample student data
    sample_student = {
        'student_id': 'STU0001',
        'name': 'John Doe',
        'grade_level': '11th',
        'age': 16,
        'attendance_rate': 0.92,
        'previous_gpa': 3.5,
        'study_hours_per_week': 18,
        'extracurricular_activities': 2,
        'parent_education_level': 'Bachelor',
        'socioeconomic_status': 'Medium',
        'current_average_grade': 85.5,
        'total_assignments_completed': 156
    }
    
    # Make prediction
    result = client.predict_student_performance(sample_student)
    
    print("Student Performance Prediction:")
    print(f"Student: {result['student_name']} ({result['student_id']})")
    print(f"Predicted Performance: {result['predicted_performance_percentage']}%")
    print(f"Confidence Score: {result['confidence_score']}")
    print("\nKey Factors:")
    for factor in result['factors_analysis']:
        print(f"  - {factor}")
    print("\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  - {rec}")