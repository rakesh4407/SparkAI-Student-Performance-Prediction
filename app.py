from flask import (
    Flask, render_template, request, abort,
    redirect, url_for, session, send_file, flash
)
import joblib
import numpy as np
import pandas as pd
import sqlite3
import os
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# ===================== APP =====================
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret")

# ===================== PATHS =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "student_system.db")

# Updated model paths for new scoring system
MODEL_PATH = os.path.join(BASE_DIR, "ml_model", "endterm_predictor_40.joblib")
ENCODER_PATH = os.path.join(BASE_DIR, "ml_model", "label_encoder.joblib")
SCALER_PATH = os.path.join(BASE_DIR, "ml_model", "scaler.joblib")
FEATURES_PATH = os.path.join(BASE_DIR, "ml_model", "feature_columns.joblib")

# ===================== MODEL LOADING =====================
try:
    model = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(ENCODER_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_columns = joblib.load(FEATURES_PATH)
    print("✅ All ML models loaded successfully!")
except Exception as e:
    print(f"⚠️  Warning: Could not load ML models: {e}")
    model = None
    label_encoder = None
    scaler = None
    feature_columns = None

# ===================== DB HELPERS =====================
def get_db_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db_and_admin():
    conn = get_db_connection()

    # Create users table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            roll_no INTEGER
        )
    """)

    # Create students table with internal_score column (renamed from test_score)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
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
    """)

    # Create prediction_history table with new columns (IF NOT EXISTS)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no INTEGER,
            assignments_score REAL,
            midterm_score REAL,
            internal_score REAL,
            predicted_endterm REAL,
            total_score REAL,
            predicted_label TEXT,
            date_time TEXT
        )
    """)

    # Check and create admin account
    admin = conn.execute(
        "SELECT * FROM users WHERE username='admin'"
    ).fetchone()

    if not admin:
        conn.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (
            "admin",
            generate_password_hash("admin123"),
            "admin"
        ))

    # Add teacher account
    teacher = conn.execute(
        "SELECT * FROM users WHERE username='teacher'"
    ).fetchone()

    if not teacher:
        conn.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (
            "teacher",
            generate_password_hash("teacher123"),
            "teacher"
        ))

    conn.commit()
    conn.close()

# -------------------- DATABASE MIGRATION ROUTE --------------------
@app.route("/migrate-db")
def migrate_db():
    """Migrate existing database to new schema"""
    try:
        conn = get_db_connection()
        
        # Check if old table exists and has old structure
        table_info = conn.execute("PRAGMA table_info(prediction_history)").fetchall()
        existing_columns = [col[1] for col in table_info]
        
        # If it's the old table (only has id, roll_no, predicted_label, date_time)
        if len(existing_columns) <= 4 and 'assignments_score' not in existing_columns:
            # Create new table with updated schema
            conn.execute("""
                CREATE TABLE IF NOT EXISTS prediction_history_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roll_no INTEGER,
                    assignments_score REAL,
                    midterm_score REAL,
                    internal_score REAL,
                    predicted_endterm REAL,
                    total_score REAL,
                    predicted_label TEXT,
                    date_time TEXT
                )
            """)
            
            # Copy data from old table
            conn.execute("""
                INSERT INTO prediction_history_new (id, roll_no, predicted_label, date_time)
                SELECT id, roll_no, predicted_label, date_time FROM prediction_history
            """)
            
            # Drop old table and rename new one
            conn.execute("DROP TABLE prediction_history")
            conn.execute("ALTER TABLE prediction_history_new RENAME TO prediction_history")
            
            conn.commit()
            return "✅ Database migrated successfully! Old data preserved."
        else:
            # Check if any columns are missing and add them
            migrations_run = []
            
            new_columns = [
                ('assignments_score', 'REAL'),
                ('midterm_score', 'REAL'),
                ('internal_score', 'REAL'),
                ('predicted_endterm', 'REAL'),
                ('total_score', 'REAL')
            ]
            
            for col_name, col_type in new_columns:
                if col_name not in existing_columns:
                    try:
                        conn.execute(f"ALTER TABLE prediction_history ADD COLUMN {col_name} {col_type}")
                        migrations_run.append(col_name)
                    except:
                        pass
            
            if migrations_run:
                conn.commit()
                return f"✅ Added missing columns: {', '.join(migrations_run)}"
            else:
                return "✅ Database schema is already up to date."
                
    except Exception as e:
        return f"Error during migration: {str(e)}"
    finally:
        conn.close()

# -------------------- PREDICTION FUNCTIONS --------------------
def engineer_prediction_features(attendance, assignments, midterm, internal_score):
    """Engineer features for prediction (study hours removed)"""
    internal_total = assignments + midterm + internal_score  # 60 marks total
    internal_percentage = (internal_total / 60) * 100 if internal_total > 0 else 0
    
    # Create feature array in the same order as training
    features = {
        'attendance': attendance,
        'assignments_score': assignments,
        'midterm_score': midterm,
        'internal_score': internal_score,
        'internal_percentage': internal_percentage,
        'attendance_impact': -0.1 if attendance < 75 else (0.1 if attendance > 90 else 0),
        'previous_performance': internal_percentage / 100,
        'assignments_ratio': assignments / 10,
        'midterm_ratio': midterm / 20,
        'internal_ratio': internal_score / 30,
        'academic_score': (assignments/10 * 0.1 + midterm/20 * 0.2 + internal_score/30 * 0.3) * 100
    }
    
    # Create array in correct order - filter out any features not in our dict
    if feature_columns:
        valid_features = []
        for col in feature_columns:
            if col in features:
                valid_features.append(features[col])
            else:
                valid_features.append(0)  # Placeholder for missing features
        feature_array = np.array([valid_features])
    else:
        # Fallback if feature_columns not available
        feature_array = np.array([[attendance, assignments, midterm, internal_score, internal_percentage]])
    
    return feature_array, features

def predict_endterm(attendance, assignments, midterm, internal_score):
    """Predict end-term marks (0-40) - study hours removed"""
    # Try to use ML model if available
    if model is not None and scaler is not None and feature_columns is not None:
        try:
            # Engineer features
            feature_array, feature_dict = engineer_prediction_features(
                attendance, assignments, midterm, internal_score
            )
            
            # Scale features
            feature_scaled = scaler.transform(feature_array)
            
            # Make prediction
            predicted_score = model.predict(feature_scaled)[0]
            
            # Clip to valid range (0-40)
            predicted_score = np.clip(predicted_score, 0, 40)
            
            # Calculate confidence based on data quality
            confidence = 85  # Base confidence
            
            # Adjust confidence based on data quality
            if attendance < 50:
                confidence -= 10
            if assignments == 0 or midterm == 0 or internal_score == 0:
                confidence -= 5
                
            return round(predicted_score, 1), confidence, None
            
        except Exception as e:
            print(f"ML prediction failed, using fallback: {e}")
            # Fall through to fallback formula
    
    # FALLBACK FORMULA: Calculate based on academic performance and attendance
    input_total = assignments + midterm + internal_score
    input_percentage = input_total / 60
    
    # Formula: 70% from academics, 30% from attendance
    predicted_score = (input_percentage * 28) + ((attendance / 100) * 12)
    predicted_score = min(40, max(0, round(predicted_score, 1)))
    
    # Calculate confidence
    confidence = 80
    if attendance < 50:
        confidence -= 10
    if input_total < 30:
        confidence -= 10
        
    return predicted_score, confidence, None

def get_performance_category(total_score):
    """Determine performance category based on total score (100 marks)"""
    if total_score >= 80:
        return "Excellent"
    elif total_score >= 70:
        return "Good"
    elif total_score >= 60:
        return "Average"
    else:
        return "Poor"

def get_risk_level(total_score, attendance):
    """Determine risk level"""
    if total_score < 60 or attendance < 60:
        return "High"
    elif total_score < 70 or attendance < 75:
        return "Medium"
    else:
        return "Low"

def generate_recommendations(attendance, assignments, midterm, internal_score, study_hours, predicted_endterm, total_score):
    """Generate personalized recommendations"""
    recommendations = []
    
    internal_total = assignments + midterm + internal_score
    internal_percentage = (internal_total / 60) * 100
    
    if attendance < 75:
        recommendations.append(f"Improve attendance (currently {attendance}%) to at least 75% for better understanding")
    
    if internal_percentage < 60:
        recommendations.append(f"Focus on internal assessments - current total is {internal_total:.1f}/60 (below 60%)")
    
    if study_hours < 2:
        recommendations.append(f"Increase study hours to at least 2-3 hours per day (currently {study_hours} hrs)")
    
    if predicted_endterm < 25:
        recommendations.append(f"Need to prepare well for end-term - predicted score {predicted_endterm}/40")
    
    if total_score < 60:
        recommendations.append("⚠️ URGENT: You are at high risk of poor performance. Schedule a meeting with your teacher.")
    elif total_score < 70:
        recommendations.append("Focus on improving your weakest subject to reach the 'Good' category")
    elif total_score < 80:
        recommendations.append("You're doing well! Consistent effort can help you achieve 'Excellent'")
    else:
        recommendations.append("Excellent performance! Consider helping peers or taking advanced courses")
    
    if not recommendations:
        recommendations.append("Good progress! Maintain consistency for end-term exam")
    
    return recommendations

# -------------------- RISK & RECOMMENDATION (Legacy support) --------------------
def get_risk_and_recommendation(student):
    """Calculate risk level and recommendations for a student (updated for new schema)"""
    try:
        # Safely get values with defaults
        attendance = float(student.get("attendance") or 0)
        performance = str(student.get("performance") or "Average")
        
        # Calculate total score if available
        assignments = float(student.get("assignments_score") or 0)
        midterm = float(student.get("midterm_score") or 0)
        internal_score = float(student.get("internal_score") or 0)
        final = float(student.get("final_score") or 0)
        
        total_score = assignments + midterm + internal_score + final
        
        # Calculate risk based on total score and attendance
        if attendance < 60 or total_score < 60:
            risk = "High"
        elif attendance < 75 or total_score < 70:
            risk = "Medium"
        else:
            risk = "Low"

        # Generate recommendations
        rec = []
        if attendance < 75:
            rec.append("Improve attendance and avoid missing classes.")
        if total_score < 60:
            rec.append("Focus on basics & seek extra help.")
        if final < 20:
            rec.append("Need to prepare better for end-term exam.")

        if not rec:
            rec.append("Good progress! Maintain consistency.")

        return risk, " ".join(rec)
    except Exception as e:
        print(f"Error in get_risk_and_recommendation: {e}")
        return "Medium", "Unable to generate recommendations due to data issues."

# -------------------- CHATBOT LOGIC --------------------
def chatbot_reply(message: str) -> str:
    msg = message.lower()

    if any(word in msg for word in ["hello", "hi", "hey"]):
        return "Hi! 👋 I'm your AI assistant. Ask me about attendance, marks, risk level, or how to improve your studies."

    if "attendance" in msg:
        return "Attendance is very important. Try to keep it above 75% for better performance."

    if "study" in msg or "hours" in msg:
        return "Aim for 2-3 hours of focused study daily. Break it into 45-minute sessions with short breaks."

    if "exam" in msg or "test" in msg:
        return "For exams, revise previous papers, focus on important topics, and practice regularly."

    if "improve" in msg or "low marks" in msg:
        return "Check which area is weak: attendance, assignments, or internal assessments. Focus on improving one area at a time."

    if "risk" in msg:
        return "Risk levels: Low (doing well), Medium (need improvement), High (at risk of failing). Check your dashboard for details."

    if "recommendation" in msg or "suggest" in msg:
        return "Make a study timetable, focus on weak subjects, revise daily, and ask doubts early."

    if "who are you" in msg:
        return "I'm SparkAI's chatbot assistant. I help with study guidance and system navigation."

    return "I'm not sure about that. You can ask me about attendance, study tips, exam preparation, or risk levels."

# -------------------- AUTH HELPERS --------------------
def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    return user

def login_required(role=None):
    if "user_id" not in session:
        return False
    if role and session.get("role") != role:
        return False
    return True

# ===================== ERROR HANDLING =====================

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', 
                         error_message="The page you're looking for doesn't exist.",
                         error_code=404), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server Error: {error}')
    return render_template('error.html',
                         error_message="Something went wrong on our server. Please try again later.",
                         error_code=500), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('error.html',
                         error_message="You don't have permission to access this page.",
                         error_code=403), 403

@app.errorhandler(400)
def bad_request_error(error):
    return render_template('error.html',
                         error_message="Bad request. Please check your input.",
                         error_code=400), 400

# -------------------- ROUTES --------------------

@app.route("/")
def home():
    return render_template("index.html")

# ---------- LOGIN / LOGOUT ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        role = request.form["role"]
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        user = get_user_by_username(username)
        if user and user["role"] == role and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            if role == "admin":
                return redirect(url_for("admin_dashboard"))
            elif role == "teacher":
                return redirect(url_for("teacher_dashboard"))
            else:
                return redirect(url_for("student_dashboard"))
        else:
            error = "Invalid login details!"

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/predict", methods=["GET"])
def predict_form():
    return render_template("predict.html")

# ---------- PREDICT (UPDATED with fallback formula) ----------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get form data
        attendance = float(request.form["attendance"])
        assignments = float(request.form["assignments"])
        midterm = float(request.form["midterm"])
        internal_score = float(request.form["internal_score"])
        hours = float(request.form["hours"])

        # Validate inputs
        if not (0 <= attendance <= 100):
            raise ValueError("Attendance must be between 0 and 100")
        if not (0 <= assignments <= 10):
            raise ValueError("Assignments score must be between 0 and 10")
        if not (0 <= midterm <= 20):
            raise ValueError("Midterm score must be between 0 and 20")
        if not (0 <= internal_score <= 30):
            raise ValueError("Internal score must be between 0 and 30")
        if not (0 <= hours <= 24):
            raise ValueError("Study hours must be between 0 and 24")

        # Calculate input total (60 marks)
        input_total = assignments + midterm + internal_score
        input_percentage = (input_total / 60) * 100

        # Predict end-term marks (0-40) - now with fallback
        predicted_endterm, confidence, error = predict_endterm(
            attendance, assignments, midterm, internal_score
        )

        # Calculate total score (out of 100)
        total_score = input_total + predicted_endterm

        # Get performance category (using 'category' to match result.html)
        category = get_performance_category(total_score)

        # Get risk level
        risk_level = get_risk_level(total_score, attendance)

        # Generate recommendations (study hours still used for recommendations)
        recommendations = generate_recommendations(
            attendance, assignments, midterm, internal_score, hours, 
            predicted_endterm, total_score
        )

        # Calculate study efficiency (for display only, not used in prediction)
        study_efficiency = round(input_total / hours if hours > 0 else 0, 1)

        # Save to database (with error handling)
        try:
            conn = get_db_connection()
            
            roll_no = None
            if "user_id" in session and session.get("role") == "student":
                user = get_user_by_username(session.get("username"))
                if user and user["roll_no"]:
                    roll_no = user["roll_no"]

            conn.execute("""
                INSERT INTO prediction_history 
                (roll_no, assignments_score, midterm_score, internal_score, 
                 predicted_endterm, total_score, predicted_label, date_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                roll_no,
                assignments,
                midterm,
                internal_score,
                predicted_endterm,
                total_score,
                category,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            conn.commit()
            conn.close()
        except Exception as db_error:
            app.logger.error(f"Database error: {db_error}")
            # Continue even if database save fails

        # Render results
        return render_template(
            "result.html",
            # Input values
            attendance=attendance,
            assignments=assignments,
            midterm=midterm,
            internal_score=internal_score,
            hours=hours,
            
            # Calculated values
            input_total=round(input_total, 1),
            predicted_endterm=predicted_endterm,
            total_score=round(total_score, 1),
            
            # Predictions - using 'category' (not performance_category)
            category=category,
            confidence=confidence,
            
            # Analysis
            risk_level=risk_level,
            recommendations=recommendations,
            efficiency=study_efficiency
        )

    except ValueError as e:
        return render_template('error.html',
                             error_message=str(e),
                             error_code=400), 400
    except KeyError as e:
        return render_template('error.html',
                             error_message=f"Missing form field: {str(e)}. Please check that all fields are filled.",
                             error_code=400), 400
    except Exception as e:
        app.logger.error(f"Prediction error: {e}")
        return render_template('error.html',
                             error_message="An error occurred during prediction. Please try again.",
                             error_code=500), 500

@app.route("/dashboard")
def dashboard_redirect():
    if "role" not in session:
        return redirect(url_for("login"))

    if session["role"] == "teacher":
        return redirect(url_for("teacher_dashboard"))
    elif session["role"] == "student":
        return redirect(url_for("student_dashboard"))
    elif session["role"] == "admin":
        return redirect(url_for("admin_dashboard"))

    return redirect(url_for("login"))

# ---------- TEACHER DASHBOARD (FIXED VERSION) ----------
@app.route("/teacher-dashboard", methods=["GET"])
def teacher_dashboard():
    if not login_required(role="teacher"):
        return redirect(url_for("login"))

    try:
        search_query = request.args.get("search", "").lower()
        filter_risk = request.args.get("risk", "")
        filter_perf = request.args.get("performance", "")
        sort_by = request.args.get("sort", "")

        conn = get_db_connection()
        
        # Get all students
        students_result = conn.execute("SELECT * FROM students").fetchall()
        conn.close()

        # Handle empty student list
        if not students_result:
            return render_template(
                "teacher_dashboard.html",
                total_students=0,
                avg_attendance=0,
                avg_input=0,
                avg_endterm=0,
                avg_total=0,
                perf_counts={"Excellent": 0, "Good": 0, "Average": 0, "Poor": 0},
                perf_labels=["Excellent", "Good", "Average", "Poor"],
                perf_values=[0, 0, 0, 0],
                at_risk_students=[],
                search_query=search_query,
                filter_risk=filter_risk,
                filter_perf=filter_perf,
                sort_by=sort_by
            )

        # Convert to list of dictionaries with proper column names
        students_list = []
        column_names = ["roll_no", "name", "attendance", "assignments_score", 
                       "midterm_score", "internal_score", "final_score", "study_hours", "performance"]
        
        for row in students_result:
            student_dict = {}
            for i, col_name in enumerate(column_names):
                if i < len(row):
                    student_dict[col_name] = row[i]
                else:
                    student_dict[col_name] = 0  # Default value for missing columns
            students_list.append(student_dict)

        # Calculate risk and recommendation for each student
        at_risk_students = []
        total_input_sum = 0
        total_endterm_sum = 0
        total_score_sum = 0
        
        for student in students_list:
            # Calculate input total (60 marks)
            input_total = (float(student.get("assignments_score", 0)) + 
                          float(student.get("midterm_score", 0)) + 
                          float(student.get("internal_score", 0)))
            
            # Get end-term score (40 marks)
            endterm = float(student.get("final_score", 0))
            
            # Calculate total score (100 marks)
            total = input_total + endterm
            
            # Update sums for averages
            total_input_sum += input_total
            total_endterm_sum += endterm
            total_score_sum += total
            
            # Determine performance category based on total score
            if total >= 80:
                perf_category = "Excellent"
            elif total >= 70:
                perf_category = "Good"
            elif total >= 60:
                perf_category = "Average"
            else:
                perf_category = "Poor"
            
            # Determine risk level
            attendance = float(student.get("attendance", 0))
            if total < 60 or attendance < 60:
                risk = "High"
            elif total < 70 or attendance < 75:
                risk = "Medium"
            else:
                risk = "Low"
            
            # Generate recommendation
            rec = []
            if attendance < 75:
                rec.append("Improve attendance to at least 75%")
            if input_total < 36:  # 60% of 60
                rec.append("Focus on internal assessments (assignments, midterm, internal)")
            if endterm < 24:  # 60% of 40
                rec.append("Need to prepare better for end-term exam")
            if not rec:
                rec.append("Good progress! Maintain consistency")
            
            student["input_total"] = round(input_total, 1)
            student["total_score"] = round(total, 1)
            student["performance_category"] = perf_category  # Use this for display
            student["risk_level"] = risk
            student["recommendation"] = " ".join(rec)
            at_risk_students.append(student)

        # Apply filters
        filtered_students = at_risk_students
        
        if search_query:
            filtered_students = [
                s for s in filtered_students 
                if search_query in str(s["name"]).lower() or search_query in str(s["roll_no"])
            ]
        
        if filter_risk:
            filtered_students = [s for s in filtered_students if s["risk_level"] == filter_risk]
        
        if filter_perf:
            filtered_students = [s for s in filtered_students if s["performance_category"] == filter_perf]

        # Apply sorting
        if sort_by == "attendance":
            filtered_students.sort(key=lambda x: x["attendance"], reverse=True)
        elif sort_by == "total_score":
            filtered_students.sort(key=lambda x: x["total_score"], reverse=True)
        elif sort_by == "risk_high":
            risk_order = {"High": 3, "Medium": 2, "Low": 1}
            filtered_students.sort(key=lambda x: risk_order.get(x["risk_level"], 0), reverse=True)

        # Calculate statistics for filtered students
        total_students = len(filtered_students)
        
        if total_students > 0:
            avg_attendance = round(sum(s["attendance"] for s in filtered_students) / total_students, 1)
            avg_input = round(total_input_sum / len(students_list), 1)  # Overall average
            avg_endterm = round(total_endterm_sum / len(students_list), 1)
            avg_total = round(total_score_sum / len(students_list), 1)
        else:
            avg_attendance = 0
            avg_input = 0
            avg_endterm = 0
            avg_total = 0
        
        # Performance counts based on total score
        perf_counts = {"Excellent": 0, "Good": 0, "Average": 0, "Poor": 0}
        for student in filtered_students:
            perf_counts[student["performance_category"]] += 1
        
        perf_labels = list(perf_counts.keys())
        perf_values = list(perf_counts.values())
        
        return render_template(
            "teacher_dashboard.html",
            total_students=total_students,
            avg_attendance=avg_attendance,
            avg_input=avg_input,
            avg_endterm=avg_endterm,
            avg_total=avg_total,
            perf_counts=perf_counts,
            perf_labels=perf_labels,
            perf_values=perf_values,
            at_risk_students=filtered_students,
            search_query=search_query,
            filter_risk=filter_risk,
            filter_perf=filter_perf,
            sort_by=sort_by
        )
        
    except Exception as e:
        app.logger.error(f"Error in teacher_dashboard: {e}")
        import traceback
        traceback.print_exc()
        return render_template('error.html',
                             error_message=f"Error loading teacher dashboard: {str(e)}",
                             error_code=500), 500

# ---------- STUDENT PROFILE (UPDATED) ----------
@app.route("/student/<int:roll_no>")
def student_profile(roll_no):
    if not login_required(role="teacher"):
        return redirect(url_for("login"))

    conn = get_db_connection()
    student_row = conn.execute(
        "SELECT * FROM students WHERE roll_no = ?", (roll_no,)
    ).fetchone()
    conn.close()

    if student_row is None:
        return abort(404, "Student not found")

    # Convert to dictionary
    column_names = ["roll_no", "name", "attendance", "assignments_score", 
                   "midterm_score", "internal_score", "final_score", "study_hours", "performance"]
    student = {}
    for i, col_name in enumerate(column_names[:len(student_row)]):
        student[col_name] = student_row[i]

    risk, rec = get_risk_and_recommendation(student)
    
    # Calculate totals
    input_total = (student.get("assignments_score", 0) + 
                  student.get("midterm_score", 0) + 
                  student.get("internal_score", 0))
    endterm = student.get("final_score", 0)
    total = input_total + endterm

    return render_template(
        "student_profile.html",
        roll_no=student["roll_no"],
        name=student["name"],
        attendance=student["attendance"],
        assignments=student["assignments_score"],
        midterm=student["midterm_score"],
        internal_score=student.get("internal_score", 0),
        final=student["final_score"],
        study_hours=student["study_hours"],
        performance=student["performance"],
        input_total=round(input_total, 1),
        total_score=round(total, 1),
        risk_level=risk,
        recommendation=rec
    )

# ---------- STUDENT DASHBOARD (UPDATED) ----------
@app.route("/student-dashboard")
def student_dashboard():
    if not login_required(role="student"):
        return redirect(url_for("login"))

    username = session.get("username")
    user = get_user_by_username(username)

    if not user or not user["roll_no"]:
        return render_template('error.html',
                             error_message="Your account is not linked to a student record. Contact admin.",
                             error_code=400), 400

    roll_no = user["roll_no"]

    conn = get_db_connection()
    student_row = conn.execute(
        "SELECT * FROM students WHERE roll_no = ?", (roll_no,)
    ).fetchone()
    
    # Get prediction history for this student
    history_rows = conn.execute("""
        SELECT * FROM prediction_history 
        WHERE roll_no = ? 
        ORDER BY date_time DESC LIMIT 5
    """, (roll_no,)).fetchall()
    conn.close()

    if not student_row:
        return render_template('error.html',
                             error_message="Student record not found.",
                             error_code=404), 404

    # Convert to dictionary
    column_names = ["roll_no", "name", "attendance", "assignments_score", 
                   "midterm_score", "internal_score", "final_score", "study_hours", "performance"]
    student = {}
    for i, col_name in enumerate(column_names[:len(student_row)]):
        student[col_name] = student_row[i]

    risk, rec = get_risk_and_recommendation(student)
    
    # Calculate totals
    input_total = (student.get("assignments_score", 0) + 
                  student.get("midterm_score", 0) + 
                  student.get("internal_score", 0))
    endterm = student.get("final_score", 0)
    total = input_total + endterm

    # Process history
    history = []
    for row in history_rows:
        history.append({
            "date": row["date_time"],
            "predicted_endterm": row["predicted_endterm"],
            "total_score": row["total_score"],
            "category": row["predicted_label"]
        })

    return render_template(
        "student_dashboard.html",
        name=student["name"],
        roll_no=student["roll_no"],
        attendance=student["attendance"],
        assignments=student["assignments_score"],
        midterm=student["midterm_score"],
        internal_score=student.get("internal_score", 0),
        final=student["final_score"],
        study_hours=student["study_hours"],
        performance=student["performance"],
        input_total=round(input_total, 1),
        total_score=round(total, 1),
        risk_level=risk,
        recommendation=rec,
        history=history,
        username=username
    )

# ---------- TEACHER: PREDICTION HISTORY (UPDATED with backwards compatibility) ----------
@app.route("/prediction-history")
def prediction_history():
    if not login_required(role="teacher"):
        return redirect(url_for("login"))

    search = request.args.get("search", "").strip()
    label = request.args.get("label", "")
    sort = request.args.get("sort", "")

    conn = get_db_connection()
    
    # First, check which columns exist in the table
    try:
        table_info = conn.execute("PRAGMA table_info(prediction_history)").fetchall()
        existing_columns = [col[1] for col in table_info]
        print("Existing columns:", existing_columns)
        
        # Check if new columns exist
        has_new_columns = all(col in existing_columns for col in 
                              ['assignments_score', 'midterm_score', 'internal_score', 
                               'predicted_endterm', 'total_score'])
    except:
        has_new_columns = False
    
    if has_new_columns:
        # Use new query with all columns
        query = """
            SELECT ph.id, ph.roll_no, ph.assignments_score, ph.midterm_score, 
                   ph.internal_score, ph.predicted_endterm, ph.total_score, 
                   ph.predicted_label, ph.date_time, s.name
            FROM prediction_history ph
            LEFT JOIN students s ON ph.roll_no = s.roll_no
            WHERE 1=1
        """
        params = []

        if search:
            query += " AND (CAST(ph.roll_no AS TEXT) LIKE ? OR LOWER(s.name) LIKE ?)"
            params.extend([f"%{search}%", f"%{search.lower()}%"])

        if label:
            query += " AND ph.predicted_label = ?"
            params.append(label)

        if sort == "date_asc":
            query += " ORDER BY datetime(ph.date_time) ASC"
        elif sort == "total_desc":
            query += " ORDER BY ph.total_score DESC"
        elif sort == "endterm_desc":
            query += " ORDER BY ph.predicted_endterm DESC"
        else:
            query += " ORDER BY datetime(ph.date_time) DESC"

        rows = conn.execute(query, params).fetchall()
        
        # Process with new columns
        history = []
        for row in rows:
            history.append({
                "id": row[0],
                "roll_no": row[1],
                "assignments_score": row[2],
                "midterm_score": row[3],
                "internal_score": row[4],
                "predicted_endterm": row[5],
                "total_score": row[6],
                "predicted_label": row[7],
                "date_time": row[8],
                "name": row[9] if row[9] else "Unknown"
            })
    else:
        # Use old query (backwards compatibility)
        print("Using old table structure")
        query = """
            SELECT ph.id, ph.roll_no, ph.predicted_label, ph.date_time, s.name
            FROM prediction_history ph
            LEFT JOIN students s ON ph.roll_no = s.roll_no
            WHERE 1=1
        """
        params = []

        if search:
            query += " AND (CAST(ph.roll_no AS TEXT) LIKE ? OR LOWER(s.name) LIKE ?)"
            params.extend([f"%{search}%", f"%{search.lower()}%"])

        if label:
            query += " AND ph.predicted_label = ?"
            params.append(label)

        query += " ORDER BY datetime(ph.date_time) DESC"

        rows = conn.execute(query, params).fetchall()
        
        # Process with old structure
        history = []
        for row in rows:
            history.append({
                "id": row[0],
                "roll_no": row[1],
                "predicted_label": row[2],
                "date_time": row[3],
                "name": row[4] if row[4] else "Unknown",
                # Set default values for new fields
                "assignments_score": None,
                "midterm_score": None,
                "internal_score": None,
                "predicted_endterm": None,
                "total_score": None
            })
    
    conn.close()

    return render_template(
        "prediction_history.html",
        history=history,
        search=search,
        label=label,
        sort=sort
    )

# ---------- STUDENT: OWN HISTORY ----------
@app.route("/student-history")
def student_history():
    if not login_required(role="student"):
        return redirect(url_for("login"))

    username = session.get("username")
    user = get_user_by_username(username)

    if not user or not user["roll_no"]:
        return render_template('error.html',
                             error_message="Your account is not linked to a student record.",
                             error_code=400), 400

    roll_no = user["roll_no"]

    conn = get_db_connection()
    
    # Check which columns exist
    try:
        table_info = conn.execute("PRAGMA table_info(prediction_history)").fetchall()
        existing_columns = [col[1] for col in table_info]
        has_new_columns = 'assignments_score' in existing_columns
    except:
        has_new_columns = False
    
    if has_new_columns:
        # Use new query
        rows = conn.execute("""
            SELECT id, assignments_score, midterm_score, internal_score,
                   predicted_endterm, total_score, predicted_label, date_time 
            FROM prediction_history
            WHERE roll_no = ?
            ORDER BY datetime(date_time) DESC
        """, (roll_no,)).fetchall()
        
        history = []
        for row in rows:
            history.append({
                "id": row[0],
                "assignments": row[1],
                "midterm": row[2],
                "internal": row[3],
                "predicted_endterm": row[4],
                "total": row[5],
                "category": row[6],
                "date_time": row[7]
            })
    else:
        # Use old query
        rows = conn.execute("""
            SELECT id, predicted_label, date_time 
            FROM prediction_history
            WHERE roll_no = ?
            ORDER BY datetime(date_time) DESC
        """, (roll_no,)).fetchall()
        
        history = []
        for row in rows:
            history.append({
                "id": row[0],
                "assignments": None,
                "midterm": None,
                "internal": None,
                "predicted_endterm": None,
                "total": None,
                "category": row[1],
                "date_time": row[2]
            })
    
    conn.close()
    return render_template("student_history.html", history=history)

# ---------- PDF REPORT: STUDENT (UPDATED) ----------
@app.route("/student-report/<int:roll_no>")
def student_report(roll_no):
    if not login_required():
        return redirect(url_for("login"))

    username = session.get("username")
    role = session.get("role")
    user = get_user_by_username(username)

    if role == "student":
        if not user or not user["roll_no"] or int(user["roll_no"]) != roll_no:
            return render_template('error.html',
                                 error_message="You are not allowed to download this report.",
                                 error_code=403), 403

    conn = get_db_connection()
    student_row = conn.execute(
        "SELECT * FROM students WHERE roll_no = ?", (roll_no,)
    ).fetchone()
    conn.close()

    if student_row is None:
        return render_template('error.html',
                             error_message="Student not found.",
                             error_code=404), 404

    # Convert to dictionary
    column_names = ["roll_no", "name", "attendance", "assignments_score", 
                   "midterm_score", "internal_score", "final_score", "study_hours", "performance"]
    student = {}
    for i, col_name in enumerate(column_names[:len(student_row)]):
        student[col_name] = student_row[i]

    risk, rec = get_risk_and_recommendation(student)
    
    # Calculate totals
    input_total = (student.get("assignments_score", 0) + 
                  student.get("midterm_score", 0) + 
                  student.get("internal_score", 0))
    endterm = student.get("final_score", 0)
    total = input_total + endterm

    # Build PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    c.setFillColor(colors.HexColor("#2563eb"))
    c.rect(0, height-80, width, 80, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(40, height-50, "AI Progress Report")

    # Student info
    c.setFillColor(colors.black)
    y = height - 110
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, f"Student: {student['name']}  (Roll: {student['roll_no']})")
    y -= 25
    c.setFont("Helvetica", 11)
    c.drawString(40, y, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 30

    # Academic metrics
    c.setFont("Helvetica-Bold", 13)
    c.drawString(40, y, "Academic Metrics")
    y -= 18
    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Attendance: {student['attendance']}%")
    y -= 16
    c.drawString(50, y, f"Assignments Score: {student['assignments_score']}/10")
    y -= 16
    c.drawString(50, y, f"Midterm Score: {student['midterm_score']}/20")
    y -= 16
    c.drawString(50, y, f"Internal Score: {student.get('internal_score', 0)}/30")
    y -= 16
    c.drawString(50, y, f"Final Exam Score: {student['final_score']}/40")
    y -= 16
    c.drawString(50, y, f"Study Hours/Day: {student['study_hours']}")
    y -= 28

    # Performance section
    c.setFont("Helvetica-Bold", 13)
    c.drawString(40, y, "Performance Summary")
    y -= 18
    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Input Total (Assignments+Midterm+Internal): {input_total}/60")
    y -= 16
    c.drawString(50, y, f"Final Exam: {endterm}/40")
    y -= 16
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Total Score: {total}/100")
    y -= 20
    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Performance Category: {student['performance']}")
    y -= 16
    c.drawString(50, y, f"Risk Level: {risk}")
    y -= 28

    # Recommendations
    c.setFont("Helvetica-Bold", 13)
    c.drawString(40, y, "AI Recommendations")
    y -= 18
    c.setFont("Helvetica", 11)

    from reportlab.lib.utils import simpleSplit
    lines = simpleSplit(rec, "Helvetica", 11, width - 80)
    for line in lines:
        c.drawString(50, y, "• " + line)
        y -= 14
        if y < 80:
            c.showPage()
            y = height - 80
            c.setFont("Helvetica", 11)

    c.showPage()
    c.save()
    buffer.seek(0)

    filename = f"Student_Report_{student['roll_no']}.pdf"
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype="application/pdf")

# ---------- CHATBOT ROUTE ----------
@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    if "chat_history" not in session:
        session["chat_history"] = []
    
    history = session.get("chat_history", [])
    
    MAX_HISTORY = 20

    if request.method == "POST":
        user_msg = request.form.get("message", "").strip()
        clear_history = request.form.get("clear", "false") == "true"
        
        if clear_history:
            session["chat_history"] = []
            return redirect(url_for("chatbot"))
            
        if user_msg:
            bot_msg = chatbot_reply(user_msg)
            history.append({"sender": "user", "text": user_msg})
            history.append({"sender": "bot", "text": bot_msg})
            
            if len(history) > MAX_HISTORY:
                history = history[-MAX_HISTORY:]
                
            session["chat_history"] = history

    return render_template("chatbot.html", history=history, max_history=MAX_HISTORY)

# ---------- ADMIN DASHBOARD (UPDATED) ----------
@app.route("/admin-dashboard")
def admin_dashboard():
    if not login_required(role="admin"):
        return redirect(url_for("login"))

    conn = get_db_connection()

    users = conn.execute("""
        SELECT id, username, role, roll_no
        FROM users
        ORDER BY role
    """).fetchall()

    students = conn.execute("SELECT * FROM students").fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        users=users,
        students=students
    )

