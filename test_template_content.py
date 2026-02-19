#!/usr/bin/env python3
"""
Test template content on port 5001
"""

import requests

def test_template_content():
    """Test the template content on the debug server"""
    print("Testing template content on debug server (port 5001)...")
    
    try:
        response = requests.get("http://127.0.0.1:5001/")
        
        if response.status_code == 200:
            print("✅ Template loaded successfully")
            
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
            print(f"❌ Failed to load template: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to debug server")

if __name__ == "__main__":
    test_template_content()