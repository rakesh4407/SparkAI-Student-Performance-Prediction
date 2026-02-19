import sqlite3
import pandas as pd

conn = sqlite3.connect("database/student_system.db")
df = pd.read_sql_query("SELECT * FROM students", conn)
conn.close()

print(df.columns.tolist())
print(df.head())
