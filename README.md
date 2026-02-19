# SparkAI – Student Performance Prediction and Recommendation System

SparkAI is a full-stack AI-powered web application designed to predict student academic performance and provide personalized recommendations. The system leverages Machine Learning techniques to identify at-risk students and assist teachers, students, and administrators with data-driven insights.

This project is developed as a **Final Year Engineering Project** and follows both **academic (IEEE)** and **industry-level** standards.

---

## 🚀 Features

### 🔐 Role-Based Access Control

- **Admin**
  - Add / delete users
  - Upload student data via CSV
  - Manage student and user records
- **Teacher**
  - View analytics dashboard
  - Identify at-risk students
  - View prediction history with detailed scores
  - Download AI-generated reports
- **Student**
  - View personal academic dashboard
  - Receive AI-based recommendations
  - Track prediction history
  - Download performance PDF report

---

### 🤖 Artificial Intelligence & Machine Learning

- Student performance prediction using **Random Forest Classifier** and **Regression models**
- **Scoring System (100 marks total):**
  - **Assignments**: 10 marks
  - **Midterm**: 20 marks
  - **Internal Score**: 30 marks
  - **End-term (Predicted)**: 40 marks
- Performance categories based on total score:
  - **Excellent**: 80-100 marks
  - **Good**: 70-79 marks
  - **Average**: 60-69 marks
  - **Needs Improvement**: Below 60 marks
- Risk level classification:
  - **High Risk** (Total < 60 or Attendance < 60%)
  - **Medium Risk** (Total < 70 or Attendance < 75%)
  - **Low Risk** (All other cases)
- Personalized academic recommendations based on performance metrics

---

### 📊 Dashboards & Analytics

- **Teacher Dashboard** with:
  - Class overview statistics
  - Student list with detailed scores
  - Risk level indicators
  - Performance distribution charts
  - Filtering and sorting capabilities
- **Student Dashboard** with:
  - Personal metrics (attendance, input total, end-term, total)
  - Score breakdown with progress bars
  - AI performance insights
  - Personalized recommendations
  - Recent prediction history
- **Prediction History** with:
  - Timeline view of predictions
  - Detailed score breakdowns
  - Performance trend analysis
  - CSV export functionality

---

### 💬 AI Chatbot

- Intelligent academic assistant
- Provides guidance on:
  - Attendance improvement
  - Study planning
  - Exam preparation
  - GPA enhancement
  - Risk level analysis
- Clean, modern chat interface with:
  - Quick action buttons
  - Message history
  - Export conversation feature

---

### 📄 PDF Report Generation

- AI-generated student progress report
- Includes:
  - Student information
  - Academic metrics with score breakdown
  - AI-predicted performance
  - Risk level analysis
  - Personalized recommendations
  - Total score calculation

---

### 📂 CSV Bulk Upload

- Admin can upload multiple students via CSV
- Required columns:
  ```
  roll_no, name, attendance, assignments_score, midterm_score, internal_score, final_score, study_hours, performance
  ```
- Auto-generates student login credentials

---

## 🧠 Machine Learning Model Details

### Models Used:

- **Regression Model**: Predicts end-term marks (0-40)
- **Classification Model**: Predicts performance category (Excellent/Good/Average/Poor)

### Libraries:

- **Scikit-learn** (Random Forest, Gradient Boosting)
- **Joblib** for model serialization
- **Pandas** & **NumPy** for data processing

### Input Features:

- Attendance (%)
- Assignments score (0-10)
- Midterm score (0-20)
- Internal score (0-30)
- Study hours per day

### Fallback Formula (when ML model not available):

```
Predicted End-term = (Academic Scores × 70%) + (Attendance × 30%)
```

- Academic Scores = Assignments + Midterm + Internal (60 marks total)

---

## 🗂 Project Structure

