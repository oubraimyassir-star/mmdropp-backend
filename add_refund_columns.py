import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "convertai.db")

def migrate():
    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Add columns to orders table
    columns_to_add_orders = [
        ("locked_price", "FLOAT DEFAULT 0.0"),
        ("refunded", "BOOLEAN DEFAULT 0"),
        ("refunded_at", "DATETIME")
    ]

    for col_name, col_type in columns_to_add_orders:
        try:
            cursor.execute(f"ALTER TABLE orders ADD COLUMN {col_name} {col_type}")
            print(f"Added column {col_name} to orders table.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print(f"Column {col_name} already exists in orders table.")
            else:
                print(f"Error adding {col_name} to orders: {e}")

    # Add column to transactions table
    try:
        cursor.execute("ALTER TABLE transactions ADD COLUMN reference_order_id INTEGER REFERENCES orders(id)")
        print("Added column reference_order_id to transactions table.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("Column reference_order_id already exists in transactions table.")
        else:
            print(f"Error adding reference_order_id to transactions: {e}")

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
