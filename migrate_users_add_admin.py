import sqlite3

conn = sqlite3.connect("database/student_system.db")
cur = conn.cursor()

# 1. Create new users table with admin role allowed
cur.execute("""
CREATE TABLE IF NOT EXISTS users_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin','teacher','student')) NOT NULL,
    roll_no INTEGER
);
""")

# 2. Copy data from old users table
cur.execute("""
INSERT INTO users_new (id, username, password, role, roll_no)
SELECT id, username, password, role, roll_no FROM users;
""")

# 3. Drop old users table
cur.execute("DROP TABLE users;")

# 4. Rename new table
cur.execute("ALTER TABLE users_new RENAME TO users;")

conn.commit()
conn.close()

print("Users table migrated successfully. Admin role is now allowed.")
