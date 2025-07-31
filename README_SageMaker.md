# Student Performance Prediction with AWS SageMaker LLM

This Python application demonstrates how to use AWS SageMaker to host an LLM for predicting student performance percentages based on spreadsheet-like data.

## 🎯 Overview

The application simulates a real-world scenario where:
1. **Student data** is loaded from spreadsheet sources (Excel files or generated dummy data)
2. **AWS SageMaker** hosts a Language Learning Model (LLM) 
3. The **LLM predicts student performance percentages** based on various factors
4. **Comprehensive analysis and recommendations** are provided

## 🏗️ Architecture

```
Student Data (Excel/CSV) → Python Application → AWS SageMaker LLM → Prediction Results
                                ↑                        ↓
                        Data Processing          Performance Analysis
                                                 & Recommendations
```

## 📁 Project Structure

```
.
├── main_application.py          # Main orchestration application
├── student_data_generator.py    # Generates dummy student data
├── sagemaker_llm_client.py     # AWS SageMaker client for LLM
├── requirements.txt             # Python dependencies
├── .env.example                # Environment variables template
├── README_SageMaker.md         # This documentation
└── generated_student_data.xlsx  # Generated sample data (created on run)
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- AWS Account with SageMaker access
- AWS CLI configured or IAM role with SageMaker permissions

### 2. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials (if not using IAM roles)
aws configure
```

### 3. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your AWS configuration
# At minimum, set your AWS region and SageMaker role
```

### 4. Run the Application

#### Demo Mode (No AWS Costs)
```bash
# Generate dummy data and run predictions with mock LLM
python main_application.py --students 5

# Analyze a specific student
python main_application.py --student-id STU0001

# Save results to JSON
python main_application.py --students 10 --save-results
```

#### Production Mode (Uses Real SageMaker - Costs Apply)
```bash
# Deploy real SageMaker model and make predictions
python main_application.py --deploy-model --students 3

# Use existing Excel file
python main_application.py --excel-file your_data.xlsx --deploy-model
```

## 📊 Sample Data Format

The application generates/expects student data with these columns:

| Column | Type | Description |
|--------|------|-------------|
| student_id | string | Unique identifier (e.g., STU0001) |
| name | string | Student name |
| grade_level | string | Grade level (9th, 10th, 11th, 12th) |
| age | integer | Student age |
| attendance_rate | float | Attendance rate (0.0-1.0) |
| previous_gpa | float | Previous GPA (0.0-4.0) |
| study_hours_per_week | integer | Weekly study hours |
| extracurricular_activities | integer | Number of activities |
| parent_education_level | string | Education level |
| socioeconomic_status | string | Low/Medium/High |
| [subject]_grade | float | Grade in specific subject |
| [subject]_assignments_completed | integer | Assignments completed |

## 🧠 LLM Integration

### Model Selection
- **Default**: Microsoft DialoGPT-medium (good for demonstrations)
- **Alternatives**: Any HuggingFace text-generation model
- **Instance**: ml.g4dn.xlarge (GPU instance for better performance)

### Prediction Process
1. **Feature Extraction**: Relevant student attributes are extracted
2. **Prompt Creation**: Structured prompt is created for the LLM
3. **LLM Inference**: Model generates performance prediction
4. **Response Parsing**: Percentage is extracted from LLM response
5. **Analysis**: Additional factors and recommendations are generated

### Sample LLM Prompt
```
You are an AI education analyst. Based on the following student data, 
predict their academic performance percentage for the next semester.

Student Information:
- ID: STU0001
- Name: John Doe
- Grade Level: 11th
- Age: 16
- Attendance Rate: 92%
- Previous GPA: 3.5
- Study Hours per Week: 18
- Current Average Grade: 85.5%
...

