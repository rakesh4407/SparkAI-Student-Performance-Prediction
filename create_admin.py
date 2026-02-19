import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("database/student_system.db")
cur = conn.cursor()

username = "admin"
password = generate_password_hash("admin123")
role = "admin"

# Check if admin already exists
exists = cur.execute(
    "SELECT * FROM users WHERE username = ?", (username,)
).fetchone()

if exists:
    print("Admin already exists.")
else:
    cur.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
    """, (username, password, role))
    conn.commit()
    print("Admin user created successfully.")

conn.close()
