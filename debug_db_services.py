import sqlite3
import os

db_path = r"c:\Users\yassir\Downloads\ecom index\backend\convertai.db"

if not os.path.exists(db_path):
    print(f"Database NOT found at {db_path}")
    # Try alternate location
    db_path = r"c:\Users\yassir\Downloads\ecom index\backend\database.db"
    if not os.path.exists(db_path):
        print(f"Alternate database NOT found at {db_path}")
    else:
        print(f"Database found at {db_path}")
else:
    print(f"Database found at {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # List tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:", [t[0] for t in tables])
    
    if ('services',) in tables:
        cursor.execute("SELECT COUNT(*) FROM services")
        count = cursor.fetchone()[0]
        print(f"Service count: {count}")
        
        cursor.execute("SELECT id, title, price FROM services LIMIT 5")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    else:
        print("'services' table NOT FOUND")
        
    conn.close()
except Exception as e:
    print(f"Error checking DB: {e}")
