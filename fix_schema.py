import sqlite3
import os

DB_PATH = 'convertai.db'

def fix_schema():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # List of columns to check/add
    columns_to_add = [
        ("currency", "TEXT DEFAULT 'USD'"),
        ("stripe_session_id", "TEXT"),
        ("stripe_customer_id", "TEXT"),
        ("onboarding_completed", "BOOLEAN DEFAULT 0"),
        ("onboarding_data", "TEXT")
    ]

    for col_name, col_type in columns_to_add:
        try:
            # Check if column exists first to avoid exception noise (optional, but cleaner)
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type};")
            print(f"Column {col_name} added successfully.")
        except Exception as e:
            # SQLite throws "duplicate column name" if it exists
            if "duplicate column name" in str(e).lower():
                print(f"Column {col_name} already exists.")
            else:
                print(f"Error adding {col_name}: {e}")

    conn.commit()
    conn.close()
    print("Schema check completed.")

if __name__ == "__main__":
    fix_schema()
