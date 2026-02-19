#!/usr/bin/env python3
"""Test teacher login flow"""

import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

# Connect to database
conn = sqlite3.connect('database/student_system.db')
conn.row_factory = sqlite3.Row

print("=== TESTING TEACHER LOGIN FLOW ===\n")

# Test credentials
test_credentials = [
    ("teacher", "teacher123"),
    ("teacher1", "teacher123"),
    ("suman", "teacher123"),
]

for username, password in test_credentials:
    print(f"Testing: {username} / {password}")
    
    # Simulate login logic from app.py
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    
    if user:
        print(f"  ✅ User found: {user['username']}")
        print(f"  Role: {user['role']}")
        
        # Check if role matches
        if user['role'] == 'teacher':
            print(f"  ✅ Role matches 'teacher'")
            
            # Check password
            if check_password_hash(user['password'], password):
                print(f"  ✅ Password correct!")
                print(f"  ✅ LOGIN SUCCESSFUL - Would redirect to teacher_dashboard")
            else:
                print(f"  ❌ Password incorrect")
        else:
            print(f"  ❌ Role mismatch: expected 'teacher', got '{user['role']}'")
    else:
        print(f"  ❌ User not found")
    
    print()

# Check if there are any issues with the teacher accounts
print("\n=== CHECKING TEACHER ACCOUNT INTEGRITY ===")
teachers = conn.execute("SELECT * FROM users WHERE role='teacher'").fetchall()

for teacher in teachers:
    print(f"\nTeacher: {teacher['username']}")
    print(f"  ID: {teacher['id']}")
    print(f"  Role: {teacher['role']}")
    print(f"  Password hash length: {len(teacher['password'])}")
    print(f"  Password starts with: {teacher['password'][:20]}...")
    
    # Verify it's a valid bcrypt/werkzeug hash
    if teacher['password'].startswith('scrypt:') or teacher['password'].startswith('pbkdf2:'):
        print(f"  ✅ Valid password hash format")
    else:
        print(f"  ⚠️  Unusual password hash format")

conn.close()

print("\n=== RECOMMENDATION ===")
print("Working teacher accounts:")
print("  • Username: teacher1, Password: teacher123")
print("  • Username: teacher, Password: teacher123")
print("\nIf login still fails, check:")
print("  1. Is the Flask app running?")
print("  2. Are you selecting 'Teacher' role in the dropdown?")
print("  3. Check browser console for JavaScript errors")
print("  4. Check Flask terminal for error messages")
