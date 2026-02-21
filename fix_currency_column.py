import sqlite3
import os

db_path = 'convertai.db'

def migrate():
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column exists first
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'currency' in columns:
            print("Column 'currency' already exists.")
        else:
            print("Adding column 'currency'...")
            cursor.execute("ALTER TABLE users ADD COLUMN currency VARCHAR DEFAULT 'USD'")
            conn.commit()
            print("Successfully added 'currency' column.")
            
        conn.close()
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
