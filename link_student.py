import sqlite3

conn = sqlite3.connect("database/student_system.db")
cur = conn.cursor()

# LINK USER → STUDENT
cur.execute("""
UPDATE users
SET roll_no = ?
WHERE username = ? AND role = 'student'
""", (11, "rohan01"))

conn.commit()
conn.close()

print("Student user linked successfully.")
