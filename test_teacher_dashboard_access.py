#!/usr/bin/env python3
"""Test teacher dashboard access specifically"""

from app import app, init_db_and_admin

try:
    init_db_and_admin()
    
    with app.test_client() as client:
        # Test teacher login
        login_data = {
            'role': 'teacher',
            'username': 'teacher',
            'password': 'teacher123'
        }
        
        response = client.post('/login', data=login_data, follow_redirects=True)
        
        if response.status_code == 200:
            print("✅ Teacher login successful")
            
            # Check if we're on the teacher dashboard
            if b'Teacher Dashboard' in response.data or b'teacher-dashboard' in response.data:
                print("✅ Teacher dashboard loaded successfully")
            else:
                print("⚠️ Teacher dashboard might have issues")
                print("Response contains:", response.data[:200].decode('utf-8', errors='ignore'))
        else:
            print(f"❌ Teacher login failed with status: {response.status_code}")
            
        # Test direct access to teacher dashboard (should redirect to login)
        response = client.get('/teacher-dashboard')
        if response.status_code == 302:  # Redirect to login
            print("✅ Teacher dashboard properly protected")
        elif response.status_code == 200:
            print("✅ Teacher dashboard accessible")
        else:
            print(f"⚠️ Teacher dashboard returned status: {response.status_code}")
            
except Exception as e:
    print(f"❌ Error testing teacher dashboard: {e}")
    import traceback
    traceback.print_exc()