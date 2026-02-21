import sqlite3
import os

db_path = "c:\\Users\\yassir\\Downloads\\ecom index\\backend\\convertai.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Listing Users and Roles:")
cursor.execute("SELECT id, email, role, is_active FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
