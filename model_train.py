import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, r2_score, mean_squared_error, mean_absolute_error
import joblib
import warnings
warnings.filterwarnings('ignore')

# ---------------- LOAD DATA ----------------
print("="*60)
print("STUDENT PERFORMANCE PREDICTION MODEL TRAINING")
print("="*60)
print("\nLoading dataset...")

df = pd.read_csv("student_data.csv")

# ---------------- DATA CLEANING ----------------
print("\n" + "="*60)
print("DATA CLEANING")
print("="*60)

# Remove missing / invalid labels
df = df.dropna(subset=["performance"])
df = df[df["performance"].astype(str).str.strip() != ""]

# Normalize labels
df["performance"] = df["performance"].str.strip().str.title()

print("\nClass distribution:")
print(df["performance"].value_counts())

np.random.seed(42)

# Check if test_score column exists, if not create it
if 'test_score' not in df.columns:
    print("\n⚠️  test_score column not found. Creating from existing data...")
    # Create test_score from midterm and assignments
    df['test_score'] = (df['midterm_score'] + df['assignments_score']) / 2
    df['test_score'] = df['test_score'].clip(0, 30).round(1)

# Ensure final_score is in 0-40 range (convert from 0-50 if needed)
if df['final_score'].max() > 40:
    print("\n⚠️  Converting final_score from 0-50 to 0-40 range...")
    df['final_score'] = (df['final_score'] * 0.8).clip(0, 40).round(1)

# Add noise to make data more realistic
score_cols = [
    "assignments_score",
    "midterm_score",
    "test_score",
    "final_score"
]

for col in score_cols:
    if col in df.columns:
        noise = np.random.normal(loc=0, scale=2, size=len(df))
        df[col] = (df[col] + noise).clip(0, df[col].max()).round(1)

# Add small noise to labels (5% mislabeling for realism)
noise_fraction = 0.05
n_noisy = int(len(df) * noise_fraction)
indices = np.random.choice(df.index, n_noisy, replace=False)
labels = df["performance"].unique()

for idx in indices:
    current_label = df.at[idx, "performance"]
    df.at[idx, "performance"] = np.random.choice(
        [l for l in labels if l != current_label]
    )

print("\n✅ Data cleaning complete!")

# ---------------- FEATURE ENGINEERING ----------------
print("\n" + "="*60)
print("FEATURE ENGINEERING")
print("="*60)

def engineer_features(df):
    """Create enhanced features for better prediction"""
    df = df.copy()
    
    # Calculate input total (60 marks)
    df['input_total'] = df['assignments_score'] + df['midterm_score'] + df['test_score']
    df['input_percentage'] = (df['input_total'] / 60) * 100
    
    # Calculate total score (100 marks)
    df['total_score'] = df['input_total'] + df['final_score']
    
    # Interaction features
    df['attendance_study_interaction'] = df['attendance'] * df['study_hours'] / 100
    
    # Study efficiency
    df['study_efficiency'] = df['input_total'] / (df['study_hours'] + 1)
    
    # Attendance impact
    df['attendance_impact'] = np.where(df['attendance'] < 75, -0.1, 
                                       np.where(df['attendance'] > 90, 0.1, 0))
    
    # Score ratios
    df['assignments_ratio'] = df['assignments_score'] / 10
    df['midterm_ratio'] = df['midterm_score'] / 20
    df['test_ratio'] = df['test_score'] / 30
    
    # Combined academic score
    df['academic_score'] = (df['assignments_ratio'] * 0.1 + 
                           df['midterm_ratio'] * 0.2 + 
                           df['test_ratio'] * 0.3) * 100
    
    # Performance category based on total score (100 marks)
    df['performance_category'] = pd.cut(df['total_score'], 
                                       bins=[0, 60, 70, 80, 100], 
                                       labels=['Poor', 'Average', 'Good', 'Excellent'])
    
    return df

# Apply feature engineering
df = engineer_features(df)

print(f"\nFeatures created: {[col for col in df.columns if col not in ['attendance', 'assignments_score', 'midterm_score', 'test_score', 'final_score', 'study_hours', 'performance']]}")

