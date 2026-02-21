import models
from database import SessionLocal, engine
from auth import get_password_hash

# Ensure tables are created
models.Base.metadata.create_all(bind=engine)

def create_admin_user():
    db = SessionLocal()
    
    # Check if user already exists
    admin_email = "admin@test.com"
    existing_user = db.query(models.User).filter(models.User.email == admin_email).first()
    
    if existing_user:
        print(f"L'utilisateur {admin_email} existe déjà.")
        # Force activation if it wasn't active
        existing_user.is_active = True
        db.commit()
        return

    # Create new active user
    new_user = models.User(
        name="Admin Test",
        email=admin_email,
        password_hash="admin_fallback_hash",
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    print(f"✅ Compte de test créé avec succès !")
    print(f"Email: {admin_email}")
    print(f"Mot de passe: admin123")
    
    db.close()

if __name__ == "__main__":
    create_admin_user()
