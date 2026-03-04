from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

# Test teacher login
conn = sqlite3.connect('database/student_system.db')
cursor = conn.cursor()

# 1. Check teacher exists
cursor.execute("SELECT * FROM users WHERE role = 'teacher'")
teacher = cursor.fetchone()

if teacher:
    print(f"Teacher found: {teacher[1]}")
    print(f"Password hash: {teacher[2][:50]}...")
else:
    print("No teacher found! Creating one...")
    password = "teacher123"
    hashed = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        ("teacher1", hashed, "teacher")
    )
    conn.commit()
    print(f"Created teacher: teacher1 / {password}")

# 2. Check students data
cursor.execute("SELECT COUNT(*) FROM students")
student_count = cursor.fetchone()[0]
print(f"Students in database: {student_count}")

conn.close()