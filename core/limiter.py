from fastapi import HTTPException, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
import models
from core.config import PLAN_LIMITS

class SubscriptionLimiter:
    def __init__(self, feature: str):
        self.feature = feature

    async def __call__(self, request: Request, db: Session = Depends(get_db)):
        # Authentication is handled by previous dependency (get_current_user) usually,
        # but we need to fetch the user again or rely on request.state if available.
        # For simplicity and robustness, we'll fetch user from local dependency in main if needed,
        # but pure dependencies don't share data easily unless we use a higher level approach.
        #
        # A common pattern: usage via function injection in the route.
        # But to be used as `Depends(check_limit('feature'))`, we need the user.
        # We will assume `get_current_user` is called BEFORE this dependency in the route list
        # or we explicitly call it here.
        pass

# Since we need the user object, it's easier to create a function that returns a dependency
# which takes the user as an argument.

def check_subscription_limit(feature: str):
    def dependency(user: models.User, db: Session = Depends(get_db)):
        plan = user.plan or "starter"
        limits = PLAN_LIMITS.get(plan, PLAN_LIMITS["starter"])
        
        limit = limits.get(feature, 0)
        
        # Determine current usage based on feature
        current_usage = 0
        if feature == "landing_pages_per_month":
            current_usage = user.landing_pages_used_this_month
        elif feature == "ai_images_per_month":
            current_usage = user.ai_images_used_this_month
        elif feature == "email_campaigns_per_month":
            current_usage = user.email_campaigns_used_this_month
        elif feature == "whatsapp_messages_per_month":
            current_usage = user.whatsapp_messages_used_this_month
        elif feature == "connected_stores":
            current_usage = user.stores_connected_count
            
        if current_usage >= limit:
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Limit reached",
                    "message": f"Vous avez atteint la limite de {limit} pour votre plan {plan}.",
                    "current_usage": current_usage,
                    "limit": limit,
                    "upgrade_url": "/settings"
                }
            )
        return True
    return dependency

def increment_usage(user: models.User, feature: str, db: Session):
    if feature == "landing_pages_per_month":
        user.landing_pages_used_this_month += 1
    elif feature == "ai_images_per_month":
        user.ai_images_used_this_month += 1
    elif feature == "email_campaigns_per_month":
        user.email_campaigns_used_this_month += 1
    elif feature == "whatsapp_messages_per_month":
        user.whatsapp_messages_used_this_month += 1
    elif feature == "connected_stores":
        user.stores_connected_count += 1
        
    db.commit()
