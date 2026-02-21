import sqlite3
import os

db_path = r"c:\Users\yassir\Downloads\ecom index\backend\convertai.db"

def add_column(cursor, table, column, type):
    try:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {type}")
        print(f"Added column {column} to {table}")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print(f"Column {column} already exists in {table}")
        else:
            print(f"Error adding column {column}: {e}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Missing columns
    add_column(cursor, "users", "role", "VARCHAR DEFAULT 'user'")
    add_column(cursor, "users", "last_active", "DATETIME")
    
    conn.commit()
    conn.close()
    print("Schema repair (Final) complete")
except Exception as e:
    print(f"Error repairing schema: {e}")
