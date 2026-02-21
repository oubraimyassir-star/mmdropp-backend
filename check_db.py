import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
import models

def check():
    db = SessionLocal()
    try:
        users = db.query(models.User).count()
        orders = db.query(models.Order).count()
        services = db.query(models.Service).count()
        print(f"Users: {users}")
        print(f"Orders: {orders}")
        print(f"Services: {services}")
        
        if users > 0:
            print("\nUsers List:")
            all_users = db.query(models.User).all()
            for u in all_users:
                print(f"ID: {u.id}, Email: {u.email}, Balance: {u.balance}, Active: {u.is_active}")
        
        if orders > 0:
            print("\nLatest Orders:")
            latest_orders = db.query(models.Order).limit(5).all()
            for o in latest_orders:
                print(f"ID: {o.id}, User: {o.user_id}, Service: {o.service_id}, Status: {o.status}")
    finally:
        db.close()

if __name__ == "__main__":
    check()
