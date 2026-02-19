import sqlite3
from werkzeug.security import check_password_hash

conn = sqlite3.connect("database/student_system.db")
cur = conn.cursor()

users = cur.execute("SELECT username, password, role FROM users").fetchall()

print("Checking password hashes:")
for username, password_hash, role in users:
    print(f"\nUser: {username} ({role})")
    print(f"Hash: {password_hash[:50]}...")
    
    # Test password verification
    if username == "admin":
        test_password = "admin123"
    elif username.startswith("teacher"):
        test_password = "teacher123"
    elif username.startswith("student"):
        test_password = "student123"
    else:
        test_password = "unknown"
    
    is_valid = check_password_hash(password_hash, test_password)
    print(f"Password '{test_password}' valid: {is_valid}")

conn.close()