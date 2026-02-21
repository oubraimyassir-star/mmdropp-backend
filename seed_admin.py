import sys
import os

# Add the current directory to sys.path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
import models
import auth

def seed_admin():
    db = SessionLocal()
    email = "oubraimyassir@gmail.com"
    password = "Jad.1233"
    
    # Check if user exists
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if user:
        print(f"User {email} already exists. Updating role and password.")
        user.role = "admin"
        user.is_active = True
        user.password_hash = auth.get_password_hash(password)
    else:
        print(f"Creating new admin user: {email}")
        user = models.User(
            name="Yassir Oubraim",
            email=email,
            password_hash=auth.get_password_hash(password),
            role="admin",
            is_active=True,
            onboarding_completed=True,
            balance=0.0,
            currency="EUR"
        )
        db.add(user)
    
    db.commit()
    print("Admin user seeded successfully.")
    db.close()

if __name__ == "__main__":
    seed_admin()
