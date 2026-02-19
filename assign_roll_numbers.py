import sqlite3

conn = sqlite3.connect("database/student_system.db")
cur = conn.cursor()

# Map username → roll_no
roll_map = {
    "alice01": 1,
    "bob01": 2,
    "charlie01": 3
}

for username, roll in roll_map.items():
    cur.execute("UPDATE users SET roll_no = ? WHERE username = ?", (roll, username))

conn.commit()
conn.close()

print("Roll numbers assigned to student accounts successfully!")
