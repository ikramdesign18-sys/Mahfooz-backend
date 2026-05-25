# app/api/auth.py
# Phone number login with OTP

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.sms_service import SMSService

sms_service = SMSService()
from app.models.user import User
import random
from datetime import datetime, timedelta

router = APIRouter()

# Store OTPs temporarily (in production, use Redis)
otp_store = {}

# Request models
class SendOTPRequest(BaseModel):
    phone_number: str

class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp: str

class UserCreate(BaseModel):
    phone_number: str
    full_name: str = ""
    email: str = ""

# Send OTP
@router.post("/send-otp")
def send_otp(request: SendOTPRequest):
    """Send OTP to phone number"""
    result = sms_service.send_otp(request.phone_number)
    
    if result["success"]:
        return {
            "success": True,
            "message": "OTP sent successfully",
            "expires_in": "5 minutes",
            # In development only - remove in production
            "otp": result.get("otp", "Sent via SMS"),
        }
    
    raise HTTPException(status_code=500, detail="Failed to send OTP")

# Verify OTP and Login
@router.post("/verify-otp")
def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    """Verify OTP and login"""
    is_valid, message = sms_service.verify_otp(request.phone_number, request.otp)
    
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    # Find or create user
    user = db.query(User).filter(User.phone_number == request.phone_number).first()
    
    if not user:
        user = User(phone_number=request.phone_number)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return {
        "success": True,
        "message": "Login successful",
        "user_id": user.id,
        "phone_number": user.phone_number,
        "full_name": user.full_name,
        "is_new_user": user.full_name == ""
    }

# Update user profile
@router.put("/update-profile")
def update_profile(request: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == request.phone_number).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.full_name = request.full_name
    user.email = request.email
    db.commit()
    
    return {
        "success": True,
        "message": "Profile updated"
    }

# Get user by phone
@router.get("/user/{phone_number}")
def get_user(phone_number: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == phone_number).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "phone_number": user.phone_number,
        "full_name": user.full_name,
        "email": user.email,
        "is_verified": user.is_verified
    }