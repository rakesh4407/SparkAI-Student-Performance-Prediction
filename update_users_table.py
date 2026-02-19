import sqlite3

conn = sqlite3.connect("database/student_system.db")
cur = conn.cursor()

# Add roll_no column if not exists
try:
    cur.execute("ALTER TABLE users ADD COLUMN roll_no INTEGER;")
    print("Added roll_no column to users table.")
except:
    print("roll_no column already exists.")

conn.commit()
conn.close()
