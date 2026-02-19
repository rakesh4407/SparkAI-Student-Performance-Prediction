#!/usr/bin/env python3
"""
Debug database path and contents
"""

import os
import sqlite3

# Check the paths that the Flask app would use
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "student_system.db")

print(f"Base directory: {BASE_DIR}")
print(f"Database directory: {DB_DIR}")
print(f"Database path: {DB_PATH}")
print(f"Database file exists: {os.path.exists(DB_PATH)}")

if os.path.exists(DB_PATH):
    print(f"Database file size: {os.path.getsize(DB_PATH)} bytes")
    
    # Check users in the database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    users = conn.execute("SELECT username, role FROM users").fetchall()
    print(f"\nUsers in database:")
    for user in users:
        print(f"  {user['username']} ({user['role']})")
    
    conn.close()
else:
    print("Database file does not exist!")

# Also check if there are any other database files
print(f"\nContents of database directory:")
if os.path.exists(DB_DIR):
    for file in os.listdir(DB_DIR):
        file_path = os.path.join(DB_DIR, file)
        print(f"  {file} ({os.path.getsize(file_path)} bytes)")
else:
    print("Database directory does not exist!")