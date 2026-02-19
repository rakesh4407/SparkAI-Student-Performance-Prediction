import sqlite3
from werkzeug.security import check_password_hash

# Connect to database
conn = sqlite3.connect('database/student_system.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Check all users
print("=== ALL USERS IN DATABASE ===")
users = cursor.execute('SELECT id, username, role FROM users').fetchall()
for user in users:
    print(f"ID: {user['id']}, Username: {user['username']}, Role: {user['role']}")

print("\n=== TEACHER ACCOUNTS ===")
teachers = cursor.execute('SELECT * FROM users WHERE role="teacher"').fetchall()
if teachers:
    for teacher in teachers:
        print(f"Username: {teacher['username']}")
        print(f"Role: {teacher['role']}")
        print(f"Password hash exists: {bool(teacher['password'])}")
        
        # Test password
        test_passwords = ['teacher123', 'teacher', 'Teacher123']
        for pwd in test_passwords:
            if check_password_hash(teacher['password'], pwd):
                print(f"✅ Password '{pwd}' works!")
            else:
                print(f"❌ Password '{pwd}' doesn't work")
        print()
else:
    print("❌ No teacher accounts found!")

conn.close()
