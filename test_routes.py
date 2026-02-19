#!/usr/bin/env python3
"""
Test script to verify all routes and functionality in the EduAI application
"""

import requests
import time
import sys
from urllib.parse import urljoin

BASE_URL = "http://127.0.0.1:5000"

def test_route(path, method="GET", data=None, expected_status=200, description=""):
    """Test a single route"""
    url = urljoin(BASE_URL, path)
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=5, allow_redirects=False)
        elif method == "POST":
            response = requests.post(url, data=data, timeout=5, allow_redirects=False)
        
        if response.status_code == expected_status:
            print(f"✅ {path} - {description}")
            return True
        else:
            print(f"❌ {path} - Expected {expected_status}, got {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {path} - Connection failed (is the server running?)")
        return False
    except Exception as e:
        print(f"❌ {path} - Error: {e}")
        return False

def test_all_routes():
    """Test all application routes"""
    print("🚀 Testing EduAI Application Routes\n")
    print("⚠️  Make sure the Flask app is running on http://127.0.0.1:5000\n")
    
    routes_to_test = [
        # Public routes
        ("/", "GET", None, 200, "Home page"),
        ("/login", "GET", None, 200, "Login page"),
        ("/predict", "GET", None, 200, "Prediction form"),
        ("/chatbot", "GET", None, 200, "Chatbot page"),
        
        # Routes that require authentication (should redirect to login)
        ("/teacher-dashboard", "GET", None, 302, "Teacher dashboard (redirect to login)"),
        ("/student-dashboard", "GET", None, 302, "Student dashboard (redirect to login)"),
        ("/admin-dashboard", "GET", None, 302, "Admin dashboard (redirect to login)"),
        ("/prediction-history", "GET", None, 302, "Prediction history (redirect to login)"),
        ("/student-history", "GET", None, 302, "Student history (redirect to login)"),
        
        # Logout (should redirect)
        ("/logout", "GET", None, 302, "Logout (redirect)"),
    ]
    
    passed = 0
    total = len(routes_to_test)
    
    for path, method, data, expected_status, description in routes_to_test:
        if test_route(path, method, data, expected_status, description):
            passed += 1
        time.sleep(0.1)  # Small delay between requests
    
    print(f"\n📊 Route Test Results: {passed}/{total} routes working correctly")
    
    if passed == total:
        print("🎉 All routes are accessible!")
    else:
        print("⚠️  Some routes may have issues.")
    
    return passed == total

def test_prediction_functionality():
    """Test the prediction functionality with sample data"""
    print("\n🧠 Testing ML Prediction Functionality")
    
    sample_data = {
        "attendance": "85",
        "assignments": "80", 
        "midterm": "75",
        "final": "78",
        "hours": "2.5"
    }
    
    return test_route("/predict", "POST", sample_data, 200, "ML Prediction with sample data")

def main():
    """Run all tests"""
    print("=" * 60)
    print("EduAI Application Route Testing")
    print("=" * 60)
    
    # Test basic routes
    routes_ok = test_all_routes()
    
    # Test prediction functionality
    prediction_ok = test_prediction_functionality()
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS:")
    print("=" * 60)
    
    if routes_ok and prediction_ok:
        print("🎉 ALL TESTS PASSED! The application is fully functional.")
        print("\n💡 You can now:")
        print("   • Visit http://127.0.0.1:5000 to use the app")
        print("   • Login with admin/admin123 for admin access")
        print("   • Test the ML prediction functionality")
        print("   • Use the AI chatbot for guidance")
    else:
        print("⚠️  Some functionality may not be working correctly.")
        print("   Please check the Flask application logs for errors.")
    
    print("\n🔗 Quick Links:")
    print(f"   • Home: {BASE_URL}")
    print(f"   • Login: {BASE_URL}/login")
    print(f"   • Predict: {BASE_URL}/predict")
    print(f"   • Chatbot: {BASE_URL}/chatbot")

if __name__ == "__main__":
    main()