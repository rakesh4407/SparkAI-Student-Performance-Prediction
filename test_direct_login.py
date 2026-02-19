#!/usr/bin/env python3
"""
Test login logic directly with Flask app context
"""

import sys
import os
from werkzeug.test import Client
from werkzeug.wrappers import Response

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app
from app import app

def test_direct_login():
    """Test login using Flask's test client"""
    print("Testing login using Flask test client:")
    
    with app.test_client() as client:
        # Test admin login
        print("\nTesting admin login:")
        response = client.post('/login', data={
            'role': 'admin',
            'username': 'admin',
            'password': 'admin123'
        })
        print(f"Status: {response.status_code}")
        if response.status_code == 302:
            print(f"Redirect to: {response.location}")
        else:
            print("Login failed")
        
        # Test teacher login
        print("\nTesting teacher login:")
        response = client.post('/login', data={
            'role': 'teacher',
            'username': 'teacher1',
            'password': 'teacher123'
        })
        print(f"Status: {response.status_code}")
        if response.status_code == 302:
            print(f"Redirect to: {response.location}")
        else:
            print("Login failed")
            if b"Invalid login details" in response.data:
                print("Error: Invalid login details")
        
        # Test student login
        print("\nTesting student login:")
        response = client.post('/login', data={
            'role': 'student',
            'username': 'student1',
            'password': 'student123'
        })
        print(f"Status: {response.status_code}")
        if response.status_code == 302:
            print(f"Redirect to: {response.location}")
        else:
            print("Login failed")
            if b"Invalid login details" in response.data:
                print("Error: Invalid login details")

if __name__ == "__main__":
    test_direct_login()