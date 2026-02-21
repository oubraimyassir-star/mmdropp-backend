import sqlite3
import os

def migrate_to_enterprise():
    db_path = "convertai.db"
    if not os.path.exists(db_path):
        print(f"Error: Database {db_path} not found.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Update all users to enterprise plan
        cursor.execute("UPDATE users SET plan = 'enterprise'")
        affected = cursor.rowcount
        
        conn.commit()
        conn.close()
        print(f"Successfully updated {affected} users to 'enterprise' plan.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    migrate_to_enterprise()
