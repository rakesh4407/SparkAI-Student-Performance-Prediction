#!/usr/bin/env python3
"""
Test Flask login function directly
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app functions
from app import get_user_by_username
from werkzeug.security import check_password_hash

def test_flask_login_function():
    print("Testing Flask app's get_user_by_username function:")
    
    test_users = ["admin", "teacher1", "student1"]
    
    for username in test_users:
        print(f"\nTesting {username}:")
        user = get_user_by_username(username)
        
        if user:
            print(f"  User found: {user['username']} ({user['role']})")
            
            # Test password
            if username == "admin":
                password = "admin123"
            elif username.startswith("teacher"):
                password = "teacher123"
            else:
                password = "student123"
            
            password_valid = check_password_hash(user["password"], password)
            print(f"  Password '{password}' valid: {password_valid}")
        else:
            print(f"  User not found!")

if __name__ == "__main__":
    test_flask_login_function()