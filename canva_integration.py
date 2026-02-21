import os
import httpx
import json
import datetime
import secrets
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
import models
from auth import decode_access_token

router = APIRouter(prefix="/canva", tags=["canva"])

# In-memory store for OAuth state (for demo purposes)
# In production, use Redis or a database
state_store = {}

CANVA_CLIENT_ID = os.getenv("CANVA_CLIENT_ID")
CANVA_CLIENT_SECRET = os.getenv("CANVA_CLIENT_SECRET")
CANVA_REDIRECT_URI = os.getenv("CANVA_REDIRECT_URI", "http://localhost:8000/api/canva/callback")
CANVA_API_BASE_URL = "https://api.canva.com/rest/v1"
CANVA_AUTH_URL = "https://www.canva.com/api/oauth/authorize"
CANVA_TOKEN_URL = f"{CANVA_API_BASE_URL}/oauth/token"

SCOPES = [
    "design:read",
    "design:write",
    "design:content:read",
    "design:content:write",
    "asset:read",
    "asset:write",
    "folder:read",
    "brandtemplate:read",
    "brandtemplate:write"
]

# Auth dependency
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authorized")
    
    token = auth_header.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    email = payload.get("sub")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

class CanvaClient:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    async def create_design_from_template(self, brand_template_id: str, data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{CANVA_API_BASE_URL}/autofills",
                headers=self.headers,
                json={
                    "brand_template_id": brand_template_id,
                    "data": data
                }
            )
            response.raise_for_status()
            return response.json()

    async def get_edit_url(self, design_id: str, return_url: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{CANVA_API_BASE_URL}/designs/{design_id}/edit",
                headers=self.headers,
                json={"return_url": return_url}
            )
            response.raise_for_status()
            return response.json()

    async def export_design(self, design_id: str, format_type: str = "png"):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{CANVA_API_BASE_URL}/exports",
                headers=self.headers,
                json={
                    "design_id": design_id,
                    "format": {"type": format_type}
                }
            )
            response.raise_for_status()
            return response.json()

    async def get_export_status(self, export_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{CANVA_API_BASE_URL}/exports/{export_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

async def get_valid_token(user_id: int, db: Session):
    token_record = db.query(models.CanvaToken).filter(models.CanvaToken.user_id == user_id).first()
    if not token_record:
        return None
    
    if datetime.datetime.utcnow() >= token_record.expires_at:
        # Refresh token
        async with httpx.AsyncClient() as client:
            response = await client.post(
                CANVA_TOKEN_URL,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": token_record.refresh_token,
                    "client_id": CANVA_CLIENT_ID,
                    "client_secret": CANVA_CLIENT_SECRET
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            if response.status_code != 200:
                return None
            
            data = response.json()
            token_record.access_token = data["access_token"]
            token_record.refresh_token = data.get("refresh_token", token_record.refresh_token)
            token_record.expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=data["expires_in"])
            db.commit()
            
    return token_record.access_token

@router.get("/auth/login")
async def canva_auth_login(user: models.User = Depends(get_current_user)):
    state = secrets.token_hex(16)
    # Store state to link it back to user in callback
    state_store[state] = user.id
    
    auth_url = f"{CANVA_AUTH_URL}?response_type=code&client_id={CANVA_CLIENT_ID}&redirect_uri={CANVA_REDIRECT_URI}&scope={' '.join(SCOPES)}&state={state}"
    return {"authUrl": auth_url}

@router.get("/callback")
async def canva_callback(code: str, state: str, db: Session = Depends(get_db)):
    user_id = state_store.get(state)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid state")
    
    # Clean up state
    del state_store[state]

    async with httpx.AsyncClient() as client:
        response = await client.post(
            CANVA_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": CANVA_REDIRECT_URI,
                "client_id": CANVA_CLIENT_ID,
                "client_secret": CANVA_CLIENT_SECRET
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange code for token")
        
        data = response.json()
        
        token_record = db.query(models.CanvaToken).filter(models.CanvaToken.user_id == user_id).first()
        if token_record:
            token_record.access_token = data["access_token"]
            token_record.refresh_token = data["refresh_token"]
            token_record.expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=data["expires_in"])
        else:
            token_record = models.CanvaToken(
                user_id=user_id,
                access_token=data["access_token"],
                refresh_token=data["refresh_token"],
                expires_at=datetime.datetime.utcnow() + datetime.timedelta(seconds=data["expires_in"])
            )
            db.add(token_record)
        
        db.commit()
        
    return RedirectResponse(url="http://localhost:5173/studio_ai?canva_connected=true")

@router.get("/check-connection")
async def check_connection(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    token = await get_valid_token(user.id, db)
    return {"connected": token is not None}

@router.post("/create-design")
async def create_design(
    templateId: str = None, 
    data: dict = None, 
    user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    access_token = await get_valid_token(user.id, db)
    if not access_token:
        raise HTTPException(status_code=401, detail="Canva not connected")
    
    canva = CanvaClient(access_token)
    
    try:
        if templateId:
            result = await canva.create_design_from_template(templateId, data or {})
            design_id = result["design"]["id"]
        else:
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    f"{CANVA_API_BASE_URL}/designs",
                    headers=canva.headers,
                    json={"design_type": "Presentation"}
                )
                res.raise_for_status()
                design_id = res.json()["design"]["id"]
        
        edit_data = await canva.get_edit_url(design_id, return_url="http://localhost:5173/studio_ai")
        
        new_design = models.CanvaDesign(
            user_id=user.id,
            design_id=design_id,
            edit_url=edit_data["url"],
            status="editing",
            data=json.dumps(data) if data else None
        )
        db.add(new_design)
        db.commit()
        
        return {"success": True, "designId": design_id, "editUrl": edit_data["url"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export")
async def export_design(
    designId: str, 
    user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    access_token = await get_valid_token(user.id, db)
    if not access_token:
        raise HTTPException(status_code=401, detail="Canva not connected")
    
    canva = CanvaClient(access_token)
    try:
        export_job = await canva.export_design(designId)
        return {"success": True, "exportJobId": export_job["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export-status/{jobId}")
async def export_status(
    jobId: str, 
    user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    access_token = await get_valid_token(user.id, db)
    if not access_token:
        raise HTTPException(status_code=401, detail="Canva not connected")
        
    canva = CanvaClient(access_token)
    try:
        status = await canva.get_export_status(jobId)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
