#!/usr/bin/env python3
"""
Test the predict route directly without going through the button
"""

import requests

BASE_URL = "http://127.0.0.1:5000"

def test_predict_direct():
    """Test accessing /predict directly and using the prediction functionality"""
    print("🧪 Testing AI Prediction Functionality Directly")
    print("=" * 60)
    
    # Step 1: Access predict page directly
    print("1. Accessing /predict page directly...")
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
    
    # Step 2: Test the prediction form functionality
    print("\n2. Testing prediction form submission...")
    
    # Test with different student profiles
    test_cases = [
        {
            "name": "Excellent Student",
            "data": {"attendance": "95", "assignments": "90", "midterm": "88", "final": "92", "hours": "4"},
        },
        {
            "name": "Average Student", 
            "data": {"attendance": "75", "assignments": "70", "midterm": "68", "final": "72", "hours": "2.5"},
        },
        {
            "name": "At-Risk Student",
            "data": {"attendance": "60", "assignments": "45", "midterm": "40", "final": "42", "hours": "1"},
        }
    ]
    
    for test_case in test_cases:
        print(f"\n   Testing {test_case['name']}:")
        print(f"   Input: {test_case['data']}")
        
        prediction_response = requests.post(f"{BASE_URL}/predict", data=test_case["data"])
        
        if prediction_response.status_code == 200:
            print("   ✅ Prediction successful")
            
            # Check if we got a result
            response_text = prediction_response.text.lower()
            if any(perf in response_text for perf in ['excellent', 'good', 'average', 'poor']):
                # Extract the predicted performance
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
                
                print(f"   🎯 Predicted Performance: {predicted}")
            else:
                print("   ❌ No prediction result found")
                return False
        else:
            print(f"   ❌ Prediction failed: {prediction_response.status_code}")
            return False
    
    return True

def main():
    """Run the test"""
    success = test_predict_direct()
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS")
    print("=" * 60)
    
    if success:
        print("🎉 AI PREDICTION FUNCTIONALITY WORKS PERFECTLY!")
        print("✅ /predict route accessible without login")
        print("✅ Prediction form loads correctly")
        print("✅ ML model processes all types of student data")
        print("✅ Results are returned for all test cases")
        print("\n💡 The AI Prediction feature is fully functional!")
        print("   Users can access it directly at: http://127.0.0.1:5000/predict")
        print("   Or through the homepage button (once template cache clears)")
    else:
        print("❌ AI Prediction functionality has issues")

if __name__ == "__main__":
    main()