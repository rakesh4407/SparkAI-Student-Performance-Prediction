#!/usr/bin/env python3
"""
Simple test to check authentication behavior
"""

import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

def test_auth():
    print("Testing authentication behavior...")
    
    # Test accessing protected route without login
    response = requests.get(f"{BASE_URL}/teacher-dashboard")
    print(f"Teacher dashboard without login: Status {response.status_code}")
    print(f"URL after redirect: {response.url}")
    
    if "login" in response.url:
        print("✅ Properly redirected to login")
    else:
        print("❌ Not redirected to login - authentication issue!")
        print(f"Response content preview: {response.text[:200]}...")
    
    # Test login functionality
    print("\nTesting login...")
    session = requests.Session()
    
    # Get login page first
    login_page = session.get(f"{BASE_URL}/login")
    print(f"Login page: Status {login_page.status_code}")
    
    # Try to login with admin credentials
    login_data = {
        "role": "admin",
        "username": "admin", 
        "password": "admin123"
    }
    
    login_response = session.post(f"{BASE_URL}/login", data=login_data)
    print(f"Login attempt: Status {login_response.status_code}")
    print(f"URL after login: {login_response.url}")
    
    if "admin-dashboard" in login_response.url:
        print("✅ Successfully logged in and redirected to admin dashboard")
        
        # Now test accessing teacher dashboard while logged in as admin
        teacher_dash = session.get(f"{BASE_URL}/teacher-dashboard")
        print(f"Teacher dashboard as admin: Status {teacher_dash.status_code}")
        
    else:
        print("❌ Login failed or incorrect redirect")

if __name__ == "__main__":
    test_auth()