```
SparkAI-Student-Performance-Prediction/
│
├── app.py                          # Main Flask application
├── model_train.py                  # Model training & evaluation
├── database_setup.py                # Database initialization
├── requirements.txt                 # Python dependencies
├── student_data.csv                 # Sample dataset
│
├── ml_model/
│   ├── endterm_predictor_40.joblib  # Regression model
│   ├── performance_classifier.joblib # Classification model
│   ├── label_encoder.joblib         # Label encoder
│   ├── scaler.joblib                 # Feature scaler
│   └── feature_columns.joblib        # Feature names
│
├── database/
│   └── student_system.db             # SQLite database
│
├── templates/
│   ├── base.html                      # Base template
│   ├── index.html                     # Landing page
│   ├── login.html                     # Login page
│   ├── predict.html                    # Prediction form
│   ├── result.html                     # Prediction results
│   ├── teacher_dashboard.html          # Teacher view
│   ├── student_dashboard.html          # Student view
│   ├── admin_dashboard.html            # Admin view
│   ├── prediction_history.html         # Teacher history view
│   ├── student_history.html            # Student history view
│   ├── chatbot.html                    # AI assistant
│   └── student_profile.html            # Individual student profile
│
└── .gitignore
```

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.8+
- pip package manager
- SQLite3

### Steps

1. **Clone the repository**

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up database**

   ```bash
   python database_setup.py
   ```

5. **Train ML models (optional)**

   ```bash
   python model_train.py
   ```

   _Note: The app includes a fallback formula, so training is optional._

6. **Run the application**

   ```bash
   python app.py
   ```

7. **Access the application**
   ```
   http://localhost:5000
   ```

---

## 🔑 Default Login Credentials

| Role    | Username     | Password     |
| ------- | ------------ | ------------ |
| Admin   | `admin`      | `admin123`   |
| Teacher | `teacher`    | `teacher123` |
| Student | `student101` | `student123` |

_Add sample data by visiting `/add-sample-data` after starting the app._

---

## 📊 Database Schema

### Users Table

```sql
users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT,
    roll_no INTEGER
)
```

### Students Table

```sql
students (
    roll_no INTEGER PRIMARY KEY,
    name TEXT,
    attendance REAL,
    assignments_score REAL,
    midterm_score REAL,
    internal_score REAL,
    final_score REAL,
    study_hours REAL,
    performance TEXT
)
```

### Prediction History Table

```sql
prediction_history (
    id INTEGER PRIMARY KEY,
    roll_no INTEGER,
    assignments_score REAL,
    midterm_score REAL,
    internal_score REAL,
    predicted_endterm REAL,
    total_score REAL,
    predicted_label TEXT,
    date_time TEXT
)
```

---

## 🧪 Model Evaluation Metrics

The system evaluates both models:

### Regression Model (End-term Predictor)

- R² Score
- Root Mean Square Error (RMSE)
- Mean Absolute Error (MAE)

### Classification Model (Performance Category)

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

---

## 📌 Use Cases

- **Early identification** of at-risk students
- **Personalized academic guidance** for students
- **Decision support** for teachers and administrators
- **Educational data analytics** and reporting
- **Progress tracking** over time

---

## 🔮 Future Enhancements

- [ ] Deep Learning-based models (LSTM for time-series prediction)
- [ ] Large Language Model (LLM) powered chatbot
- [ ] Real-time analytics with WebSockets
- [ ] Cloud deployment (AWS/Azure/GCP)
- [ ] Mobile app with React Native
- [ ] Multi-language support
- [ ] Integration with LMS platforms (Moodle, Canvas)

---

## 👨‍🎓 Author

**RAKESH G**
Engineering Student
AI / Machine Learning Minor Project
KRMU (K.R. Mangalam University)

---

## 📄 License

This project is for educational purposes only.

---

## 🙏 Acknowledgements

- K.R. Mangalam University for project guidance
- Scikit-learn documentation
- Flask community
- Tailwind CSS for UI components
- Font Awesome for icons

---

_Last Updated: February 2026_
