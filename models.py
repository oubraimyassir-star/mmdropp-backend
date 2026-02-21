from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Text, Float, JSON, Numeric, Index
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_active = Column(Boolean, default=False)
    stripe_session_id = Column(String, nullable=True)
    stripe_customer_id = Column(String, nullable=True)
    
    # Role based access (user, admin)
    role = Column(String, default="user")
    
    # Tier & Limits
    plan = Column(String, default="enterprise") # starter, pro, enterprise
    
    # Usage Tracking
    landing_pages_used_this_month = Column(Integer, default=0)
    ai_images_used_this_month = Column(Integer, default=0)
    email_campaigns_used_this_month = Column(Integer, default=0)
    whatsapp_messages_used_this_month = Column(Integer, default=0)
    stores_connected_count = Column(Integer, default=0)
    
    # Legacy/Generic counters (can be kept or deprecated)
    usage_count = Column(Integer, default=0)
    usage_limit = Column(Integer, default=10)
    
    onboarding_completed = Column(Boolean, default=False)
    onboarding_data = Column(JSON, nullable=True)
    currency = Column(String, default="USD")
    balance = Column(Float, default=0.0)
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    generations = relationship("Generation", back_populates="owner")
    platform_connections = relationship("PlatformConnection", back_populates="owner")
    imported_products = relationship("ImportedProduct", back_populates="owner")
    conversions = relationship("Conversion", back_populates="owner")
    leads = relationship("Lead", back_populates="owner")
    analytics = relationship("AnalyticsEvent", back_populates="owner")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="owner")

class Generation(Base):
    __tablename__ = "generations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String) # landing, seo, social, image
    data = Column(Text) # JSON content
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="generations")

class PlatformConnection(Base):
    __tablename__ = "platform_connections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    platform = Column(String) # shopify, woocommerce, prestashop, youcan
    shop_domain = Column(String, nullable=True)
    shop_url = Column(String, nullable=True)
    access_token = Column(Text, nullable=True)
    api_key = Column(Text, nullable=True)
    api_secret = Column(Text, nullable=True)
    webhook_secret = Column(String, nullable=True)
    last_sync_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="platform_connections")
    webhooks = relationship("PlatformWebhook", back_populates="connection")

class ImportedProduct(Base):
    __tablename__ = "imported_products"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    platform = Column(String)
    external_id = Column(String)
    name = Column(String)
    price = Column(Float)
    description = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    sku = Column(String, nullable=True)
    data = Column(JSON, nullable=True) # Full product data
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="imported_products")

class PlatformWebhook(Base):
    __tablename__ = "platform_webhooks"

    id = Column(Integer, primary_key=True, index=True)
    connection_id = Column(Integer, ForeignKey("platform_connections.id"))
    webhook_id = Column(String, nullable=True)
    topic = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    connection = relationship("PlatformConnection", back_populates="webhooks")

class Conversion(Base):
    __tablename__ = "conversions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    landing_page_id = Column(Integer, nullable=True)
    platform = Column(String)
    external_order_id = Column(String)
    amount = Column(Float)
    currency = Column(String, default="EUR")
    status = Column(String, default="completed")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="conversions")

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email = Column(String)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    source = Column(String, nullable=True) # landing_page, contact_form
    status = Column(String, default="new") # new, contacted, converted
    data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="leads")

class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    landing_page_id = Column(Integer, nullable=True)
    event_type = Column(String) # page_view, click, convert
    ip_address = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)
    referrer = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="analytics")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String) # success, info, warning, error, feature
    title = Column(String)
    message = Column(Text)
    action_url = Column(String, nullable=True)
    action_text = Column(String, nullable=True)
    icon = Column(String, nullable=True)
    metadata_json = Column(JSON, nullable=True)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="notifications")
class ABTest(Base):
    __tablename__ = "ab_tests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    original_generation_id = Column(Integer, ForeignKey("generations.id"))
    variant_generation_id = Column(Integer, ForeignKey("generations.id"))
    status = Column(String, default="active") # active, completed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User")
    original = relationship("Generation", foreign_keys=[original_generation_id])
    variant = relationship("Generation", foreign_keys=[variant_generation_id])

class CanvaToken(Base):
    __tablename__ = "canva_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    access_token = Column(Text)
    refresh_token = Column(Text)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class CanvaDesign(Base):
    __tablename__ = "canva_designs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    design_id = Column(String, unique=True, index=True)
    edit_url = Column(Text, nullable=True)
    exported_url = Column(Text, nullable=True)
    status = Column(String, default="editing") # editing, completed, failed
    data = Column(JSON, nullable=True) # Autofill data if used
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# WhatsApp Marketing Models
class WhatsAppContact(Base):
    __tablename__ = "whatsapp_contacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    phone_number = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, nullable=True)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    owner = relationship("User")
    messages = relationship("WhatsAppMessage", back_populates="contact")
    conversations = relationship("WhatsAppConversation", back_populates="contact")

class WhatsAppConversation(Base):
    __tablename__ = "whatsapp_conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    contact_id = Column(Integer, ForeignKey("whatsapp_contacts.id"))
    status = Column(String, default="active") # active, closed, archived
    last_message_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User")
    contact = relationship("WhatsAppContact", back_populates="conversations")
    messages = relationship("WhatsAppMessage", back_populates="conversation")

