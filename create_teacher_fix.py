from werkzeug.security import generate_password_hash
import sqlite3

conn = sqlite3.connect('database/student_system.db')
cursor = conn.cursor()

# Check if teacher already exists
cursor.execute("SELECT * FROM users WHERE role = 'teacher'")
existing = cursor.fetchone()

if existing:
    print(f"Teacher already exists: {existing[1]} (ID: {existing[0]})")
else:
    # Create teacher with hashed password
    password = "teacher123"
    hashed_password = generate_password_hash(password)
    
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        ("teacher1", hashed_password, "teacher")
    )
    conn.commit()
    print(f"Teacher created: teacher1 / {password}")

conn.close()