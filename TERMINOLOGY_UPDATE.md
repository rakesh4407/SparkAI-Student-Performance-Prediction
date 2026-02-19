# Terminology Update: Test → Internal Marks

## Summary
All user-facing references to "Test" or "Test Score" have been changed to "Internal Marks" throughout the application templates.

## Files Updated

### 1. teacher_dashboard.html
- Column header tooltip: "Test" → "Internal Score"
- Column abbreviation: T(30) → I(30)

### 2. admin_dashboard.html
- Badge label: T(30) → I(30)
- Field label: "Test Score (0-30)" → "Internal Score (0-30)"
- Formula display: Test(30) → Internal Score(30)
- Validation message: "Test score must be..." → "Internal score must be..."

### 3. predict.html
- Section title: "Test Score" → "Internal Score"
- Input placeholder: "Enter test score" → "Enter internal score"
- Label in breakdown: "Test" → "Internal Score"
- Validation message updated
- Help text: "test (30)" → "internal marks (30)"
- Section heading: "Input Total (Assignments + Midterm + Test)" → "Input Total (Assignments + Midterm + Internal Marks)"
- Info text: "Test (30)" → "Internal Marks (30)"
- JavaScript comment: "Update test (0-30)" → "Update internal marks (0-30)"

### 4. prediction_history.html
- Column header: T(30) → I(30)
- CSV export header: "Test" → "Internal Marks"

### 5. result.html
- Description: "test scores" → "internal scores"
- Card title: "Test" → "Internal Marks"
- Formula: "Test(30)" → "Internal Score(30)"

### 6. student_dashboard.html
- Comment: "test score" → "internal score"
- Section comment: "Test (NEW)" → "Internal Marks (NEW)"
- Label: "Test" → "Internal Score"
- Recommendation text: "Test scores" → "Internal scores"
- Academic breakdown: "Test: {{ test }}/30" → "Internal Marks: {{ test }}/30"
- Footer formula: "Test(30)" → "Internal Score(30)"
- Help text: "Assignments + Midterm + Test" → "Assignments + Midterm + Internal Marks"

### 7. app.py
- PDF report: "Test Score" → "Internal Score"
- Sample data message: "Test(30)" → "Internal Score(30)"

## Technical Notes

### What Was NOT Changed (Intentionally)
The following technical elements remain unchanged to maintain code functionality:

1. **Database column name**: `test_score` (database schema)
2. **JavaScript variables**: `currentTest`, `test` (variable names)
3. **HTML form field names**: `name="test"`, `id="test"` (form processing)
4. **Function names**: `updateTest()` (JavaScript functions)
5. **Template variables**: `{{ test }}` (Jinja2 variables from backend)
6. **CSS color variables**: `test: "#a855f7"` (chart colors)

These technical identifiers must remain as-is to ensure the application continues to function correctly. Only user-visible text was changed.

## Scoring System
The application uses the following scoring breakdown:
- Assignments: 10 marks
- Midterm: 20 marks
- **Internal Marks: 30 marks** (formerly "Test")
- End-term: 40 marks
- **Total: 100 marks**

## User Impact
Users will now see "Internal Marks" or "Internal Score" instead of "Test" or "Test Score" throughout the interface, making the terminology more appropriate for the educational context.
