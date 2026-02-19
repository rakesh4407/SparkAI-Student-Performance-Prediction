import sqlite3

conn = sqlite3.connect("database/student_system.db")
cur = conn.cursor()

rows = cur.execute("SELECT id, username, role FROM users").fetchall()

print("Users found:")
for r in rows:
    print(r)

conn.close()
