from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Service Schemas
class ServiceBase(BaseModel):
    title: str
    description: str
    price: float
    unit: str = "1000"
    category: str
    platform: str
    min_quantity: int = 100
    max_quantity: int = 10000
    cost: float = 0.0
    is_active: bool = True
    icon_name: Optional[str] = None
    color: Optional[str] = None
    bg_color: Optional[str] = None
    features: Optional[List[str]] = None

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    unit: Optional[str] = None
    category: Optional[str] = None
    platform: Optional[str] = None
    min_quantity: Optional[int] = None
    max_quantity: Optional[int] = None
    cost: Optional[float] = None
    is_active: Optional[bool] = None
    icon_name: Optional[str] = None
    color: Optional[str] = None
    bg_color: Optional[str] = None
    features: Optional[List[str]] = None

class Service(ServiceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# User Schemas
class UserMini(BaseModel):
    id: int
    name: Optional[str] = None
    email: str

class User(UserMini):
    role: str
    is_active: bool
    balance: float
    currency: str
    onboarding_completed: bool
    is_blocked: Optional[bool] = False

class UserAdmin(User):
    order_count: int = 0
    total_profit: float = 0.0

    class Config:
        from_attributes = True

class ManagerCreate(BaseModel):
    name: str
    email: str
    password: str

class ManagerTransfer(BaseModel):
    amount: float
    description: Optional[str] = "Transfert Admin"

# Order Schemas
class OrderBase(BaseModel):
    service_id: int
    quantity: int
    link: str
    total_price: float # Total price charged to the user
    proof_url: Optional[str] = None
    customer_name: Optional[str] = None
    payment_method: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: str

class Order(BaseModel):
    id: int
    user_id: int
    service_id: Optional[int]
    quantity: int
    link: str
    cost: float
    price: float
    profit: float
    status: str
    
    # Refund fields
    locked_price: float = 0.0
    refunded: bool = False
    refunded_at: Optional[datetime] = None

    transaction_id: Optional[int]
    proof_url: Optional[str] = None
    customer_name: Optional[str] = None
    payment_method: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Nested models for response
    service: Optional[Service] = None
    owner: Optional[UserMini] = None
    processed_by: Optional[int] = None

    class Config:
        from_attributes = True
# Settings Schemas
class AppSettingsBase(BaseModel):
    general: dict
    api: dict
    payment: dict
    email: dict
    security: dict
    notifications: dict

class AppSettingsUpdate(BaseModel):
    general: Optional[dict] = None
    api: Optional[dict] = None
    payment: Optional[dict] = None
    email: Optional[dict] = None
    security: Optional[dict] = None
    notifications: Optional[dict] = None

class OnboardingData(BaseModel):
    agencyName: str
    fullName: str
    phone: str
    country: str
    niche: str
    goal: str
    discovery: str

class ManagementStats(BaseModel):
    revenue: float
    cost: float
    profit: float
    order_count: int
    client_count: int
    active_services: int

class AppSettings(AppSettingsBase):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True
