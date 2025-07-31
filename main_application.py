#!/usr/bin/env python3
"""
Main application for Student Performance Prediction using AWS SageMaker LLM
This application demonstrates:
1. Loading student data from spreadsheet-like sources
2. Using AWS SageMaker to host an LLM
3. Predicting student performance percentages
4. Providing comprehensive analysis and recommendations
"""

import os
import sys
import pandas as pd
import json
from typing import Dict, List, Optional
import argparse
import time
from datetime import datetime

from student_data_generator import StudentDataGenerator
from sagemaker_llm_client import SageMakerLLMClient

class StudentPerformancePredictor:
    """Main application class for student performance prediction"""
    
    def __init__(self, use_real_sagemaker: bool = False):
        self.use_real_sagemaker = use_real_sagemaker
        self.data_generator = StudentDataGenerator()
        self.llm_client = SageMakerLLMClient()
        self.student_data = None
        self.results_history = []
        
    def load_student_data(self, source: str = "generate", file_path: Optional[str] = None, num_students: int = 20) -> pd.DataFrame:
        """Load student data from various sources"""
        print(f"\n📊 Loading student data...")
        
        if source == "generate":
            # Generate dummy data
            print(f"Generating {num_students} dummy student records...")
            self.data_generator = StudentDataGenerator(num_students)
            self.student_data = self.data_generator.generate_student_data()
            
            # Save to Excel for reference
            excel_file = self.data_generator.save_to_excel(self.student_data, "generated_student_data.xlsx")
            print(f"✅ Generated data saved to: {excel_file}")
            
        elif source == "excel" and file_path:
            # Load from existing Excel file
            print(f"Loading data from: {file_path}")
            self.student_data = pd.read_excel(file_path)
            print(f"✅ Loaded {len(self.student_data)} student records")
            
        else:
            raise ValueError("Invalid source. Use 'generate' or 'excel' with file_path")
        
        print(f"📈 Dataset shape: {self.student_data.shape}")
        print(f"📋 Columns: {list(self.student_data.columns)}")
        
        return self.student_data
    
    def setup_sagemaker_llm(self, deploy_model: bool = False) -> str:
        """Setup SageMaker LLM endpoint"""
        print(f"\n🤖 Setting up SageMaker LLM...")
        
        if deploy_model and self.use_real_sagemaker:
            print("🚀 Deploying model to SageMaker (this may take 5-10 minutes)...")
            endpoint_name = self.llm_client.deploy_huggingface_model(
                model_id="microsoft/DialoGPT-medium",
                instance_type="ml.g4dn.xlarge"
            )
            print(f"✅ Model deployed to endpoint: {endpoint_name}")
        else:
            print("🔧 Using mock LLM for demo purposes...")
            endpoint_name = "mock-endpoint-for-demo"
            
        return endpoint_name
    
    def predict_single_student(self, student_id: str) -> Dict:
        """Predict performance for a single student"""
        if self.student_data is None:
            raise ValueError("No student data loaded. Call load_student_data() first.")
        
        # Get student features
        student_features = self.data_generator.get_sample_student_features(self.student_data, student_id)
        
        print(f"\n🔍 Analyzing student: {student_features['name']} ({student_id})")
        print("📋 Student profile:")
        for key, value in student_features.items():
            if key not in ['student_id', 'name']:
                print(f"   {key.replace('_', ' ').title()}: {value}")
        
        # Make prediction using LLM
        print("\n🧠 Generating LLM prediction...")
        prediction_result = self.llm_client.predict_student_performance(student_features)
        
        # Store result
        prediction_result['timestamp'] = datetime.now().isoformat()
        self.results_history.append(prediction_result)
        
        return prediction_result
    
    def predict_batch_students(self, student_ids: List[str] = None, max_students: int = 5) -> List[Dict]:
        """Predict performance for multiple students"""
        if self.student_data is None:
            raise ValueError("No student data loaded. Call load_student_data() first.")
        
        if student_ids is None:
            # Select random students
            student_ids = self.student_data['student_id'].sample(min(max_students, len(self.student_data))).tolist()
        
        print(f"\n📊 Batch prediction for {len(student_ids)} students...")
        
        batch_results = []
        for i, student_id in enumerate(student_ids, 1):
            print(f"\n--- Student {i}/{len(student_ids)} ---")
            try:
                result = self.predict_single_student(student_id)
                batch_results.append(result)
                
                # Brief summary
                print(f"✅ Prediction: {result['predicted_performance_percentage']}% "
                      f"(Confidence: {result['confidence_score']})")
                
            except Exception as e:
                print(f"❌ Error predicting for {student_id}: {e}")
                continue
        
        return batch_results
    
    def display_prediction_results(self, result: Dict):
        """Display detailed prediction results"""
        print(f"\n" + "="*60)
        print(f"🎓 STUDENT PERFORMANCE PREDICTION REPORT")
        print(f"="*60)
        
        print(f"\n👤 Student Information:")
        print(f"   Name: {result['student_name']}")
        print(f"   ID: {result['student_id']}")
        
        print(f"\n📈 Prediction Results:")
        print(f"   Predicted Performance: {result['predicted_performance_percentage']}%")
        print(f"   Confidence Score: {result['confidence_score']}")
        
        print(f"\n🔍 Key Factors Analysis:")
        for factor in result['factors_analysis']:
            print(f"   • {factor}")
        
        print(f"\n💡 Recommendations:")
        for recommendation in result['recommendations']:
            print(f"   • {recommendation}")
        
        if 'error' in result:
            print(f"\n⚠️  Note: {result['error']}")
        
        print(f"\n" + "="*60)
    
    def save_results(self, results: List[Dict], filename: str = None):
        """Save prediction results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"student_predictions_{timestamp}.json"
        
        # Prepare data for JSON serialization
        json_results = []
        for result in results:
            json_result = result.copy()
            # Convert any non-serializable objects
            for key, value in json_result.items():
                if isinstance(value, pd.Timestamp):
                    json_result[key] = value.isoformat()
        
        with open(filename, 'w') as f:
            json.dump(json_results, f, indent=2, default=str)
        
        print(f"💾 Results saved to: {filename}")
        return filename
    
    def generate_summary_report(self, results: List[Dict]):
        """Generate a summary report of all predictions"""
        if not results:
            print("No results to summarize.")
            return
        
        print(f"\n" + "="*60)
        print(f"📊 BATCH PREDICTION SUMMARY REPORT")
        print(f"="*60)
        
        # Calculate statistics
        performances = [r['predicted_performance_percentage'] for r in results]
        confidences = [r['confidence_score'] for r in results]
        
        print(f"\n📈 Performance Statistics:")
        print(f"   Total Students: {len(results)}")
        print(f"   Average Predicted Performance: {sum(performances)/len(performances):.1f}%")
        print(f"   Highest Predicted Performance: {max(performances):.1f}%")
        print(f"   Lowest Predicted Performance: {min(performances):.1f}%")
        print(f"   Average Confidence: {sum(confidences)/len(confidences):.2f}")
        
        # Performance distribution
        high_performers = [r for r in results if r['predicted_performance_percentage'] >= 85]
        medium_performers = [r for r in results if 70 <= r['predicted_performance_percentage'] < 85]
        low_performers = [r for r in results if r['predicted_performance_percentage'] < 70]
        
        print(f"\n📊 Performance Distribution:")
        print(f"   High Performers (≥85%): {len(high_performers)} students")
        print(f"   Medium Performers (70-84%): {len(medium_performers)} students")
        print(f"   At-Risk Students (<70%): {len(low_performers)} students")
        
        # Top recommendations
        all_recommendations = []
        for result in results:
            all_recommendations.extend(result['recommendations'])
        
        # Count recommendation frequency
        rec_counts = {}
        for rec in all_recommendations:
            rec_counts[rec] = rec_counts.get(rec, 0) + 1
        
        print(f"\n💡 Most Common Recommendations:")
        sorted_recs = sorted(rec_counts.items(), key=lambda x: x[1], reverse=True)
        for rec, count in sorted_recs[:5]:
            print(f"   • {rec} ({count} students)")
        
        print(f"\n" + "="*60)
    
    def cleanup(self):
        """Cleanup resources"""
        print(f"\n🧹 Cleaning up resources...")
        if self.llm_client:
            self.llm_client.cleanup_endpoint()
        print("✅ Cleanup completed")

def main():
    """Main function to run the application"""
    parser = argparse.ArgumentParser(description="Student Performance Prediction using AWS SageMaker LLM")
    parser.add_argument("--students", type=int, default=10, help="Number of students to generate/analyze")
    parser.add_argument("--student-id", type=str, help="Specific student ID to analyze")
    parser.add_argument("--deploy-model", action="store_true", help="Deploy real SageMaker model (costs money)")
    parser.add_argument("--excel-file", type=str, help="Path to existing Excel file with student data")
    parser.add_argument("--save-results", action="store_true", help="Save results to JSON file")
    
    args = parser.parse_args()
    
    print("🎓 Student Performance Prediction System")
    print("=" * 50)
    
    # Initialize application
    app = StudentPerformancePredictor(use_real_sagemaker=args.deploy_model)
    
    try:
        # Load student data
        if args.excel_file:
            app.load_student_data(source="excel", file_path=args.excel_file)
        else:
            app.load_student_data(source="generate", num_students=args.students)
        
        # Setup SageMaker LLM
        app.setup_sagemaker_llm(deploy_model=args.deploy_model)
        
        # Make predictions
        if args.student_id:
            # Single student prediction
            result = app.predict_single_student(args.student_id)
            app.display_prediction_results(result)
            
            if args.save_results:
                app.save_results([result])
        else:
            # Batch prediction
            results = app.predict_batch_students(max_students=min(args.students, 10))
            
            # Display individual results
            for result in results:
                app.display_prediction_results(result)
            
            # Generate summary
            app.generate_summary_report(results)
            
            if args.save_results:
                app.save_results(results)
    
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
    except Exception as e:
        print(f"\n❌ Application error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        app.cleanup()

if __name__ == "__main__":
    main()