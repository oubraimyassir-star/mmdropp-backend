import sqlite3

def repair_and_unlock():
    conn = sqlite3.connect('convertai.db')
    cursor = conn.cursor()
    
    # Try to add the column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN whatsapp_messages_used_this_month INTEGER DEFAULT 0;")
        print("Column whatsapp_messages_used_this_month added.")
    except Exception as e:
        print(f"Column might already exist: {e}")
        
    # Update user plan
    try:
        cursor.execute("UPDATE users SET plan = 'enterprise' WHERE email = 'oubraimyassir@gmail.com';")
        conn.commit()
        print("User plan updated to enterprise.")
    except Exception as e:
        print(f"Update failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    repair_and_unlock()
