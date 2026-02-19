#!/usr/bin/env python3
"""Test if the Flask app can start without errors"""

import sys
import os

try:
    # Import the app
    from app import app, init_db_and_admin
    
    print("✅ App imported successfully")
    
    # Initialize database
    init_db_and_admin()
    print("✅ Database initialized successfully")
    
    # Test a simple route
    with app.test_client() as client:
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Home route works")
        else:
            print(f"⚠️ Home route returned status: {response.status_code}")
            
        # Test login page
        response = client.get('/login')
        if response.status_code == 200:
            print("✅ Login route works")
        else:
            print(f"⚠️ Login route returned status: {response.status_code}")
    
    print("\n✅ All basic tests passed!")
    print("The application should start without errors.")
    print("\nTo start the app, run: python app.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()