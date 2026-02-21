from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import models
import schemas
from database import get_db
from auth import get_current_admin, get_current_user, create_access_token

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

@router.get("/stats")
async def get_admin_stats(
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    # Total Revenue (sum of all money spent by users)
    total_revenue = db.query(func.sum(func.abs(models.Transaction.amount))).filter(
        models.Transaction.status == "completed",
        models.Transaction.type == "purchase"
    ).scalar() or 0.0

    # Total Profit (sum of profit from completed orders)
    total_profit = db.query(func.sum(models.Order.profit)).filter(
        models.Order.status == "completed"
    ).scalar() or 0.0

    # Total Users
    total_users = db.query(models.User).count()

    # Online Users (Mock for now, or could use a 5-min activity window)
    # Using a 5-minute activity window if we had 'last_active'
    online_users = 1 # Always at least the admin

    # Total Orders
    total_orders = db.query(models.Order).count()
    
    # Active Services
    active_services = db.query(models.Service).filter(models.Service.is_active == True).count()

    return {
        "revenue": {
            "total": total_revenue,
            "profit": total_profit,
            "trend": "+0%", # Placeholder
            "data": [0, 0, 0, 0, 0, 0, total_revenue]
        },
        "users": {
            "total": total_users,
            "online": online_users,
            "trend": "+0%",
            "data": [0, 0, 0, 0, 0, 0, total_users]
        },
        "orders": {
            "total": total_orders,
            "trend": "+0%",
            "data": [0, 0, 0, 0, 0, 0, total_orders]
        },
        "active_services": active_services
    }

# --- Users ---
# --- Users ---
@router.get("/users")
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    users = db.query(models.User).offset(skip).limit(limit).all()
    
    users_data = []
    for user in users:
        # Calculate spent based on Orders
        spent = db.query(func.sum(models.Order.price)).filter(models.Order.user_id == user.id).scalar() or 0.0
        
        users_data.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "balance": user.balance,
            "is_active": user.is_active,
            "role": user.role,
            "spent": spent,
            "created_at": user.created_at
        })
        
    return users_data

@router.get("/users/{user_id}/details")
async def get_user_details(
    user_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    spent = db.query(func.sum(models.Order.price)).filter(models.Order.user_id == user.id).scalar() or 0.0
    order_count = db.query(models.Order).filter(models.Order.user_id == user.id).count()
    
    # Get recent orders
    recent_orders = db.query(models.Order).filter(models.Order.user_id == user.id)\
        .order_by(models.Order.created_at.desc()).limit(5).all()
        
    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "balance": user.balance,
            "is_active": user.is_active,
            "role": user.role,
            "created_at": user.created_at
        },
        "stats": {
            "spent": spent,
            "order_count": order_count
        },
        "recent_orders": recent_orders
    }

# --- Orders ---
@router.get("/orders", response_model=List[schemas.Order])
async def get_orders(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    query = db.query(models.Order)
    if status:
        query = query.filter(models.Order.status == status)
    
    orders = query.order_by(models.Order.created_at.desc()).offset(skip).limit(limit).all()
    return orders

@router.put("/orders/{order_id}/status", response_model=schemas.Order)
async def update_order_status(
    order_id: int,
    status_update: schemas.OrderUpdate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status_update.status
    db.commit()
    db.refresh(order)
    return order

# --- Services ---
@router.get("/services", response_model=List[schemas.Service])
async def get_admin_services(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    services = db.query(models.Service).offset(skip).limit(limit).all()
    return services

@router.post("/services", response_model=schemas.Service)
async def create_service(
    service: schemas.ServiceCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    db_service = models.Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

@router.put("/services/{service_id}", response_model=schemas.Service)
async def update_service(
    service_id: int,
    service_update: schemas.ServiceUpdate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    update_data = service_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_service, key, value)
    
    db.commit()
    db.refresh(db_service)
    return db_service

@router.delete("/services/{service_id}")
async def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin)
):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    db.delete(db_service)
    db.commit()
    return {"message": "Service deleted successfully"}

