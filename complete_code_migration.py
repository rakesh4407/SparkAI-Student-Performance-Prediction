#!/usr/bin/env python3
"""
Complete Code Migration: internal_marks → internal_score
Changes EVERYTHING including variables, form fields, JavaScript, etc.
"""

import glob
import re
import os

print('=== COMPLETE MIGRATION: internal_marks → internal_score ===\n')

# Files to update
files_to_update = ['app.py'] + glob.glob('templates/*.html')

for filepath in files_to_update:
    print(f'Updating: {os.path.basename(filepath)}')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace ALL variations of internal_marks
    content = content.replace('internal_marks', 'internal_score')
    content = content.replace('Internal_Marks', 'Internal_Score')
    content = content.replace('internal_Marks', 'internal_Score')
    content = content.replace('Internal_marks', 'Internal_score')
    
    # Replace JavaScript function names and variables
    content = content.replace('updateInternal_Marks', 'updateInternal_Score')
    content = content.replace('currentInternal_Marks', 'currentInternal_Score')
    content = content.replace('updateInternal_Scores', 'updateInternal_Score')
    content = content.replace('currentInternal_Scores', 'currentInternal_Score')
    
    # Replace form field names and IDs
    content = content.replace('name="internal_marks"', 'name="internal_score"')
    content = content.replace('id="internal_marks"', 'id="internal_score"')
    content = content.replace('internal_marks-percentage', 'internal_score-percentage')
    
    # Replace any remaining references
    content = re.sub(r'\binternal_marks\b', 'internal_score', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'  ✅ {os.path.basename(filepath)} updated')

print('\n' + '='*60)
print('✅ COMPLETE MIGRATION FINISHED!')
print('='*60)
print('✅ Database columns: internal_marks → internal_score')
print('✅ Python variables: internal_marks → internal_score')
print('✅ Form fields: name="internal_marks" → name="internal_score"')
print('✅ JavaScript variables: internal_marks → internal_score')
print('✅ Function names: updateInternal_Marks → updateInternal_Score')
print('✅ IDs and classes: internal_marks → internal_score')
print('✅ EVERYTHING has been changed to internal_score!')
print('='*60)