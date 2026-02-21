from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from auth import get_password_hash

def create_admin():
    db = SessionLocal()
    email = "admin@smmadroop.com"
    password = "adminpassword123" # Temporary password
    
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if user:
            print(f"User {email} already exists. Updating role to admin...")
            user.role = "admin"
            db.commit()
            print("Role updated.")
        else:
            print(f"Creating admin user {email}...")
            hashed_password = get_password_hash(password)
            new_user = models.User(
                email=email,
                hashed_password=hashed_password,
                full_name="Admin User",
                role="admin",
                credits=1000.0,
                plan="enterprise"
            )
            db.add(new_user)
            db.commit()
            print(f"Admin user created with password: {password}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Ensure tables exist
    models.Base.metadata.create_all(bind=engine)
    create_admin()
