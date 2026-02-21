from database import SessionLocal
import models

def fix():
    db = SessionLocal()
    try:
        users = db.query(models.User).all()
        for u in users:
            print(f"Bumping balance for {u.email} to 1000.0")
            u.balance = 1000.0
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    fix()
