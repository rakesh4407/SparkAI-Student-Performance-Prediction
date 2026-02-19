import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("database/student_system.db")
cur = conn.cursor()

# SAMPLE student logins (roll_no = same value for mapping)
students = [
    ("alice01", "alice123", "student", 1),
    ("bob01", "bob123", "student", 2),
    ("charlie01", "charlie123", "student", 3),
]

for username, password, role, roll in students:
    cur.execute("""
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES (?, ?, ?)
    """, (username, generate_password_hash(password), role))

conn.commit()
conn.close()

print("Student logins created successfully!")
print("Credentials:")
print("alice01 / alice123")
print("bob01 / bob123")
print("charlie01 / charlie123")
