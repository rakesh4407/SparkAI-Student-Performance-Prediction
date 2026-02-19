#!/usr/bin/env python3
"""
Verification script to ensure all test/test_score references have been renamed to internal_marks
"""

import os
import re
import glob

def check_file_for_old_terms(filepath, patterns):
    """Check a file for old terminology"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        found = []
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                found.append((pattern_name, len(matches)))
        
        return found
    except Exception as e:
        return [("ERROR", str(e))]

def main():
    print("="*70)
    print("VERIFICATION: Checking for old 'test' terminology")
    print("="*70)
    
    # Patterns to search for (excluding test script files)
    patterns = {
        'test_score': r'\btest_score\b',
        'Test_score': r'\bTest_score\b',
        'standalone_test': r'(?<!_)(?<!/)test(?!_)(?!\.py)(?!ing)(?!s\b)',  # Avoid test.py, testing, tests
    }
    
    # Files to check
    files_to_check = []
    files_to_check.append('app.py')
    files_to_check.extend(glob.glob('templates/*.html'))
    
    print(f"\nChecking {len(files_to_check)} files...\n")
    
    issues_found = False
    
    for filepath in files_to_check:
        if not os.path.exists(filepath):
            continue
            
        found = check_file_for_old_terms(filepath, patterns)
        
        if found:
            issues_found = True
            print(f"⚠️  {filepath}")
            for pattern_name, count in found:
                print(f"   - Found '{pattern_name}': {count} occurrence(s)")
    
    print("\n" + "="*70)
    
    if not issues_found:
        print("✅ VERIFICATION PASSED")
        print("   No old 'test' terminology found in main files!")
        print("   All references have been successfully renamed to 'internal_marks'")
    else:
        print("⚠️  VERIFICATION INCOMPLETE")
        print("   Some old terminology still exists (see above)")
        print("   Note: Test script files are intentionally excluded")
    
    print("="*70)
    
    # Check database
    print("\nChecking database schema...")
    import sqlite3
    try:
        conn = sqlite3.connect('database/student_system.db')
        cursor = conn.cursor()
        
        # Check students table
        cursor.execute("PRAGMA table_info(students)")
        students_cols = [col[1] for col in cursor.fetchall()]
        
        # Check prediction_history table
        cursor.execute("PRAGMA table_info(prediction_history)")
        history_cols = [col[1] for col in cursor.fetchall()]
        
        if 'internal_marks' in students_cols and 'internal_marks' in history_cols:
            print("✅ Database schema updated correctly")
            print(f"   - students table has 'internal_marks' column")
            print(f"   - prediction_history table has 'internal_marks' column")
        else:
            print("❌ Database schema issue detected")
            if 'test_score' in students_cols or 'test_score' in history_cols:
                print("   - Old 'test_score' column still exists!")
        
        conn.close()
    except Exception as e:
        print(f"❌ Database check failed: {e}")
    
    print("\n" + "="*70)
    print("Verification complete!")
    print("="*70)

if __name__ == "__main__":
    main()