@app.route("/admin-add-student", methods=["POST"])
def admin_add_student():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))

    try:
        roll_no = int(request.form["roll_no"])
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]

        attendance = float(request.form["attendance"])
        assignments = float(request.form["assignments"])
        midterm = float(request.form["midterm"])
        internal_score = float(request.form.get("internal_score", 0))
        final = float(request.form["final"])
        study_hours = float(request.form["study_hours"])
        performance = request.form["performance"]

        conn = get_db_connection()
        cur = conn.cursor()

        # Insert into USERS
        cur.execute("""
            INSERT INTO users (username, password, role, roll_no)
            VALUES (?, ?, 'student', ?)
        """, (
            username,
            generate_password_hash(password),
            roll_no
        ))

        # Insert into STUDENTS with internal_score
        cur.execute("""
            INSERT INTO students
            (roll_no, name, attendance, assignments_score, midterm_score, 
             internal_score, final_score, study_hours, performance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            roll_no, name, attendance, assignments, midterm, 
            internal_score, final, study_hours, performance
        ))

        conn.commit()
        conn.close()
        
        return redirect(url_for("admin_dashboard"))
        
    except Exception as e:
        app.logger.error(f"Error adding student: {e}")
        return render_template('error.html',
                             error_message=f"Error adding student: {str(e)}",
                             error_code=400), 400

@app.route("/admin-add-user", methods=["POST"])
def admin_add_user():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))

    try:
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        role = request.form["role"]
        roll_no = request.form.get("roll_no")

        hashed_pw = generate_password_hash(password)

        conn = get_db_connection()
        
        roll_no_val = int(roll_no) if roll_no and roll_no.strip() else None
        
        conn.execute("""
            INSERT INTO users (username, password, role, roll_no)
            VALUES (?, ?, ?, ?)
        """, (
            username,
            hashed_pw,
            role,
            roll_no_val
        ))
        conn.commit()
        conn.close()
        
        return redirect(url_for("admin_dashboard"))
        
    except sqlite3.IntegrityError:
        return render_template('error.html',
                             error_message="Username already exists. Please choose a different username.",
                             error_code=400), 400
    except Exception as e:
        app.logger.error(f"Error adding user: {e}")
        return render_template('error.html',
                             error_message=f"Error adding user: {str(e)}",
                             error_code=400), 400

@app.route("/admin-delete-user/<int:user_id>")
def admin_delete_user(user_id):
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))

    try:
        conn = get_db_connection()
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()

        return redirect(url_for("admin_dashboard"))
        
    except Exception as e:
        app.logger.error(f"Error deleting user: {e}")
        return render_template('error.html',
                             error_message=f"Error deleting user: {str(e)}",
                             error_code=500), 500

# ---------- ADMIN: UPLOAD CSV (UPDATED) ----------
@app.route("/admin-upload-csv", methods=["POST"])
def admin_upload_csv():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))

    file = request.files.get("csv_file")
    if not file or not file.filename.endswith(".csv"):
        return render_template('error.html',
                             error_message="Invalid file. Please upload a CSV file.",
                             error_code=400), 400

    try:
        df = pd.read_csv(file)

        required_cols = [
            "roll_no", "name", "attendance",
            "assignments_score", "midterm_score",
            "internal_score", "final_score", "study_hours", "performance"
        ]

        for col in required_cols:
            if col not in df.columns:
                return render_template('error.html',
                                     error_message=f"Missing column: {col}. Required columns: {', '.join(required_cols)}",
                                     error_code=400), 400

        df = df.replace(r'^\s*$', None, regex=True)

        numeric_cols = [
            "roll_no", "attendance", "assignments_score", 
            "midterm_score", "internal_score", "final_score", "study_hours"
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=numeric_cols)

        df["roll_no"] = df["roll_no"].astype(int)
        df["attendance"] = df["attendance"].astype(float)
        df["assignments_score"] = df["assignments_score"].astype(float)
        df["midterm_score"] = df["midterm_score"].astype(float)
        df["internal_score"] = df["internal_score"].astype(float)
        df["final_score"] = df["final_score"].astype(float)
        df["study_hours"] = df["study_hours"].astype(float)

        df["performance"] = df["performance"].astype(str).str.strip().str.title()

        conn = get_db_connection()
        success_count = 0
        error_messages = []

        for _, row in df.iterrows():
            try:
                conn.execute("""
                    INSERT OR REPLACE INTO students
                    (roll_no, name, attendance, assignments_score, midterm_score,
                     internal_score, final_score, study_hours, performance)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row["roll_no"],
                    row["name"] if pd.notna(row["name"]) else "",
                    row["attendance"],
                    row["assignments_score"],
                    row["midterm_score"],
                    row["internal_score"],
                    row["final_score"],
                    row["study_hours"],
                    row["performance"]
                ))

                username = f"student{row['roll_no']}"
                default_password = "student123"
                
                existing_user = conn.execute(
                    "SELECT * FROM users WHERE username = ?", (username,)
                ).fetchone()
                
                if not existing_user:
                    conn.execute("""
                        INSERT INTO users (username, password, role, roll_no)
                        VALUES (?, ?, 'student', ?)
                    """, (
                        username,
                        generate_password_hash(default_password),
                        row["roll_no"]
                    ))
                    success_count += 1
                else:
                    conn.execute("""
                        UPDATE users SET roll_no = ? WHERE username = ?
                    """, (row["roll_no"], username))
                    success_count += 1
                    
            except Exception as e:
                error_messages.append(f"Row {row['roll_no']}: {str(e)}")

        conn.commit()
        conn.close()

        message = f"Successfully uploaded {success_count} students."
        if error_messages:
            message += f" Errors: {', '.join(error_messages[:3])}"
            if len(error_messages) > 3:
                message += f" and {len(error_messages)-3} more..."
                
        session['upload_message'] = message
        
        return redirect(url_for("admin_dashboard"))

    except Exception as e:
        app.logger.error(f"CSV upload error: {e}")
        return render_template('error.html',
                             error_message=f"CSV Upload Error: {str(e)}",
                             error_code=500), 500

