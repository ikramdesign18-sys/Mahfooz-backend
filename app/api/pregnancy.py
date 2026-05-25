# app/api/pregnancy.py
# PREGNANCY TRACKING API

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.pregnancy_service import PregnancyService
from typing import Optional

router = APIRouter()
pregnancy_service = PregnancyService()

class PregnancyStart(BaseModel):
    last_period_date: str  # YYYY-MM-DD
    pre_pregnancy_weight: Optional[float] = None
    blood_group: Optional[str] = None

class WeekQuery(BaseModel):
    week: int

# Start pregnancy tracking
@router.post("/start")
def start_tracking(request: PregnancyStart):
    """Start pregnancy tracking"""
    due_date = pregnancy_service.calculate_due_date(request.last_period_date)
    current_week = pregnancy_service.calculate_current_week(request.last_period_date)
    
    return {
        "success": True,
        "message": "Pregnancy tracking started!",
        "due_date": due_date,
        "current_week": current_week,
        "trimester": pregnancy_service.get_trimester(current_week),
    }

# Get pregnancy summary
@router.get("/summary")
def get_summary(last_period_date: str):
    """Get complete pregnancy summary"""
    try:
        summary = pregnancy_service.get_pregnancy_summary(last_period_date)
        return {"success": True, **summary}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get specific week info
@router.get("/week/{week_number}")
def get_week_info(week_number: int):
    """Get detailed info for a specific week"""
    if week_number < 1 or week_number > 40:
        raise HTTPException(status_code=400, detail="Week must be between 1 and 40")
    
    info = pregnancy_service.get_week_info(week_number)
    return {"success": True, **info}

# Get trimester info
@router.get("/trimester/{trimester_number}")
def get_trimester_info(trimester_number: int):
    """Get info for entire trimester"""
    if trimester_number not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Trimester must be 1, 2, or 3")
    
    start_week = {1: 1, 2: 14, 3: 27}[trimester_number]
    end_week = {1: 13, 2: 26, 3: 40}[trimester_number]
    
    weeks_info = {}
    for week in range(start_week, end_week + 1):
        if week in pregnancy_service.data:
            weeks_info[str(week)] = pregnancy_service.get_week_info(week)
    
    return {
        "success": True,
        "trimester": trimester_number,
        "weeks_range": f"Week {start_week} to Week {end_week}",
        "weeks": weeks_info
    }

# Get danger signs
@router.get("/danger-signs")
def get_danger_signs():
    """Get all pregnancy danger signs"""
    return {
        "success": True,
        "danger_signs": pregnancy_service.advice["danger_signs"],
        "message": "🚨 If you experience ANY of these, seek medical help IMMEDIATELY!"
    }

# Get nutrition advice
@router.get("/nutrition")
def get_nutrition(week: Optional[int] = None):
    """Get nutrition advice"""
    advice = pregnancy_service.advice["nutrition"]
    
    if week and week in advice:
        specific = advice[week]
    else:
        specific = advice["general"]
    
    return {
        "success": True,
        "week_specific": specific,
        "general_advice": advice["general"],
    }

# Get exercise advice
@router.get("/exercise")
def get_exercise():
    """Get safe exercise advice"""
    return {
        "success": True,
        "advice": pregnancy_service.advice["exercise"],
    }

# Calculate due date
@router.post("/calculate-due-date")
def calculate_due(last_period_date: str):
    """Calculate due date from LMP"""
    due_date = pregnancy_service.calculate_due_date(last_period_date)
    return {
        "success": True,
        "last_period": last_period_date,
        "due_date": due_date,
        "gestation_period": "40 weeks (280 days)",
    }