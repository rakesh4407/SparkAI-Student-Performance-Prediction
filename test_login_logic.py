#!/usr/bin/env python3
"""
Test the login logic directly
"""

import sqlite3
from werkzeug.security import check_password_hash

def get_db_connection():
    conn = sqlite3.connect("database/student_system.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    return user

def test_login_logic(username, password, role):
    print(f"Testing login logic for {username} ({role})")
    
    user = get_user_by_username(username)
    print(f"User found: {user is not None}")
    
    if user:
        print(f"User role: {user['role']}")
        print(f"Role matches: {user['role'] == role}")
        
        password_valid = check_password_hash(user["password"], password)
        print(f"Password valid: {password_valid}")
        
        login_success = user and user["role"] == role and password_valid
        print(f"Login should succeed: {login_success}")
    else:
        print("User not found!")
    
    print()

# Test all accounts
test_login_logic("admin", "admin123", "admin")
test_login_logic("teacher1", "teacher123", "teacher")
test_login_logic("student1", "student123", "student")