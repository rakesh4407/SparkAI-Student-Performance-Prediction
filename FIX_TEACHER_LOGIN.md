# Teacher Login Troubleshooting Guide

## ✅ Verified Working Credentials

The database has been checked and these credentials work:

### Option 1:
- **Username:** `teacher`
- **Password:** `teacher123`
- **Role:** Teacher (select from dropdown)

### Option 2:
- **Username:** `teacher1`
- **Password:** `teacher123`
- **Role:** Teacher (select from dropdown)

## 🔍 Common Issues & Solutions

### Issue 1: Server Not Running
**Symptom:** Cannot access http://127.0.0.1:5000

**Solution:**
```bash
cd NEW_EduAI-Student-Performance-Prediction-mainLatest/EduAI-Student-Performance-Prediction-main
python app.py
```

Wait for: `Running on http://127.0.0.1:5000`

### Issue 2: Wrong Credentials
**Symptom:** "Invalid login details!" error

**Common Mistakes:**
- ❌ Using `teacher123` as username (it's the PASSWORD!)
- ❌ Typing `Teacher` instead of `teacher` (case-sensitive)
- ❌ Extra spaces before/after username or password
- ❌ Not selecting "Teacher" from the role dropdown

**Solution:**
1. Clear the form
2. Select "Teacher" role FIRST
3. Type exactly: `teacher` (lowercase)
4. Type exactly: `teacher123`
5. Click "Sign In"

### Issue 3: Wrong Role Selected
**Symptom:** Login fails even with correct credentials

**Solution:**
Make sure the "Teacher" radio button is selected (middle option)
- Admin (left) ❌
- Teacher (middle) ✅
- Student (right) ❌

### Issue 4: Session Issues
**Symptom:** Redirects back to login after successful login

**Solution:**
```bash
# Clear browser cache and cookies
# Or try incognito/private browsing mode
```

### Issue 5: Database Issues
**Symptom:** No teacher accounts exist

**Solution:**
```bash
python check_teacher_login.py
```

If no teachers found, run:
```bash
python create_default_users.py
```

## 🧪 Test Your Login

Run this script to verify everything works:
```bash
python quick_teacher_login_test.py
```

## 📝 Step-by-Step Login Process

1. **Start the server:**
   ```bash
   python app.py
   ```

2. **Open browser:**
   ```
   http://127.0.0.1:5000/login
   ```

3. **Fill the form:**
   - Click on "Teacher" (middle option)
   - Username field: `teacher`
   - Password field: `teacher123`

4. **Click "Sign In"**

5. **You should see:**
   - URL changes to: `http://127.0.0.1:5000/teacher-dashboard`
   - Teacher dashboard with student analytics

## 🐛 Still Not Working?

### Check Flask Terminal Output
Look for errors like:
- `KeyError: 'role'` - Form not submitting correctly
- `AttributeError` - Database issue
- `TemplateNotFound` - Missing template files

### Check Browser Console
1. Press F12 to open Developer Tools
2. Go to "Console" tab
3. Look for JavaScript errors (red text)

### Enable Debug Mode
The app already runs in debug mode. Check the terminal for detailed error messages.

### Verify Database
```bash
python check_teacher_login.py
```

Should show:
```
✅ Password 'teacher123' works!
```

## 🔧 Manual Database Fix (Last Resort)

If nothing works, recreate the teacher account:

```python
import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('database/student_system.db')

# Delete old teacher account
conn.execute("DELETE FROM users WHERE username='teacher'")

# Create new teacher account
conn.execute("""
    INSERT INTO users (username, password, role)
    VALUES (?, ?, ?)
""", ('teacher', generate_password_hash('teacher123'), 'teacher'))

conn.commit()
conn.close()

print("✅ Teacher account recreated!")
```

## 📞 Need More Help?

If you're still having issues, please provide:
1. Error message from Flask terminal
2. Error message from browser (if any)
3. Screenshot of the login page
4. Output of `python check_teacher_login.py`