# Show sample of engineered features
print("\nSample of engineered features:")
print(df[['input_total', 'total_score', 'performance_category', 'study_efficiency']].head())

# ---------------- FEATURES & TARGETS ----------------
print("\n" + "="*60)
print("PREPARING FEATURES AND TARGETS")
print("="*60)

# Features for both models
feature_columns = [
    "attendance", 
    "assignments_score", 
    "midterm_score", 
    "test_score",
    "study_hours",
    "input_percentage",
    "attendance_study_interaction",
    "study_efficiency",
    "attendance_impact",
    "assignments_ratio",
    "midterm_ratio",
    "test_ratio",
    "academic_score"
]

X = df[feature_columns]

print(f"\nSelected {len(feature_columns)} features:")
for i, feat in enumerate(feature_columns, 1):
    print(f"{i:2d}. {feat}")

# ---------------- TARGET 1: REGRESSION (Predict end-term marks) ----------------
y_reg = df["final_score"].values

# ---------------- TARGET 2: CLASSIFICATION (Predict performance category) ----------------
le = LabelEncoder()
y_clf = le.fit_transform(df["performance_category"])

print(f"\nRegression target: final_score (0-40 marks)")
print(f"Classification target: performance_category")
print(f"\nCategory distribution:")
print(df['performance_category'].value_counts())

# ---------------- TRAIN-TEST SPLIT ----------------
print("\n" + "="*60)
print("TRAIN-TEST SPLIT")
print("="*60)

# Split for regression
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X, y_reg,
    test_size=0.2,
    random_state=42
)

# Split for classification (with stratification)
X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(
    X, y_clf,
    test_size=0.2,
    random_state=42,
    stratify=y_clf
)

print(f"\nTraining set size: {len(X_train_reg)} samples")
print(f"Test set size: {len(X_test_reg)} samples")

# ---------------- SCALE FEATURES ----------------
scaler = StandardScaler()
X_train_reg_scaled = scaler.fit_transform(X_train_reg)
X_test_reg_scaled = scaler.transform(X_test_reg)

# Scale for classification (using same scaler)
X_train_clf_scaled = scaler.transform(X_train_clf)
X_test_clf_scaled = scaler.transform(X_test_clf)

print("\n✅ Features scaled successfully!")

# ==================== PART 1: REGRESSION MODEL (Predict End-term Marks) ====================
print("\n" + "="*60)
print("PART 1: TRAINING REGRESSION MODEL (0-40 marks)")
print("="*60)

# Train Random Forest Regressor with hyperparameter tuning
print("\n📊 Training Random Forest Regressor...")

param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 15, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

rf_regressor = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(rf_regressor, param_grid, cv=5, scoring='r2', n_jobs=-1, verbose=1)
grid_search.fit(X_train_reg_scaled, y_train_reg)

reg_model = grid_search.best_estimator_
print(f"\n✅ Best parameters: {grid_search.best_params_}")
print(f"Best cross-validation R² score: {grid_search.best_score_:.4f}")

# Evaluate on test set
y_pred_reg = reg_model.predict(X_test_reg_scaled)

regression_metrics = {
    'r2_score': r2_score(y_test_reg, y_pred_reg),
    'mse': mean_squared_error(y_test_reg, y_pred_reg),
    'rmse': np.sqrt(mean_squared_error(y_test_reg, y_pred_reg)),
    'mae': mean_absolute_error(y_test_reg, y_pred_reg)
}

print(f"\n📊 Regression Model Performance on Test Set:")
print(f"   R² Score: {regression_metrics['r2_score']:.4f}")
print(f"   RMSE: {regression_metrics['rmse']:.2f} marks (out of 40)")
print(f"   MAE: {regression_metrics['mae']:.2f} marks")
print(f"   MSE: {regression_metrics['mse']:.2f}")

