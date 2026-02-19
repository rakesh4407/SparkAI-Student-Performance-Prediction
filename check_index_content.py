#!/usr/bin/env python3
"""
Check the actual content of the index page being served
"""

import requests

BASE_URL = "http://127.0.0.1:5000"

def check_index_content():
    """Check what's actually being served on the index page"""
    print("Checking actual index page content...")
    
    response = requests.get(f"{BASE_URL}/")
    
    if response.status_code == 200:
        print("✅ Index page loaded successfully")
        print(f"Content length: {len(response.text)} characters")
        
        # Look for AI Prediction button
        if "AI Prediction" in response.text:
            print("✅ 'AI Prediction' text found")
        else:
            print("❌ 'AI Prediction' text not found")
        
        # Look for predict link
        if "/predict" in response.text:
            print("✅ '/predict' link found")
        else:
            print("❌ '/predict' link not found")
        
        # Look for openPage function
        if "openPage" in response.text:
            print("✅ 'openPage' function found")
        else:
            print("❌ 'openPage' function not found")
        
        # Show the features section
        print("\n--- Features section content ---")
        lines = response.text.split('\n')
        in_features = False
        for line in lines:
            if 'id="features"' in line:
                in_features = True
            elif in_features and '</section>' in line:
                print(line.strip())
                break
            elif in_features:
                print(line.strip())
        
        # Show any buttons found
        print("\n--- All buttons found ---")
        for line in lines:
            if '<button' in line.lower():
                print(line.strip())
    else:
        print(f"❌ Failed to load index page: {response.status_code}")

if __name__ == "__main__":
    check_index_content()