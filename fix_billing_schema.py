import sqlite3
import os

DB_PATH = r'c:\Users\yassir\Downloads\ecom index\backend\convertai.db'

def fix_billing_schema():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Add balance column to users
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN balance FLOAT DEFAULT 0.0;")
        print("Column balance added successfully.")
    except Exception as e:
        if "duplicate column name" in str(e).lower():
            print("Column balance already exists.")
        else:
            print(f"Error adding balance: {e}")

    # Create transactions table
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                transaction_id TEXT UNIQUE,
                type TEXT NOT NULL,
                description TEXT,
                amount FLOAT NOT NULL,
                currency TEXT DEFAULT 'EUR',
                status TEXT DEFAULT 'completed',
                payment_method TEXT,
                receipt_url TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        """)
        print("Table transactions created or already exists.")
    except Exception as e:
        print(f"Error creating transactions table: {e}")

    conn.commit()
    conn.close()
    print("Billing schema fix completed.")

if __name__ == "__main__":
    fix_billing_schema()
