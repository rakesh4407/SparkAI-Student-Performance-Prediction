import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("database/student_system.db")
cur = conn.cursor()

# Create test users
test_users = [
    ("teacher1", "teacher123", "teacher", None),
    ("student1", "student123", "student", 1),  # Link to roll_no 1 (Alice)
    ("student2", "student123", "student", 2),  # Link to roll_no 2 (Bob)
]

for username, password, role, roll_no in test_users:
    # Check if user already exists
    exists = cur.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    
    if not exists:
        cur.execute("""
            INSERT INTO users (username, password, role, roll_no)
            VALUES (?, ?, ?, ?)
        """, (username, generate_password_hash(password), role, roll_no))
        print(f"Created user: {username} ({role})")
    else:
        print(f"User {username} already exists")

conn.commit()
conn.close()

print("\nTest users created successfully!")
print("Login credentials:")
print("Admin: admin / admin123")
print("Teacher: teacher1 / teacher123") 
print("Student: student1 / student123 (Alice)")
print("Student: student2 / student123 (Bob)")