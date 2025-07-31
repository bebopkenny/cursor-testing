import pandas as pd
import numpy as np
from typing import Dict, List
import random

class StudentDataGenerator:
    """Generates dummy student data that mimics spreadsheet format"""
    
    def __init__(self, num_students: int = 100):
        self.num_students = num_students
        self.subjects = [
            'Mathematics', 'Science', 'English', 'History', 
            'Chemistry', 'Physics', 'Biology', 'Computer Science'
        ]
        self.grade_levels = ['9th', '10th', '11th', '12th']
        
    def generate_student_data(self) -> pd.DataFrame:
        """Generate comprehensive student data"""
        np.random.seed(42)  # For reproducible results
        
        data = []
        for i in range(self.num_students):
            student = {
                'student_id': f'STU{i+1:04d}',
                'name': f'Student_{i+1}',
                'grade_level': random.choice(self.grade_levels),
                'age': random.randint(14, 19),
                'attendance_rate': round(random.uniform(0.7, 1.0), 2),
                'previous_gpa': round(random.uniform(2.0, 4.0), 2),
                'study_hours_per_week': random.randint(5, 30),
                'extracurricular_activities': random.randint(0, 5),
                'parent_education_level': random.choice(['High School', 'Bachelor', 'Master', 'PhD']),
                'socioeconomic_status': random.choice(['Low', 'Medium', 'High']),
            }
            
            # Add subject-specific grades
            for subject in self.subjects:
                student[f'{subject.lower().replace(" ", "_")}_grade'] = round(random.uniform(60, 100), 1)
                student[f'{subject.lower().replace(" ", "_")}_assignments_completed'] = random.randint(15, 25)
            
            data.append(student)
        
        return pd.DataFrame(data)
    
    def save_to_excel(self, df: pd.DataFrame, filename: str = 'student_data.xlsx'):
        """Save data to Excel file to mimic spreadsheet source"""
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Student_Data', index=False)
            
            # Get the workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Student_Data']
            
            # Add some formatting
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            
            # Write the column headers with formatting
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                
            # Auto-adjust column width
            for i, col in enumerate(df.columns):
                column_len = max(df[col].astype(str).str.len().max(), len(col) + 2)
                worksheet.set_column(i, i, min(column_len, 50))
        
        print(f"Student data saved to {filename}")
        return filename
    
    def get_sample_student_features(self, student_data: pd.DataFrame, student_id: str) -> Dict:
        """Extract features for a specific student for LLM prediction"""
        student = student_data[student_data['student_id'] == student_id].iloc[0]
        
        # Calculate average performance across all subjects
        subject_grades = []
        for subject in self.subjects:
            grade_col = f'{subject.lower().replace(" ", "_")}_grade'
            if grade_col in student_data.columns:
                subject_grades.append(student[grade_col])
        
        avg_grade = np.mean(subject_grades)
        
        features = {
            'student_id': student['student_id'],
            'name': student['name'],
            'grade_level': student['grade_level'],
            'age': student['age'],
            'attendance_rate': student['attendance_rate'],
            'previous_gpa': student['previous_gpa'],
            'study_hours_per_week': student['study_hours_per_week'],
            'extracurricular_activities': student['extracurricular_activities'],
            'parent_education_level': student['parent_education_level'],
            'socioeconomic_status': student['socioeconomic_status'],
            'current_average_grade': round(avg_grade, 2),
            'total_assignments_completed': sum([student[f'{subject.lower().replace(" ", "_")}_assignments_completed'] for subject in self.subjects])
        }
        
        return features

if __name__ == "__main__":
    # Generate sample data
    generator = StudentDataGenerator(50)
    student_df = generator.generate_student_data()
    
    # Save to Excel
    generator.save_to_excel(student_df)
    
    # Display sample
    print("\nSample Student Data:")
    print(student_df.head())
    
    # Show sample features for LLM
    sample_features = generator.get_sample_student_features(student_df, 'STU0001')
    print(f"\nSample features for {sample_features['student_id']}:")
    for key, value in sample_features.items():
        print(f"  {key}: {value}")