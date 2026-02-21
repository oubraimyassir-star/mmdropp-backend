import sqlite3
import os

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "convertai.db")

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

    # Check 'orders' table
    columns = list_columns(cursor, 'orders')
    
    needed_columns = {
        'proof_url': 'TEXT',
        'customer_name': 'TEXT',
        'payment_method': 'TEXT'
    }
    
    for col_name, col_type in needed_columns.items():
        if col_name not in columns:
            print(f"Adding '{col_name}' column to 'orders' table...")
            try:
                cursor.execute(f"ALTER TABLE orders ADD COLUMN {col_name} {col_type}")
                print(f"'{col_name}' column added successfully.")
            except Exception as e:
                print(f"Error adding {col_name}: {e}")
        else:
            print(f"'{col_name}' column already exists.")

    # Inspect some data
    print("\nInspecting first 5 orders:")
    cursor.execute("SELECT id, user_id, service_id, customer_name, payment_method FROM orders LIMIT 5")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Order ID: {row[0]}, User ID: {row[1]}, Service ID: {row[2]}, Customer: {row[3]}, Method: {row[4]}")

    print("\nChecking users:")
    cursor.execute("SELECT id, email FROM users LIMIT 5")
    users = cursor.fetchall()
    for user in users:
        print(f"User ID: {user[0]}, Email: {user[1]}")

    conn.commit()
    conn.close()
    print("\nMigration completed.")

if __name__ == '__main__':
    migrate()
