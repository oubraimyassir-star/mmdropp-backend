import sqlite3
import os

# Database path
DB_PATH = 'database.db'

def list_columns(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    return [row[1] for row in cursor.fetchall()]

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    print(f"Connecting to database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if 'role' column exists in 'users' table
    columns = list_columns(cursor, 'users')
    
    if 'role' not in columns:
        print("Adding 'role' column to 'users' table...")
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
            print("'role' column added successfully.")
        except Exception as e:
            print(f"Error adding column: {e}")
            conn.close()
            return
    else:
        print("'role' column already exists.")

    # Set admin role for specific user
    admin_email = "admin@smmadroop.com"
    print(f"Setting admin role for {admin_email}...")
    
    cursor.execute("UPDATE users SET role = 'admin' WHERE email = ?", (admin_email,))
    
    if cursor.rowcount > 0:
        print(f"Successfully updated role for {admin_email}.")
    else:
        print(f"User {admin_email} not found. Creating admin user if not exists...")
        # Optional: Create admin user if main.py doesn't catch it
        # For now, we assume the user might sign up later or we just wait.
        pass

    conn.commit()
    conn.close()
    print("Migration completed.")

if __name__ == '__main__':
    migrate()
