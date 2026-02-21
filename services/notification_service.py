from sqlalchemy.orm import Session
import models
import datetime
from typing import Optional, List, Any

class NotificationService:
    @staticmethod
    def create_notification(
        db: Session,
        user_id: int,
        type: str,
        title: str,
        message: str,
        action_url: Optional[str] = None,
        action_text: Optional[str] = None,
        icon: Optional[str] = None,
        metadata: Optional[dict] = None
    ):
        db_notification = models.Notification(
            user_id=user_id,
            type=type,
            title=title,
            message=message,
            action_url=action_url,
            action_text=action_text,
            icon=icon,
            metadata_json=metadata
        )
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
        return db_notification

    @staticmethod
    def get_user_notifications(db: Session, user_id: int, limit: int = 50):
        return db.query(models.Notification)\
            .filter(models.Notification.user_id == user_id)\
            .order_by(models.Notification.created_at.desc())\
            .limit(limit)\
            .all()

    @staticmethod
    def get_unread_count(db: Session, user_id: int):
        return db.query(models.Notification)\
            .filter(models.Notification.user_id == user_id, models.Notification.read == False)\
            .count()

    @staticmethod
    def mark_as_read(db: Session, notification_id: int, user_id: int):
        notification = db.query(models.Notification)\
            .filter(models.Notification.id == notification_id, models.Notification.user_id == user_id)\
            .first()
        if notification:
            notification.read = True
            db.commit()
            return True
        return False

    @staticmethod
    def mark_all_as_read(db: Session, user_id: int):
        db.query(models.Notification)\
            .filter(models.Notification.user_id == user_id, models.Notification.read == False)\
            .update({"read": True})
        db.commit()

# Convenience functions for common notification types
def notify_page_generated(db: Session, user_id: int, page_name: str):
    return NotificationService.create_notification(
        db, user_id,
        type="success",
        title="Landing page générée !",
        message=f"\"{page_name}\" est prête à être publiée",
        icon="✅"
    )

def notify_limit_reached(db: Session, user_id: int, feature_name: str, usage: int, limit: int):
    return NotificationService.create_notification(
        db, user_id,
        type="warning",
        title="Limite presque atteinte",
        message=f"{usage}/{limit} {feature_name} créées ce mois. Upgrade pour continuer",
        icon="⚠️",
        action_url="/settings/billing",
        action_text="Upgrade"
    )

def notify_new_sale(db: Session, user_id: int, amount: float, currency: str, product_name: str):
    return NotificationService.create_notification(
        db, user_id,
        type="success",
        title="Nouvelle vente détectée",
        message=f"{amount}{currency} via \"{product_name}\"",
        icon="🎉"
    )

def notify_subscription_active(db: Session, user_id: int):
    return NotificationService.create_notification(
        db, user_id,
        type="feature",
        title="Paiement confirmé",
        message="Votre abonnement Pro est maintenant actif. Toutes les features sont débloquées !",
        icon="💳"
    )
