from database import SessionLocal
import models

def unlock_user(email: str):
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if user:
            user.plan = 'pro' # or enterprise to unlock everything
            db.commit()
            print(f"User {email} plan updated to {user.plan}")
        else:
            print(f"User {email} not found")
    finally:
        db.close()

if __name__ == "__main__":
    unlock_user("oubraimyassir@gmail.com")
