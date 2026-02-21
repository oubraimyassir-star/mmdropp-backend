import sqlite3
import os

db_path = r"c:\Users\yassir\Downloads\ecom index\backend\convertai.db"

def add_column(cursor, table, column, type):
    try:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {type}")
        print(f"Added column {column} to {table}")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print(f"Column {column} already exists in {table}")
        else:
            print(f"Error adding column {column}: {e}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Missing columns identified from the SQLAlchemy error
    add_column(cursor, "users", "plan", "VARCHAR")
    add_column(cursor, "users", "landing_pages_used_this_month", "INTEGER DEFAULT 0")
    add_column(cursor, "users", "ai_images_used_this_month", "INTEGER DEFAULT 0")
    add_column(cursor, "users", "email_campaigns_used_this_month", "INTEGER DEFAULT 0")
    add_column(cursor, "users", "whatsapp_messages_used_this_month", "INTEGER DEFAULT 0")
    add_column(cursor, "users", "stores_connected_count", "INTEGER DEFAULT 0")
    add_column(cursor, "users", "usage_count", "INTEGER DEFAULT 0")
    add_column(cursor, "users", "usage_limit", "INTEGER DEFAULT 0")
    add_column(cursor, "users", "onboarding_completed", "BOOLEAN DEFAULT FALSE")
    add_column(cursor, "users", "onboarding_data", "JSON")
    add_column(cursor, "users", "currency", "VARCHAR DEFAULT 'EUR'")
    add_column(cursor, "users", "balance", "FLOAT DEFAULT 0.0")
    
    conn.commit()
    conn.close()
    print("Schema repair complete")
except Exception as e:
    print(f"Error repairing schema: {e}")
