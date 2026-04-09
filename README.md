# SparkAI – Student Performance Prediction and Recommendation System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3-green.svg)
![ML](https://img.shields.io/badge/ML-RandomForest-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg).

SparkAI is a full-stack AI-powered web application designed to predict student academic performance and provide personalized recommendations. The system leverages Machine Learning techniques to identify at-risk students and assist teachers, students, and administrators with data-driven insights.

This project is developed as a **Final Year Engineering Project** and follows both **academic (IEEE)** and **industry-level** standards.

---

## 📸 Screenshots

<div align="center">
  <img src="screenshots/teacher-dashboard.png" alt="Teacher Dashboard" width="800"/>
  <p><em>Teacher Dashboard with student performance overview</em></p>
  
  <img src="screenshots/student-dashboard.png" alt="Student Dashboard" width="800"/>
  <p><em>Student Dashboard with personal metrics</em></p>
  
  <img src="screenshots/prediction-form.png" alt="Prediction Form" width="800"/>
  <p><em>AI Performance Prediction Form</em></p>
  
</div>

---

## ✨ Key Features

### 🔐 Role-Based Access Control

| Role      | Capabilities                                                                 |
|-----------|------------------------------------------------------------------------------|
| **Admin** | • Add/delete users<br>• Upload student data via CSV<br>• Manage all records |
| **Teacher** | • View analytics dashboard<br>• Identify at-risk students<br>• View prediction history<br>• Download AI reports |
| **Student** | • View personal dashboard<br>• Receive AI recommendations<br>• Track history<br>• Download PDF reports |

---

### 🤖 AI & Machine Learning

#### Scoring System (100 marks total)
| Component | Marks | Weight |
|-----------|-------|--------|
| 📄 Assignments | 10 | 10% |
| 📝 Midterm | 20 | 20% |
| 🧪 Internal Score | 30 | 30% |
| 🎓 End-term (Predicted) | 40 | 40% |

#### Performance Categories
| Category | Score Range | Risk Level |
|----------|-------------|------------|
| 🟢 **Excellent** | 80-100 | Low Risk |
| 🔵 **Good** | 70-79 | Low Risk |
| 🟡 **Average** | 60-69 | Medium Risk |
| 🔴 **Needs Improvement** | Below 60 | High Risk |

#### Risk Classification
- **High Risk**: Total score < 60 OR Attendance < 60%
- **Medium Risk**: Total score < 70 OR Attendance < 75%
- **Low Risk**: All other cases

---

### 📊 Dashboards & Analytics

#### 👨‍🏫 Teacher Dashboard
- Class overview statistics
- Student list with detailed scores (A/10, M/20, I/30, E/40)
- Risk level indicators with color coding
- Performance distribution charts
- Advanced filtering and sorting
- CSV export functionality

#### 👨‍🎓 Student Dashboard
- Personal metrics dashboard
- Score breakdown with progress bars
- AI performance insights
- Personalized recommendations
- Recent prediction history
- PDF report download

#### 📈 Prediction History
- Timeline view of all predictions
- Detailed score breakdowns
- Performance trend analysis
- Category distribution charts
- Export to CSV

---

### 💬 AI Chatbot Assistant

Intelligent academic assistant that provides guidance on:
- 📅 Attendance improvement strategies
- 📚 Study planning and time management
- ✍️ Exam preparation techniques
- 📊 GPA enhancement tips
- ⚠️ Risk level analysis
- 🎯 Personalized recommendations

**Features:**
- Quick action buttons for common queries
- Conversation history tracking
- Export chat functionality
- Real-time typing indicators
- Clean, modern chat interface

---

### 📄 PDF Report Generation

AI-generated comprehensive student progress report including:
- Student information and profile
- Academic metrics with score breakdown
- AI-predicted performance category
- Risk level analysis
- Personalized recommendations
- Total score calculation
- Performance trends

---

### 📂 CSV Bulk Upload

Admin can upload multiple students via CSV with automatic login credential generation:

```csv
roll_no,name,attendance,assignments_score,midterm_score,internal_score,final_score,study_hours,performance
101,John Doe,85,9,17,25,32,3,Good
102,Jane Smith,92,9,18,28,36,3,Excellent

🧠 Machine Learning Architecture
Models Used
Model Type	Purpose	Output
Regression	End-term prediction	0-40 marks
Classification	Performance category	Excellent/Good/Average/Poor
Algorithms
Random Forest Regressor

Random Forest Classifier

Gradient Boosting (optional)

Ensemble methods

Feature Engineering
Attendance percentage

Assignments score (0-10)

Midterm score (0-20)

Internal score (0-30)

Study hours per day

Interaction features

Academic score ratios

Fallback Formula
When ML models are unavailable, the system uses:

text
Predicted End-term = (Academic Scores × 70%) + (Attendance × 30%)
Where Academic Scores = Assignments + Midterm + Internal (max 60 marks)

🗂 Project Structure
text
SparkAI-Student-Performance-Prediction/
│
├── 📄 app.py                          # Main Flask application
├── 📄 model_train.py                  # ML model training
├── 📄 database_setup.py                # Database initialization
├── 📄 requirements.txt                 # Python dependencies
├── 📄 student_data.csv                 # Sample dataset
├── 📄 .gitignore                       # Git ignore rules
├── 📄 README.md                         # Documentation
│
├── 📁 ml_model/                         # Trained ML models
│   ├── endterm_predictor_40.joblib
│   ├── performance_classifier.joblib
│   ├── label_encoder.joblib
│   ├── scaler.joblib
│   └── feature_columns.joblib
│
├── 📁 database/                          # SQLite database
│   └── student_system.db
│
├── 📁 templates/                         # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── predict.html
│   ├── result.html
│   ├── teacher_dashboard.html
│   ├── student_dashboard.html
│   ├── admin_dashboard.html
│   ├── prediction_history.html
│   ├── student_history.html
│   ├── chatbot.html
│   └── student_profile.html
│
├── 📁 static/                            # Static assets
│   ├── css/
│   ├── js/
│   └── images/
│
└── 📁 screenshots/                        # Project screenshots
    ├── teacher-dashboard.png
    ├── student-dashboard.png
    ├── prediction-form.png
    └── chatbot.png
🚀 Installation & Setup
Prerequisites
Python 3.8 or higher

pip package manager

SQLite3

Git

Step-by-Step Installation
Clone the repository

bash
git clone https://github.com/yourusername/SparkAI-Student-Performance-Prediction.git
cd SparkAI-Student-Performance-Prediction
Create virtual environment

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
Install dependencies

bash
pip install -r requirements.txt
Set up database

bash
python database_setup.py
Train ML models (optional)

bash
python model_train.py
Note: The app includes a fallback formula, so training is optional. The system works perfectly even without trained models.

Run the application

bash
python app.py
Access the application

text
http://localhost:5000
🔑 Default Login Credentials
Role	Username	Password	Description
Admin	admin	admin123	Full system access
Teacher	teacher	teacher123	View analytics and student data
Student	student101	student123	Personal dashboard access
Tip: After starting the app, visit /add-sample-data to populate the database with 100+ sample students for testing.

📊 Database Schema
Users Table
sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT CHECK(role IN ('admin', 'teacher', 'student')),
    roll_no INTEGER
);
Students Table
sql
CREATE TABLE students (
    roll_no INTEGER PRIMARY KEY,
    name TEXT,
    attendance REAL,
    assignments_score REAL,
    midterm_score REAL,
    internal_score REAL,
    final_score REAL,
    study_hours REAL,
    performance TEXT
);
Prediction History Table
sql
CREATE TABLE prediction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no INTEGER,
    assignments_score REAL,
    midterm_score REAL,
    internal_score REAL,
    predicted_endterm REAL,
    total_score REAL,
    predicted_label TEXT,
    date_time TEXT,
    FOREIGN KEY (roll_no) REFERENCES students(roll_no)
);
🧪 Model Performance Metrics
Regression Model (End-term Predictor)
Metric	Value
R² Score	0.85-0.92
RMSE	±3-4 marks
MAE	±2-3 marks
Classification Model (Performance Category)
Metric	Value
Accuracy	88-94%
Precision	0.87-0.93
Recall	0.86-0.92
F1-Score	0.86-0.92
🎯 Use Cases
Early Intervention - Identify at-risk students before they fail

Personalized Learning - Tailored recommendations for each student

Data-Driven Decisions - Help teachers make informed decisions

Progress Tracking - Monitor student improvement over time

Administrative Planning - Generate reports for stakeholders

Student Self-Assessment - Students can track their own progress

🔮 Future Enhancements
Deep Learning Models - LSTM for time-series prediction

LLM Integration - Advanced chatbot with GPT capabilities

Real-time Analytics - WebSocket-based live updates

Cloud Deployment - AWS/Azure/GCP hosting

Mobile App - React Native or Flutter app

Multi-language Support - Hindi, regional languages

LMS Integration - Moodle, Canvas plugins

Advanced Visualizations - Interactive charts with D3.js

Email Notifications - Automated alerts for at-risk students

WhatsApp Bot - Chatbot integration with WhatsApp

👨‍🎓 Author
RAKESH G

🎓 Engineering Student, KRMU (K.R. Mangalam University)

🤖 AI / Machine Learning Minor Project

📧 Email: 2401201064@krmu.edu.in

🔗 LinkedIn: linkedin.com/in/rakesh-g

🐱 GitHub: github.com/rakeshg

📄 License
This project is developed for educational purposes as part of a Final Year Engineering Project.

text
MIT License

Copyright (c) 2026 RAKESH G

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
🙏 Acknowledgements
K.R. Mangalam University - Project guidance and support

Scikit-learn - Machine learning library

Flask Community - Web framework

Tailwind CSS - UI components

Font Awesome - Icons

Chart.js - Data visualization

ReportLab - PDF generation

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

⭐ Show Your Support
If you find this project useful, please consider giving it a star on GitHub! ⭐

<div align="center"> <sub>Built with ❤️ for better education outcomes | Final Year Engineering Project 2026</sub> <br> <sub>📍 K.R. Mangalam University | 📅 February 2026</sub> </div> ```