class WhatsAppMessage(Base):
    __tablename__ = "whatsapp_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    whatsapp_id = Column(String, unique=True, index=True) # WhatsApp message ID from Meta
    conversation_id = Column(Integer, ForeignKey("whatsapp_conversations.id"))
    contact_id = Column(Integer, ForeignKey("whatsapp_contacts.id"))
    direction = Column(String) # incoming, outgoing
    content = Column(Text)
    type = Column(String) # text, image, button, template
    status = Column(String) # sent, delivered, read, failed
    timestamp = Column(DateTime)
    metadata_json = Column(JSON, nullable=True)
    ai_generated = Column(Boolean, default=False)
    error_code = Column(Integer, nullable=True)
    error_message = Column(String, nullable=True)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        Index('idx_contact_timestamp', 'contact_id', 'timestamp'),
        Index('idx_conversation_timestamp', 'conversation_id', 'timestamp'),
        Index('idx_direction_status', 'direction', 'status'),
    )

    owner = relationship("User")
    conversation = relationship("WhatsAppConversation", back_populates="messages")
    contact = relationship("WhatsAppContact", back_populates="messages")

class WhatsAppAbandonedCart(Base):
    __tablename__ = "whatsapp_abandoned_carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    contact_id = Column(Integer, ForeignKey("whatsapp_contacts.id"))
    cart_data = Column(JSON) # Items, total, etc.
    recovery_attempts = Column(Integer, default=0)
    recovered = Column(Boolean, default=False)
    recovered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime)

    __table_args__ = (
        Index('idx_contact_recovered', 'contact_id', 'recovered'),
        Index('idx_expires_recovered', 'expires_at', 'recovered'),
    )

    owner = relationship("User")
    contact = relationship("WhatsAppContact")

class WhatsAppCampaign(Base):
    __tablename__ = "whatsapp_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    message = Column(Text)
    target_audience = Column(JSON) # Filters
    status = Column(String, default="draft") # draft, scheduled, sent
    scheduled_at = Column(DateTime, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    stats = Column(JSON, nullable=True) # sent, delivered, read, replies
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User")

class WhatsAppAnalytics(Base):
    __tablename__ = "whatsapp_analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    total_conversations = Column(Integer, default=0)
    new_conversations = Column(Integer, default=0)
    messages_received = Column(Integer, default=0)
    messages_sent = Column(Integer, default=0)
    response_rate = Column(Float, default=0.0)
    sales_amount = Column(Float, default=0.0)
    sales_count = Column(Integer, default=0)

    owner = relationship("User")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    transaction_id = Column(String, unique=True, index=True)
    type = Column(String) # deposit, purchase
    description = Column(String)
    amount = Column(Float)
    currency = Column(String, default="EUR")
    status = Column(String, default="completed") # pending, completed, failed
    payment_method = Column(String, nullable=True)
    receipt_url = Column(String, nullable=True)
    reference_order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="transactions")

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    unit = Column(String, default="1000") # 1000, 1, pack, mois
    category = Column(String)
    platform = Column(String)
    min_quantity = Column(Integer, default=100)
    max_quantity = Column(Integer, default=10000)
    cost = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    # Frontend props store
    icon_name = Column(String, nullable=True) 
    color = Column(String, nullable=True)
    bg_color = Column(String, nullable=True)
    features = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True)
    
    quantity = Column(Integer)
    link = Column(String)
    
    cost = Column(Float) # Cost to us
    price = Column(Float) # Price charged to user
    profit = Column(Float)
    
    status = Column(String, default="pending") # pending, processing, completed, cancelled
    
    # Optional link to financial transaction
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)
    
    # Proof of payment or order-related image
    proof_url = Column(String, nullable=True)
    
    # Specific details for the order
    customer_name = Column(String, nullable=True)
    payment_method = Column(String, nullable=True)
    
    # Financials for refund logic
    locked_price = Column(Float, default=0.0) # The price user paid at order time
    refunded = Column(Boolean, default=False)
    refunded_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Tracking who processed the order
    processed_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    owner = relationship("User", back_populates="orders", foreign_keys=[user_id])
    service = relationship("Service")
    processor = relationship("User", foreign_keys=[processed_by])

class AppSettings(Base):
    __tablename__ = "app_settings"

    id = Column(Integer, primary_key=True, index=True)
    # Key settings categories stored as JSON
    general = Column(JSON, default={
        "site_name": "SMMADROOP",
        "site_url": "https://smmadroop.com",
        "currency": "USD",
        "maintenance_mode": False,
        "registration_open": True,
        "auto_activate": False
    })
    api = Column(JSON, default={
        "smm_api_key": "",
        "smm_api_url": "",
        "google_client_id": "",
        "google_secret": ""
    })
    payment = Column(JSON, default={
        "stripe_key": "",
        "stripe_secret": "",
        "paypal_enabled": False,
        "paypal_client_id": "",
        "min_deposit": 5.0,
        "max_deposit": 1000.0
    })
    email = Column(JSON, default={
        "smtp_host": "smtp.gmail.com",
        "smtp_port": 587,
        "smtp_user": "",
        "smtp_pass": "",
        "email_from": "noreply@smmadroop.com",
        "email_order_confirm": True,
        "email_low_balance": True
    })
    security = Column(JSON, default={
        "two_factor_admin": True,
        "rate_limiting": True,
        "login_attempts": 5,
        "session_timeout": 60,
        "ip_whitelist": ""
    })
    notifications = Column(JSON, default={
        "notif_new_order": True,
        "notif_new_user": True,
        "notif_low_balance": False,
        "notif_order_fail": True,
        "telegram_token": "",
        "telegram_chat_id": ""
    })
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# Update User relationship
User.orders = relationship("Order", back_populates="owner", foreign_keys="[Order.user_id]")
User.processed_orders = relationship("Order", back_populates="processor", foreign_keys="[Order.processed_by]")

