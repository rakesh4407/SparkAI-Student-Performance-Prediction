#!/usr/bin/env python3
"""
SparkAI Application Startup Script
Simple script to start the EduAI Student Performance Prediction application
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask', 'pandas', 'numpy', 'sklearn', 'joblib', 'reportlab', 'werkzeug'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {missing_packages}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def check_project_files():
    """Check if required project files exist"""
    print("🔍 Checking project files...")
    
    required_files = [
        'app.py',
        'ml_model/performance_model.joblib',
        'ml_model/label_encoder.joblib',
        'templates/index.html',
        'templates/login.html'
    ]
    
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files are present")
    return True

def start_application():
    """Start the Flask application"""
    print("🚀 Starting EduAI Application...")
    print("=" * 50)
    
    try:
        # Import and run the Flask app
        from app import app, init_db_and_admin
        
        # Initialize database and admin user
        print("📊 Initializing database...")
        init_db_and_admin()
        print("✅ Database initialized")
        
        print("\n🌐 Starting web server...")
        print("📍 Application will be available at: http://127.0.0.1:5000")
        print("\n🔑 Login Credentials:")
        print("   Admin: admin / admin123")
        print("   Teacher: teacher1 / teacher123")
        print("   Student: student1 / student123")
        print("\n💡 Features available without login:")
        print("   • AI Prediction: http://127.0.0.1:5000/predict")
        print("   • AI Chatbot: http://127.0.0.1:5000/chatbot")
        
        print("\n" + "=" * 50)
        print("🎉 EduAI is now running!")
        print("Press Ctrl+C to stop the application")
        print("=" * 50)
        
        # Start the Flask app
        app.run(host='0.0.0.0', port=5000, debug=False)
        
    except KeyboardInterrupt:
        print("\n\n👋 EduAI application stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)

def main():
    """Main startup function"""
    print("🎓 SparkAI - Student Performance Prediction System")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check project files
    if not check_project_files():
        sys.exit(1)
    
    # Start the application
    start_application()

if __name__ == "__main__":
    main()