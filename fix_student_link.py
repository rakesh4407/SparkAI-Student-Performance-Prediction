import sqlite3

conn = sqlite3.connect("database/student_system.db")
cur = conn.cursor()

# Example: link username 'alice' to roll_no 1
cur.execute("""
UPDATE users
SET roll_no = 1
WHERE username = 'alice' AND role = 'student'
""")

conn.commit()
conn.close()

print("Student linked successfully.")
