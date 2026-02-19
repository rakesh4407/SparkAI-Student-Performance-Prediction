#!/usr/bin/env python3
"""Quick test to verify teacher login works"""

import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

print("=== TEACHER LOGIN TEST ===\n")

# Check if server is running
try:
    response = requests.get(BASE_URL, timeout=2)
    print("✅ Server is running!")
except requests.exceptions.ConnectionError:
    print("❌ Server is NOT running!")
    print("\nPlease start the server first:")
    print("  python app.py")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error connecting to server: {e}")
    sys.exit(1)

# Test teacher login
print("\nTesting teacher login...")
session = requests.Session()

# Test with teacher account
login_data = {
    "role": "teacher",
    "username": "teacher",
    "password": "teacher123"
}

try:
    response = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=False)
    
    if response.status_code == 302:  # Redirect means success
        redirect_url = response.headers.get('Location', '')
        if 'teacher-dashboard' in redirect_url:
            print("✅ Teacher login SUCCESSFUL!")
            print(f"   Redirecting to: {redirect_url}")
            
            # Try to access dashboard
            dashboard_response = session.get(f"{BASE_URL}/teacher-dashboard")
            if dashboard_response.status_code == 200:
                print("✅ Teacher dashboard accessible!")
            else:
                print(f"⚠️  Dashboard returned status: {dashboard_response.status_code}")
        else:
            print(f"⚠️  Unexpected redirect: {redirect_url}")
    else:
        print(f"❌ Login failed with status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        
except Exception as e:
    print(f"❌ Error during login test: {e}")

print("\n=== CREDENTIALS TO USE ===")
print("Username: teacher")
print("Password: teacher123")
print("Role: Teacher (select from dropdown)")
print("\nOR")
print("\nUsername: teacher1")
print("Password: teacher123")
print("Role: Teacher (select from dropdown)")
