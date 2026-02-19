#!/usr/bin/env python3
"""
Database Migration: Rename test_score to internal_marks
WARNING: Backup your database before running this script!
"""

import sqlite3
import os
from datetime import datetime

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "student_system.db")
BACKUP_PATH = os.path.join(BASE_DIR, "database", f"student_system_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")

def backup_database():
    """Create a backup of the database"""
    import shutil
    print(f"Creating backup at: {BACKUP_PATH}")
    shutil.copy2(DB_PATH, BACKUP_PATH)
    print("✅ Backup created successfully!")

def migrate_database():
    """Migrate test_score column to internal_marks"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        print("\n=== Starting Migration ===\n")
        
        # 1. Migrate students table
        print("1. Migrating 'students' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students_new (
                roll_no INTEGER PRIMARY KEY,
                name TEXT,
                attendance REAL,
                assignments_score REAL,
                midterm_score REAL,
                internal_marks REAL,
                final_score REAL,
                study_hours REAL,
                performance TEXT
            )
        """)
        
        cursor.execute("""
            INSERT INTO students_new 
            SELECT roll_no, name, attendance, assignments_score, midterm_score,
                   test_score, final_score, study_hours, performance
            FROM students
        """)
        
        cursor.execute("DROP TABLE students")
        cursor.execute("ALTER TABLE students_new RENAME TO students")
        print("   ✅ Students table migrated")
        
        # 2. Migrate prediction_history table
        print("2. Migrating 'prediction_history' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prediction_history_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_no INTEGER,
                assignments_score REAL,
                midterm_score REAL,
                internal_marks REAL,
                predicted_endterm REAL,
                total_score REAL,
                predicted_label TEXT,
                date_time TEXT
            )
        """)
        
        cursor.execute("""
            INSERT INTO prediction_history_new
            SELECT id, roll_no, assignments_score, midterm_score,
                   test_score, predicted_endterm, total_score, predicted_label, date_time
            FROM prediction_history
        """)
        
        cursor.execute("DROP TABLE prediction_history")
        cursor.execute("ALTER TABLE prediction_history_new RENAME TO prediction_history")
        print("   ✅ Prediction history table migrated")
        
        conn.commit()
        print("\n=== Migration Completed Successfully! ===\n")
        
        # Verify migration
        print("Verifying migration...")
        cursor.execute("PRAGMA table_info(students)")
        students_cols = [col[1] for col in cursor.fetchall()]
        
        cursor.execute("PRAGMA table_info(prediction_history)")
        history_cols = [col[1] for col in cursor.fetchall()]
        
        if 'internal_marks' in students_cols and 'internal_marks' in history_cols:
            print("✅ Verification passed: 'internal_marks' column exists in both tables")
            print(f"   Students columns: {students_cols}")
            print(f"   History columns: {history_cols}")
        else:
            print("❌ Verification failed!")
            
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        conn.rollback()
        print("\nRestoring from backup...")
        conn.close()
        import shutil
        shutil.copy2(BACKUP_PATH, DB_PATH)
        print("✅ Database restored from backup")
        return False
    finally:
        conn.close()
    
    return True

if __name__ == "__main__":
    print("="*60)
    print("DATABASE MIGRATION: test_score → internal_marks")
    print("="*60)
    print("\n⚠️  WARNING: This will modify your database structure!")
    print("A backup will be created automatically.\n")
    
    response = input("Do you want to proceed? (yes/no): ").strip().lower()
    
    if response == 'yes':
        backup_database()
        if migrate_database():
            print("\n✅ Migration completed successfully!")
            print(f"Backup saved at: {BACKUP_PATH}")
            print("\nNext steps:")
            print("1. Update app.py code")
            print("2. Update template files")
            print("3. Test the application")
        else:
            print("\n❌ Migration failed. Database restored from backup.")
    else:
        print("\nMigration cancelled.")
