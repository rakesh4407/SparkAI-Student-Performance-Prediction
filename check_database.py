#!/usr/bin/env python3
"""Check database status"""

import sqlite3
import os

DB_PATH = 'database/student_system.db'

try:
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f'✅ Database exists with tables: {[t[0] for t in tables]}')
        
        # Check students table
        cursor.execute('PRAGMA table_info(students)')
        columns = [col[1] for col in cursor.fetchall()]
        print(f'Students table columns: {columns}')
        
        if 'internal_marks' in columns:
            print('✅ internal_marks column exists in students table')
        else:
            print('❌ internal_marks column missing in students table')
            
        # Check prediction_history table
        cursor.execute('PRAGMA table_info(prediction_history)')
        columns = [col[1] for col in cursor.fetchall()]
        print(f'Prediction history columns: {columns}')
        
        if 'internal_marks' in columns:
            print('✅ internal_marks column exists in prediction_history table')
        else:
            print('❌ internal_marks column missing in prediction_history table')
            
        conn.close()
        print('\n✅ Database check completed successfully')
    else:
        print(f'❌ Database file does not exist at: {DB_PATH}')
        print('Run: python app.py to initialize the database')
        
except Exception as e:
    print(f'❌ Database error: {e}')