import redis
import json
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import models
from typing import Dict, Any

# Configure Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

class AnalyticsService:
    async def get_dashboard_stats(self, user_id: int, db: Session, period_days: int = 30) -> Dict[str, Any]:
        """
        Retrieves dashboard statistics with Redis caching.
        Cache TTL: 5 minutes.
        """
        cache_key = f"analytics:dashboard:{user_id}:{period_days}"
        
        # Try to get from cache
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
        
        # Calculate stats
        start_date = datetime.utcnow() - timedelta(days=period_days)
        
        total_conv = db.query(models.WhatsAppConversation).filter(
            models.WhatsAppConversation.user_id == user_id,
            models.WhatsAppConversation.created_at >= start_date
        ).count()
        
        received_msgs = db.query(models.WhatsAppMessage).filter(
            models.WhatsAppMessage.user_id == user_id,
            models.WhatsAppMessage.direction == "incoming",
            models.WhatsAppMessage.timestamp >= start_date
        ).count()
        
        sent_msgs = db.query(models.WhatsAppMessage).filter(
            models.WhatsAppMessage.user_id == user_id,
            models.WhatsAppMessage.direction == "outgoing",
            models.WhatsAppMessage.timestamp >= start_date
        ).count()
        
        # Calculate response rate
        response_rate = 0
        if received_msgs > 0:
            response_rate = round((sent_msgs / received_msgs) * 100)
            
        stats = {
            "conversations": total_conv,
            "response_rate": response_rate,
            "sales": {"amount": 0.0, "count": 0}, # To be implemented with store data
            "messages": {
                "received": received_msgs,
                "sent": sent_msgs
            },
            "period_days": period_days
        }
        
        # Cache the result for 5 minutes
        redis_client.setex(cache_key, 300, json.dumps(stats))
        
        return stats

analytics_service = AnalyticsService()
