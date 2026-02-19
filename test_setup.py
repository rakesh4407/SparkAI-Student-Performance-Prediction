#!/usr/bin/env python3
"""
Test script to verify the EduAI project setup
"""

import os
import sys
import sqlite3
from pathlib import Path

def test_project_structure():
    """Test if all required directories and files exist"""
    print("🔍 Testing project structure...")
    
    required_files = [
        "app.py",
        "model_train.py", 
        "requirements.txt",
        "student_data.csv",
        "ml_model/performance_model.joblib",
        "ml_model/label_encoder.joblib"
    ]
    
    required_dirs = [
        "templates",
        "static", 
        "ml_model"
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    for dir in required_dirs:
        if not os.path.exists(dir):
            missing_dirs.append(dir)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
        
    print("✅ All required files and directories exist")
    return True

def test_dependencies():
    """Test if all required Python packages can be imported"""
    print("\n🔍 Testing dependencies...")
    
    required_packages = [
        "flask",
        "pandas", 
        "numpy",
        "sklearn",
        "joblib",
        "reportlab",
        "werkzeug"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "sklearn":
                __import__("sklearn")
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {missing_packages}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def test_model_files():
    """Test if ML model files can be loaded"""
    print("\n🔍 Testing ML model files...")
    
    try:
        import joblib
        model = joblib.load("ml_model/performance_model.joblib")
        encoder = joblib.load("ml_model/label_encoder.joblib")
        print("✅ ML model files loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error loading model files: {e}")
        print("💡 Run: python model_train.py")
        return False

def test_database_setup():
    """Test database setup"""
    print("\n🔍 Testing database setup...")
    
    try:
        # Create database directory if it doesn't exist
        os.makedirs("database", exist_ok=True)
        
        # Test database connection
        conn = sqlite3.connect("database/student_system.db")
        cursor = conn.cursor()
        
        # Test if we can create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        """)
        
        cursor.execute("DROP TABLE test_table")
        conn.commit()
        conn.close()
        
        print("✅ Database setup working correctly")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 EduAI Project Setup Test\n")
    
    tests = [
        test_project_structure,
        test_dependencies,
        test_model_files,
        test_database_setup
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The project is ready to run.")
        print("💡 To start the application, run: python app.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()