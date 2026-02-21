import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'convertai.db')

def migrate():
    print(f"Migrating database at {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN is_blocked BOOLEAN DEFAULT 0")
        print("Successfully added is_blocked column to users table.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("Column is_blocked already exists.")
        else:
            print(f"Error: {e}")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()
