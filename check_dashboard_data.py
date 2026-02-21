import sqlite3
import os

db_path = r"c:\Users\yassir\Downloads\ecom index\backend\convertai.db"

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check users
    cursor.execute("SELECT id, email, role FROM users")
    users = cursor.fetchall()
    print(f"Total Users: {len(users)}")
    for u in users:
        print(f"User: {u}")
        
    # Check services
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='services'")
    if cursor.fetchone():
        cursor.execute("SELECT COUNT(*) FROM services")
        print(f"Total Services: {cursor.fetchone()[0]}")
    else:
        print("Table 'services' not found")
        
    # Check orders
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
    if cursor.fetchone():
        cursor.execute("SELECT COUNT(*) FROM orders")
        print(f"Total Orders: {cursor.fetchone()[0]}")
    else:
        print("Table 'orders' not found")
        
    conn.close()
except Exception as e:
    print(f"Error: {e}")
