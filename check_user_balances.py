import sqlite3
import os

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "convertai.db")

def check_balances():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Checking User Balances:")
    cursor.execute("SELECT id, email, balance, currency FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Email: {row[1]}, Balance: {row[2]}, Currency: {row[3]}")

    conn.close()

if __name__ == '__main__':
    check_balances()
