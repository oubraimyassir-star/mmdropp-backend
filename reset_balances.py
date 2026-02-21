import sqlite3
import os

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "convertai.db")

def reset_balances():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Resetting all user balances to 0.0...")
    cursor.execute("UPDATE users SET balance = 0.0")
    conn.commit()
    
    # Check results
    cursor.execute("SELECT id, email, balance FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Email: {row[1]}, New Balance: {row[2]}")

    conn.close()
    print("All balances reset to 0.0 successfully.")

if __name__ == '__main__':
    reset_balances()
