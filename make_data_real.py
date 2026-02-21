import sqlite3
import os

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "convertai.db")

def make_data_real():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Add cost column to services if it doesn't exist
    print("Checking services table...")
    cursor.execute("PRAGMA table_info(services)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'cost' not in columns:
        print("Adding 'cost' column to services...")
        cursor.execute("ALTER TABLE services ADD COLUMN cost FLOAT DEFAULT 0.0")
        conn.commit()

    # 2. Populate cost for services (70% of price)
    print("Populating service costs...")
    cursor.execute("UPDATE services SET cost = price * 0.7 WHERE cost = 0.0 OR cost IS NULL")
    conn.commit()

    # 3. Activate main users
    print("Activating main admin users...")
    emails_to_activate = ["oubraimyassir@gmail.com", "yassiroubraim3@gmail.com", "yassoub2025@gmail.com"]
    for email in emails_to_activate:
        cursor.execute("UPDATE users SET is_active = 1 WHERE email = ?", (email,))
    conn.commit()

    # 4. Clean up order data
    print("Cleaning up order data...")
    # Map old UserID 1 to "Yassir (Admin)" if name is generic
    cursor.execute("UPDATE users SET name = 'Yassir Oubraim' WHERE id = 1 AND name = 'Information économique'")
    conn.commit()

    # Update orders that have "Client Direct" to something more specific if possible
    # (Actually "Client Direct" is fine for now, but let's ensure they have a cost/profit basis)
    
    conn.close()
    print("Data enhanced successfully.")

if __name__ == '__main__':
    make_data_real()