# ---------- ADD SAMPLE DATA ROUTE (UPDATED) ----------
@app.route("/add-sample-data")
def add_sample_data():
    """Route to add sample data with internal scores"""
    try:
        conn = get_db_connection()
        
        # Clear existing data
        conn.execute("DELETE FROM students")
        conn.execute("DELETE FROM users WHERE role = 'student'")
        conn.execute("DELETE FROM prediction_history")
        
        # Sample student data with internal scores (0-30)
        students = [
            (101, "John Smith", 85.5, 8.5, 17.0, 25.0, 32.0, 3.5, "Good"),
            (102, "Emma Johnson", 92.0, 9.5, 19.0, 28.0, 36.0, 4.0, "Excellent"),
            (103, "Michael Brown", 45.0, 4.0, 8.0, 12.0, 18.0, 1.5, "Poor"),
            (104, "Sarah Davis", 75.0, 7.0, 14.0, 20.0, 28.0, 2.5, "Average"),
            (105, "Robert Wilson", 95.0, 9.0, 18.0, 27.0, 38.0, 4.5, "Excellent"),
            (106, "Lisa Miller", 68.0, 6.0, 12.0, 18.0, 24.0, 2.0, "Average"),
            (107, "David Taylor", 82.0, 8.0, 16.0, 24.0, 30.0, 3.0, "Good"),
            (108, "Jennifer Lee", 58.0, 5.0, 10.0, 15.0, 22.0, 1.8, "Poor"),
            (109, "William Clark", 88.0, 8.5, 17.0, 25.0, 34.0, 3.8, "Good"),
            (110, "Maria Garcia", 72.0, 7.0, 14.0, 21.0, 28.0, 2.8, "Average"),
        ]
        
        # Insert sample students
        conn.executemany("""
            INSERT INTO students 
            (roll_no, name, attendance, assignments_score, midterm_score, 
             internal_score, final_score, study_hours, performance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, students)
        
        # Create student user accounts
        for roll_no, name, _, _, _, _, _, _, _ in students:
            username = f"student{roll_no}"
            conn.execute("""
                INSERT INTO users (username, password, role, roll_no)
                VALUES (?, ?, 'student', ?)
            """, (
                username,
                generate_password_hash("student123"),
                roll_no
            ))
        
        conn.commit()
        conn.close()
        
        return """
        <h1>✅ Sample Data Added Successfully!</h1>
        <p>10 sample students have been added with the new scoring system.</p>
        <p><strong>Scoring System:</strong> Assignments(10) + Midterm(20) + Internal(30) + End-term(40) = 100</p>
        <p><strong>Test Credentials:</strong></p>
        <ul>
            <li>Teacher: username='teacher', password='teacher123'</li>
            <li>Admin: username='admin', password='admin123'</li>
            <li>Students: username='student101', password='student123' (and similar for 102-110)</li>
        </ul>
        <p><a href="/login">Go to Login Page</a></p>
        """
        
    except Exception as e:
        return f"<h1>Error adding sample data:</h1><p>{str(e)}</p>"

# ---------- TEST DATABASE ROUTE ----------
@app.route("/test-db")
def test_db():
    """Test database connection and data"""
    conn = get_db_connection()
    
    users = conn.execute("SELECT * FROM users").fetchall()
    students = conn.execute("SELECT * FROM students").fetchall()
    
    conn.close()
    
    result = f"<h1>Database Test</h1>"
    result += f"<h2>Users ({len(users)})</h2>"
    for user in users:
        result += f"<p>{user['username']} - {user['role']} - Roll: {user['roll_no']}</p>"
    
    result += f"<h2>Students ({len(students)})</h2>"
    for student in students:
        total = (student['assignments_score'] + student['midterm_score'] + 
                student['internal_score'] + student['final_score'])
        result += f"<p>{student['name']} - Roll: {student['roll_no']} - Total: {total}/100</p>"
    
    result += "<p><a href='/add-sample-data'>Add Sample Data</a></p>"
    result += "<p><a href='/login'>Go to Login</a></p>"
    
    return result

if __name__ == "__main__":
    init_db_and_admin()
    app.run(host="0.0.0.0", port=5000, debug=True)