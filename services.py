from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/services",
    tags=["services"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[schemas.Service])
async def get_services(
    category: Optional[str] = None,
    platform: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Service).filter(models.Service.is_active == True)
    
    if category and category != "Tous":
        query = query.filter(models.Service.category == category)
    
    if platform:
         query = query.filter(models.Service.platform == platform)
         
    return query.all()
