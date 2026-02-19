#!/usr/bin/env python3
"""
Check index content with cache busting
"""

import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def check_index_nocache():
    """Check index content with cache busting"""
    print("Checking index page content with cache busting...")
    
    # Add timestamp to bust cache
    timestamp = int(time.time())
    response = requests.get(f"{BASE_URL}/?t={timestamp}", headers={
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    })
    
    if response.status_code == 200:
        print("✅ Index page loaded successfully")
        
        # Check for the correct Flask routes
        content = response.text
        
        if "onclick=\"openPage('/predict')\"" in content:
            print("✅ AI Prediction button has correct Flask route")
        elif "onclick=\"openPage('predict.html')\"" in content:
            print("❌ AI Prediction button still has .html link")
        else:
            print("❌ AI Prediction button not found")
        
        if "onclick=\"openPage('/login')\"" in content:
            print("✅ Smart Dashboards button has correct Flask route")
        elif "onclick=\"openPage('student_dashboard.html')\"" in content:
            print("❌ Smart Dashboards button still has .html link")
        else:
            print("❌ Smart Dashboards button not found")
            
        if "onclick=\"openPage('/chatbot')\"" in content:
            print("✅ AI Guidance button has correct Flask route")
        elif "onclick=\"openPage('chatbot.html')\"" in content:
            print("❌ AI Guidance button still has .html link")
        else:
            print("❌ AI Guidance button not found")
            
    else:
        print(f"❌ Failed to load index page: {response.status_code}")

if __name__ == "__main__":
    check_index_nocache()