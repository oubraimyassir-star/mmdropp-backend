from celery import Celery
import os
from datetime import datetime, timedelta
from database import SessionLocal
import models
from services.whatsapp_service import whatsapp_service
from services.ai_marketing import ai_marketing_service
import json

# Configure Celery to use Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("marketing_tasks", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task
async def process_abandoned_carts():
    """
    Background task to find abandoned carts and send recovery messages with A/B testing.
    """
    db = SessionLocal()
    try:
        # A/B Testing Strategies
        strategies = [
            {"name": "urgency", "prompt": "urgent but friendly, stock is moving fast"},
            {"name": "discount", "prompt": "offer a special 10% discount to complete purchase"},
            {"name": "social_proof", "prompt": "mention that 20 other people are looking at these items"},
            {"name": "help", "prompt": "simply ask if they had any trouble with the checkout"}
        ]
        
        cutoff = datetime.utcnow() - timedelta(minutes=30)
        recent_limit = datetime.utcnow() - timedelta(hours=24)
        
        carts = db.query(models.WhatsAppAbandonedCart).filter(
            models.WhatsAppAbandonedCart.recovered == False,
            models.WhatsAppAbandonedCart.created_at <= cutoff,
            models.WhatsAppAbandonedCart.created_at >= recent_limit
        ).all()
        
        import random
        
        for cart in carts:
            contact = cart.contact
            if not contact:
                continue
            
            # Select A/B Strategy
            strategy = random.choice(strategies)
                
            # Generate AI Recovery Message
            cart_data = cart.cart_data 
            items = cart_data.get("items", [])
            item_names = ", ".join([i.get("name", "produit") for i in items])
            
            recovery_text = await ai_marketing_service.generate_response({
                "customer_name": contact.name,
                "intent": "abandoned_cart",
                "cart_content": item_names,
                "total": cart_data.get("total", 0),
                "strategy_hint": strategy["prompt"]
            })
            
            # Send WhatsApp
            success = await whatsapp_service.send_text_message(contact.phone_number, recovery_text)
            
            if success:
                cart.recovered = True
                cart.recovered_at = datetime.utcnow()
                cart.metadata_json = {"strategy": strategy["name"]}
                
                # Create a conversation and message entry
                conversation = db.query(models.WhatsAppConversation).filter(
                    models.WhatsAppConversation.contact_id == contact.id,
                    models.WhatsAppConversation.status == "active"
                ).first()
                if not conversation:
                    conversation = models.WhatsAppConversation(
                        user_id=cart.user_id,
                        contact_id=contact.id,
                        status="active"
                    )
                    db.add(conversation)
                    db.flush()
                
                db_msg = models.WhatsAppMessage(
                    user_id=cart.user_id,
                    whatsapp_id=f"recovery_{cart.id}",
                    conversation_id=conversation.id,
                    contact_id=contact.id,
                    direction="outgoing",
                    content=recovery_text,
                    type="text",
                    status="sent",
                    timestamp=datetime.utcnow(),
                    ai_generated=True
                )
                db.add(db_msg)
        
        db.commit()
    except Exception as e:
        print(f"Error in process_abandoned_carts: {e}")
        db.rollback()
    finally:
        db.close()

# Schedule configuration (optional, usually done in a beat file or app config)
celery_app.conf.beat_schedule = {
    'check-abandoned-carts-every-15-mins': {
        'task': 'tasks.process_abandoned_carts',
        'schedule': 900.0, # 15 minutes
    },
}
