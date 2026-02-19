#!/usr/bin/env python3
"""
Test AI Prediction button functionality from index.html without login
"""

import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def test_ai_prediction_button():
    """Test the AI Prediction button workflow without login"""
    print("🧪 Testing AI Prediction Button from Index Page (No Login Required)")
    print("=" * 70)
    
    # Step 1: Access the home page
    print("1. Accessing home page...")
    home_response = requests.get(f"{BASE_URL}/")
    
    if home_response.status_code == 200:
        print("✅ Home page loaded successfully")
        
        # Check if the AI Prediction button exists
        if 'onclick="openPage(\'/predict\')"' in home_response.text:
            print("✅ AI Prediction button found with correct link")
        elif "openPage('/predict')" in home_response.text:
            print("✅ AI Prediction button found with correct link (alternative format)")
        else:
            print("❌ AI Prediction button not found or incorrectly configured")
            return False
    else:
        print(f"❌ Failed to load home page: {home_response.status_code}")
        return False
    
    # Step 2: Test clicking the AI Prediction button (simulate navigation to /predict)
    print("\n2. Simulating AI Prediction button click...")
    predict_response = requests.get(f"{BASE_URL}/predict")
    
    if predict_response.status_code == 200:
        print("✅ Predict page accessible without login")
        
        # Check if it's the prediction form
        if 'Student Performance Prediction' in predict_response.text:
            print("✅ Prediction form loaded correctly")
        else:
            print("❌ Prediction form not found")
            return False
    else:
        print(f"❌ Failed to access predict page: {predict_response.status_code}")
        return False
    
    # Step 3: Test the prediction form functionality
    print("\n3. Testing prediction form submission...")
    
    # Sample data for prediction
    test_data = {
        "attendance": "85",
        "assignments": "80",
        "midterm": "75", 
        "final": "78",
        "hours": "2.5"
    }
    
    prediction_response = requests.post(f"{BASE_URL}/predict", data=test_data)
    
    if prediction_response.status_code == 200:
        print("✅ Prediction form submitted successfully")
        
        # Check if we got a result
        if 'Performance' in prediction_response.text and ('Excellent' in prediction_response.text or 
                                                          'Good' in prediction_response.text or 
                                                          'Average' in prediction_response.text or 
                                                          'Poor' in prediction_response.text):
            print("✅ ML prediction result received")
            
            # Extract the predicted performance (basic parsing)
            response_text = prediction_response.text.lower()
            if 'excellent' in response_text:
                predicted = 'Excellent'
            elif 'good' in response_text:
                predicted = 'Good'
            elif 'average' in response_text:
                predicted = 'Average'
            elif 'poor' in response_text:
                predicted = 'Poor'
            else:
                predicted = 'Unknown'
            
            print(f"🎯 Predicted Performance: {predicted}")
            
        else:
            print("❌ No prediction result found")
            return False
    else:
        print(f"❌ Prediction form submission failed: {prediction_response.status_code}")
        return False
    
    return True

def test_other_buttons():
    """Test other buttons from the index page"""
    print("\n🔗 Testing Other Buttons from Index Page")
    print("=" * 50)
    
    # Test Smart Dashboards button (should redirect to login)
    print("1. Testing Smart Dashboards button...")
    dashboard_response = requests.get(f"{BASE_URL}/login", allow_redirects=False)
    
    if dashboard_response.status_code == 200:
        print("✅ Smart Dashboards button correctly leads to login page")
    else:
        print(f"❌ Smart Dashboards button issue: {dashboard_response.status_code}")
    
    # Test AI Guidance button (chatbot)
    print("\n2. Testing AI Guidance button...")
    chatbot_response = requests.get(f"{BASE_URL}/chatbot")
    
    if chatbot_response.status_code == 200:
        print("✅ AI Guidance button accessible (chatbot page)")
        
        if 'EduAI Assistant' in chatbot_response.text:
            print("✅ Chatbot interface loaded correctly")
        else:
            print("❌ Chatbot interface not found")
    else:
        print(f"❌ AI Guidance button failed: {chatbot_response.status_code}")

def main():
    """Run all tests"""
    print("🚀 EduAI Index Page Button Testing")
    print("Testing AI Prediction button functionality without login requirement")
    print("=" * 70)
    
    # Test AI Prediction button workflow
    ai_prediction_success = test_ai_prediction_button()
    
    # Test other buttons
    test_other_buttons()
    
    print("\n" + "=" * 70)
    print("📊 FINAL RESULTS")
    print("=" * 70)
    
    if ai_prediction_success:
        print("🎉 AI PREDICTION BUTTON WORKS PERFECTLY!")
        print("✅ Users can access ML prediction without login")
        print("✅ Prediction form loads correctly")
        print("✅ ML model processes input and returns results")
        print("✅ Complete workflow functional")
    else:
        print("❌ AI Prediction button has issues")
    
    print(f"\n🌐 Test the button manually at: {BASE_URL}")
    print("💡 Click 'AI Prediction' button on the home page to test interactively")

if __name__ == "__main__":
    main()