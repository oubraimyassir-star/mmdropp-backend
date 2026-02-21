from database import SessionLocal
import models
import uuid

def create_test_order():
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == 'oubraimyassir@gmail.com').first()
        service = db.query(models.Service).first()
        
        if not user or not service:
            print("User or Service not found")
            return

        tx_id = f"REF-{uuid.uuid4().hex[:8].upper()}"
        transaction = models.Transaction(
            user_id=user.id,
            transaction_id=tx_id,
            type="purchase",
            description=f"TEST ORDER {service.title}",
            amount=-10.0,
            status="completed"
        )
        db.add(transaction)
        db.flush()

        order = models.Order(
            user_id=user.id,
            service_id=service.id,
            quantity=1000,
            link="https://test.com",
            cost=7.0,
            price=10.0,
            profit=3.0,
            status="pending",
            transaction_id=transaction.id
        )
        db.add(order)
        db.commit()
        print(f"Created test order ID: {order.id}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_order()
