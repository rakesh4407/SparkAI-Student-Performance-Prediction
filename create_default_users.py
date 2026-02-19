import sqlite3
from werkzeug.security import generate_password_hash

# Connect to DB
conn = sqlite3.connect("database/student_system.db")
cur = conn.cursor()

# Create a default teacher user
username = "teacher1"
plain_password = "teacher123"  # you will use this to login
role = "teacher"

password_hash = generate_password_hash(plain_password)

# Insert user (ignore if exists)
cur.execute("""
INSERT OR IGNORE INTO users (username, password, role)
VALUES (?, ?, ?)
""", (username, password_hash, role))

conn.commit()
conn.close()

print("Default teacher created -> username: teacher1, password: teacher123")
