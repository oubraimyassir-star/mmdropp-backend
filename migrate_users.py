import sqlite3
import os

DB_PATH = "convertai.db"

def migrate_users():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Checking users table...")
    
    columns = [
        ("landing_pages_used_this_month", "INTEGER DEFAULT 0"),
        ("ai_images_used_this_month", "INTEGER DEFAULT 0"),
        ("email_campaigns_used_this_month", "INTEGER DEFAULT 0"),
        ("stores_connected_count", "INTEGER DEFAULT 0")
    ]

    for col_name, col_type in columns:
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
            print(f"Added {col_name} column.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"Column {col_name} already exists.")
            else:
                print(f"Could not add column {col_name}: {e}")

    conn.commit()
    conn.close()
    print("User migration complete.")

if __name__ == "__main__":
    migrate_users()