Please provide a predicted performance percentage (0-100%) for the next semester.
Format your response as: "Predicted Performance: X%"
```

## 💰 Cost Considerations

### SageMaker Costs
- **Model Deployment**: ~$1-3/hour for ml.g4dn.xlarge instance
- **Inference**: ~$0.001-0.01 per prediction
- **Storage**: Minimal S3 costs for model artifacts

### Cost Optimization
- Use demo mode for development/testing
- Delete endpoints when not in use
- Consider smaller instances for testing
- Batch predictions to reduce overhead

## 🔧 Configuration Options

### Command Line Arguments
```bash
python main_application.py [OPTIONS]

Options:
  --students N           Number of students to generate/analyze (default: 10)
  --student-id ID        Analyze specific student ID
  --deploy-model         Deploy real SageMaker model (costs money)
  --excel-file PATH      Use existing Excel file
  --save-results         Save results to JSON file
```

### Environment Variables
```bash
# AWS Configuration
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=us-east-1
SAGEMAKER_ROLE=arn:aws:iam::ACCOUNT:role/SageMakerExecutionRole

# Application Settings
LOG_LEVEL=INFO
MAX_STUDENTS_PER_BATCH=10
```

## 📈 Sample Output

```
🎓 Student Performance Prediction System
==================================================

📊 Loading student data...
Generating 5 dummy student records...
✅ Generated data saved to: generated_student_data.xlsx

🤖 Setting up SageMaker LLM...
🔧 Using mock LLM for demo purposes...

📊 Batch prediction for 5 students...

--- Student 1/5 ---
🔍 Analyzing student: Student_1 (STU0001)
📋 Student profile:
   Grade Level: 11th
   Age: 16
   Attendance Rate: 0.92
   Previous Gpa: 3.5
   ...

🧠 Generating LLM prediction...
✅ Prediction: 87.2% (Confidence: 0.85)

============================================================
🎓 STUDENT PERFORMANCE PREDICTION REPORT
============================================================

👤 Student Information:
   Name: Student_1
   ID: STU0001

📈 Prediction Results:
   Predicted Performance: 87.2%
   Confidence Score: 0.85

🔍 Key Factors Analysis:
   • Excellent attendance rate supports strong performance
   • Strong academic history indicates continued success
   • High study time commitment shows dedication

💡 Recommendations:
   • Continue current study habits - excellent trajectory
   • Consider advanced coursework or leadership opportunities
```

## 🛠️ Customization

### Adding New Features
1. **Extend StudentDataGenerator**: Add new student attributes
2. **Modify LLM Prompts**: Enhance prediction prompts in `sagemaker_llm_client.py`
3. **Custom Analysis**: Add new factors in `_analyze_factors()` method
4. **Different Models**: Change model_id in deployment configuration

### Integration with Real Data
```python
# Load from your existing Excel/CSV files
app = StudentPerformancePredictor()
app.load_student_data(source="excel", file_path="your_students.xlsx")
```

## 🔍 Troubleshooting

### Common Issues

1. **AWS Permission Errors**
   ```bash
   # Ensure your AWS credentials have SageMaker permissions
   aws sts get-caller-identity
   ```

2. **Model Deployment Failures**
   ```python
   # Check SageMaker service limits and quotas
   # Use smaller instance types if needed
   ```

3. **Excel File Issues**
   ```bash
   # Ensure Excel files have proper column names
   # Check for missing or null values
   ```

### Debug Mode
```bash
# Enable detailed logging
export LOG_LEVEL=DEBUG
python main_application.py --students 1
```

## 🚧 Future Enhancements

- [ ] Real-time inference API
- [ ] Web dashboard for visualization
- [ ] Integration with learning management systems
- [ ] Advanced ML models (beyond LLMs)
- [ ] Historical trend analysis
- [ ] Multi-semester predictions

## 📝 License

This project is for educational/demonstration purposes. Please ensure compliance with your organization's data privacy and AWS usage policies.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## 📞 Support

For AWS SageMaker specific issues, refer to:
- [AWS SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/)
- [SageMaker Python SDK](https://sagemaker.readthedocs.io/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/)

---

**⚠️ Important**: Always remember to delete SageMaker endpoints after testing to avoid unnecessary charges!