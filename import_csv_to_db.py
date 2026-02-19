import sqlite3
import pandas as pd

# Load CSV
df = pd.read_csv("student_data.csv")

# Clean the data - remove rows with NaN values
df = df.dropna()

# Connect to DB
conn = sqlite3.connect("database/student_system.db")
cur = conn.cursor()

# Clear old data to avoid duplicates
cur.execute("DELETE FROM students")

# Insert CSV data into students table
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO students 
        (roll_no, name, attendance, assignments_score, midterm_score, final_score, study_hours, performance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        int(row["roll_no"]),
        row["name"],
        float(row["attendance"]),
        float(row["assignments_score"]),
        float(row["midterm_score"]),
        float(row["final_score"]),
        float(row["study_hours"]),
        row["performance"]
    ))

conn.commit()
conn.close()

print("CSV data imported successfully into SQLite database!")
