#!/usr/bin/env python3
"""
Debug login issues
"""

import requests

BASE_URL = "http://127.0.0.1:5000"

def debug_login(username, password, role):
    print(f"Debugging login for {username} ({role})")
    
    session = requests.Session()
    
    # Get login page first
    login_page = session.get(f"{BASE_URL}/login")
    print(f"Login page status: {login_page.status_code}")
    
    # Try login
    login_data = {
        "role": role,
        "username": username,
        "password": password
    }
    
    print(f"Sending login data: {login_data}")
    
    response = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=False)
    print(f"Login response status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    
    if response.status_code == 302:
        print(f"Redirect location: {response.headers.get('Location')}")
    else:
        print(f"Response content preview: {response.text[:500]}")
        # Check for error message
        if "Invalid login details" in response.text:
            print("❌ Login failed with 'Invalid login details' error")
        elif "error" in response.text.lower():
            print("❌ Some error occurred during login")
            
        # Check if the form data was received correctly
        if f'value="{username}"' in response.text:
            print("✅ Username was preserved in form")
        else:
            print("❌ Username was not preserved in form")
            
        if f'value="{role}"' in response.text or f'selected' in response.text:
            print("✅ Role was preserved in form")
        else:
            print("❌ Role was not preserved in form")

# Test all accounts
debug_login("admin", "admin123", "admin")
print()
debug_login("teacher1", "teacher123", "teacher") 
print()
debug_login("student1", "student123", "student")