# Feature importance for regression
feature_importance_reg = pd.DataFrame({
    'Feature': feature_columns,
    'Importance': reg_model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n📊 Feature Importance (Regression):")
print(feature_importance_reg.to_string(index=False))

# ==================== PART 2: CLASSIFICATION MODEL (Predict Performance Category) ====================
print("\n" + "="*60)
print("PART 2: TRAINING CLASSIFICATION MODEL")
print("="*60)

# Train Random Forest Classifier with hyperparameter tuning
print("\n📊 Training Random Forest Classifier...")

param_grid_clf = {
    'n_estimators': [100, 200],
    'max_depth': [10, 15, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

rf_classifier = RandomForestClassifier(random_state=42)
grid_search_clf = GridSearchCV(rf_classifier, param_grid_clf, cv=5, scoring='accuracy', n_jobs=-1, verbose=1)
grid_search_clf.fit(X_train_clf_scaled, y_train_clf)

clf_model = grid_search_clf.best_estimator_
print(f"\n✅ Best parameters: {grid_search_clf.best_params_}")
print(f"Best cross-validation accuracy: {grid_search_clf.best_score_:.4f}")

# Evaluate on test set
y_pred_clf = clf_model.predict(X_test_clf_scaled)
accuracy = accuracy_score(y_test_clf, y_pred_clf)

print(f"\n📊 Classification Model Performance on Test Set:")
print(f"   Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(
    y_test_clf,
    y_pred_clf,
    target_names=le.classes_,
    zero_division=0
))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test_clf, y_pred_clf))

# Feature importance for classification
feature_importance_clf = pd.DataFrame({
    'Feature': feature_columns,
    'Importance': clf_model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n📊 Feature Importance (Classification):")
print(feature_importance_clf.to_string(index=False))

# ==================== SAVE MODELS AND PREPROCESSORS ====================
print("\n" + "="*60)
print("SAVING MODELS AND PREPROCESSORS")
print("="*60)

# Create ml_model directory if it doesn't exist
import os
os.makedirs("ml_model", exist_ok=True)

# Save regression model (end-term predictor)
joblib.dump(reg_model, "ml_model/endterm_predictor_40.joblib")
print("✅ Saved: ml_model/endterm_predictor_40.joblib")

# Save classification model
joblib.dump(clf_model, "ml_model/performance_classifier.joblib")
print("✅ Saved: ml_model/performance_classifier.joblib")

# Save label encoder
joblib.dump(le, "ml_model/label_encoder.joblib")
print("✅ Saved: ml_model/label_encoder.joblib")

# Save scaler
joblib.dump(scaler, "ml_model/scaler.joblib")
print("✅ Saved: ml_model/scaler.joblib")

# Save feature columns
joblib.dump(feature_columns, "ml_model/feature_columns.joblib")
print("✅ Saved: ml_model/feature_columns.joblib")

# ==================== SUMMARY ====================
print("\n" + "="*60)
print("TRAINING COMPLETE - SUMMARY")
print("="*60)
print(f"""
📊 MODEL PERFORMANCE SUMMARY:
------------------------------
1. REGRESSION MODEL (End-term Predictor):
   - Best Model: Random Forest Regressor
   - R² Score: {regression_metrics['r2_score']:.4f}
   - RMSE: ±{regression_metrics['rmse']:.1f} marks (out of 40)
   - MAE: ±{regression_metrics['mae']:.1f} marks

2. CLASSIFICATION MODEL (Performance Category):
   - Best Model: Random Forest Classifier
   - Accuracy: {accuracy * 100:.1f}%
   - Categories: Poor (<60), Average (60-69), Good (70-79), Excellent (80-100)

3. FEATURE IMPORTANCE (Top 5):
   - Regression: {feature_importance_reg.iloc[0]['Feature']} ({feature_importance_reg.iloc[0]['Importance']:.3f})
   - Classification: {feature_importance_clf.iloc[0]['Feature']} ({feature_importance_clf.iloc[0]['Importance']:.3f})

4. SCORING SYSTEM:
   - Input Total: Assignments(10) + Midterm(20) + Test(30) = 60 marks
   - End-term (Predicted): 40 marks
   - Total: 100 marks

✅ All models saved successfully in 'ml_model/' directory!
""")