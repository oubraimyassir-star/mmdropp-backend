import sqlite3
import os

db_path = r"c:\Users\yassir\Downloads\ecom index\backend\convertai.db"

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    print("Columns in 'users' table:")
    for col in columns:
        print(col)
        
    conn.close()
except Exception as e:
    print(f"Error: {e}")
