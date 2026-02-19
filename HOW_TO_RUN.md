# 🚀 How to Run SparkAI Application

## Quick Start (Recommended)

### **Option 1: Using Startup Script**

```bash
python start_app.py
```

### **Option 2: Windows Batch File**

Double-click `start_app.bat` or run:

```cmd
start_app.bat
```

### **Option 3: Manual Start**

```bash
python app.py
```

## 📋 Prerequisites

### **Python Requirements**

- Python 3.7 or higher
- pip (Python package installer)

### **Install Dependencies**

```bash
pip install -r requirements.txt
```

## 🌐 Accessing the Application

Once started, the application will be available at:

```
http://127.0.0.1:5000
```

## 🔑 Login Credentials

### **Admin Access**

- Username: `admin`
- Password: `admin123`
- Features: User management, CSV upload, system administration

### **Teacher Access**

- Username: `teacher1`
- Password: `teacher123`
- Features: Student analytics, performance insights, reports

### **Student Access**

- Username: `student1`
- Password: `student123`
- Features: Personal dashboard, AI recommendations, progress reports

## 🎯 Features Available Without Login

### **AI Prediction Tool**

- URL: `http://127.0.0.1:5000/predict`
- Enter student data to get AI-powered performance predictions
- No login required

### **AI Chatbot**

- URL: `http://127.0.0.1:5000/chatbot`
- Get educational guidance and support
- No login required

## 📊 Application Features

### **For Students**

- Personal performance dashboard
- AI-generated recommendations
- Progress tracking
- PDF report downloads

### **For Teachers**

- Class performance analytics
- At-risk student identification
- Interactive charts and visualizations
- Student profile management

### **For Administrators**

- User account management
- Bulk student data upload via CSV
- System configuration
- Database management

## 🛠 Troubleshooting

### **Common Issues**

#### **"Module not found" Error**

```bash
pip install -r requirements.txt
```

#### **Port Already in Use**

If port 5000 is busy, the app will show an error. Stop other applications using port 5000 or modify the port in `app.py`.

#### **Database Issues**

The application automatically creates the database. If you encounter issues:

```bash
python database_setup.py
python create_admin.py
```

#### **Missing ML Model Files**

If model files are missing:

```bash
python model_train.py
```

## 🔄 Stopping the Application

Press `Ctrl+C` in the terminal where the application is running.

## 📁 Project Structure

```
EduAI-Student-Performance-Prediction-main/
├── app.py                 # Main Flask application
├── start_app.py          # Startup script
├── start_app.bat         # Windows batch file
├── requirements.txt      # Python dependencies
├── student_data.csv      # Sample data
├── ml_model/            # Machine learning models
├── templates/           # HTML templates
├── static/             # CSS, JS, images
└── database/           # SQLite database
```

## 🎉 Success Indicators

When the application starts successfully, you should see:

```
🎉 SparkAI is now running!
📍 Application available at: http://127.0.0.1:5000
```

## 💡 Tips

1. **First Time Setup**: The application automatically creates admin user and sample data
2. **Browser Compatibility**: Works best with Chrome, Firefox, Safari, Edge
3. **Mobile Friendly**: Responsive design works on mobile devices
4. **Data Persistence**: All data is saved in SQLite database
5. **No Internet Required**: Runs completely offline

## 🆘 Need Help?

If you encounter any issues:

1. Check that all dependencies are installed
2. Ensure Python 3.7+ is installed
3. Verify all project files are present
4. Check the terminal for error messages

The application includes comprehensive error handling and should provide clear error messages if something goes wrong.
