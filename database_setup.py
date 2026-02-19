import sqlite3
import os

# Create database directory if it doesn't exist
os.makedirs("database", exist_ok=True)

# Create database connection
conn = sqlite3.connect("database/student_system.db")
cur = conn.cursor()

print("="*60)
print("DATABASE SETUP")
print("="*60)

# ------------------ USERS TABLE (LOGIN) ------------------
print("\n📦 Creating users table...")
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT CHECK(role IN ('admin', 'teacher', 'student')),
    roll_no INTEGER
)
""")
print("✅ Users table ready")

# ------------------ STUDENTS TABLE (UPDATED with internal_score) ------------------
print("\n📦 Creating students table...")
cur.execute("""
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
print("✅ Students table ready (includes internal_score)")

# ------------------ PREDICTION HISTORY TABLE (UPDATED with all columns) ------------------
print("\n📦 Creating prediction_history table...")
cur.execute("""
CREATE TABLE IF NOT EXISTS prediction_history (
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
)
""")
print("✅ Prediction history table ready (includes all score columns)")

# ------------------ CHECK IF TABLES WERE CREATED ------------------
print("\n" + "="*60)
print("VERIFYING TABLES")
print("="*60)

# Get list of tables
tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print(f"\n📋 Tables in database:")
for table in tables:
    print(f"   - {table[0]}")

# Show schema for each table
print("\n📊 Table schemas:")
for table in tables:
    table_name = table[0]
    print(f"\n   {table_name}:")
    columns = cur.execute(f"PRAGMA table_info({table_name})").fetchall()
    for col in columns:
        print(f"     • {col[1]} ({col[2]})")

conn.commit()
print("\n" + "="*60)
print("✅ DATABASE SETUP COMPLETE!")
print("="*60)
print("\n📝 Summary of changes:")
print("   • Added internal_score column to students table (0-30 marks)")
print("   • Updated prediction_history with detailed score columns:")
print("     - assignments_score (0-10)")
print("     - midterm_score (0-20)") 
print("     - internal_score (0-30)")
print("     - predicted_endterm (0-40)")
print("     - total_score (0-100)")
print("     - predicted_label (performance category)")
print("     - date_time (timestamp)")

conn.close()

print("\n💡 Next steps:")
print("   1. Run your Flask app: python app.py")
print("   2. Add sample data: Visit http://localhost:5000/add-sample-data")
print("   3. Start making predictions with the new scoring system!")