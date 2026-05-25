# app/api/medicines.py
# Medicine tracking and reminders

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.medicine import Medicine, MedicineReminder
from typing import Optional
from datetime import date, datetime

router = APIRouter()

# Request models
class MedicineCreate(BaseModel):
    family_member_id: int
    medicine_name: str
    dosage: str
    frequency: str  # once_daily, twice_daily, three_times
    timing: str  # "08:00, 20:00"
    start_date: str
    end_date: Optional[str] = None
    notes: Optional[str] = None

class ReminderUpdate(BaseModel):
    is_taken: bool

# Add medicine
@router.post("/add")
def add_medicine(request: MedicineCreate, db: Session = Depends(get_db)):
    # Convert date strings
    start = date.fromisoformat(request.start_date)
    end = None
    if request.end_date:
        end = date.fromisoformat(request.end_date)
    
    medicine = Medicine(
        family_member_id=request.family_member_id,
        medicine_name=request.medicine_name,
        dosage=request.dosage,
        frequency=request.frequency,
        timing=request.timing,
        start_date=start,
        end_date=end,
        notes=request.notes
    )
    
    db.add(medicine)
    db.commit()
    db.refresh(medicine)
    
    # Create reminders for today
    times = [t.strip() for t in request.timing.split(",")]
    for time_str in times:
        reminder = MedicineReminder(
            medicine_id=medicine.id,
            reminder_time=time_str,
            reminder_date=start
        )
        db.add(reminder)
    
    db.commit()
    
    return {
        "success": True,
        "message": "Medicine added",
        "medicine_id": medicine.id
    }

# Get all medicines for a family member
@router.get("/list/{member_id}")
def get_medicines(member_id: int, db: Session = Depends(get_db)):
    medicines = db.query(Medicine).filter(
        Medicine.family_member_id == member_id,
        Medicine.is_active == True
    ).order_by(Medicine.created_at.desc()).all()
    
    result = []
    for med in medicines:
        result.append({
            "id": med.id,
            "medicine_name": med.medicine_name,
            "dosage": med.dosage,
            "frequency": med.frequency,
            "timing": med.timing,
            "start_date": str(med.start_date),
            "end_date": str(med.end_date) if med.end_date else None,
            "reminder_enabled": med.reminder_enabled,
            "notes": med.notes
        })
    
    return {
        "success": True,
        "medicines": result,
        "total": len(result)
    }

# Get today's reminders for a member
@router.get("/today/{member_id}")
def get_today_reminders(member_id: int, db: Session = Depends(get_db)):
    today = date.today()
    
    # Get active medicines
    medicines = db.query(Medicine).filter(
        Medicine.family_member_id == member_id,
        Medicine.is_active == True
    ).all()
    
    result = []
    for med in medicines:
        # Get today's reminders
        reminders = db.query(MedicineReminder).filter(
            MedicineReminder.medicine_id == med.id,
            MedicineReminder.reminder_date == today
        ).all()
        
        for rem in reminders:
            result.append({
                "reminder_id": rem.id,
                "medicine_name": med.medicine_name,
                "dosage": med.dosage,
                "time": rem.reminder_time,
                "is_taken": rem.is_taken,
                "taken_at": str(rem.taken_at) if rem.taken_at else None
            })
    
    return {
        "success": True,
        "date": str(today),
        "reminders": result,
        "total": len(result)
    }

# Mark medicine as taken
@router.put("/taken/{reminder_id}")
def mark_taken(reminder_id: int, db: Session = Depends(get_db)):
    reminder = db.query(MedicineReminder).filter(
        MedicineReminder.id == reminder_id
    ).first()
    
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    reminder.is_taken = True
    reminder.taken_at = datetime.utcnow()
    db.commit()
    
    return {
        "success": True,
        "message": "Medicine marked as taken"
    }

# Delete medicine
@router.delete("/delete/{medicine_id}")
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    # Delete reminders first
    db.query(MedicineReminder).filter(
        MedicineReminder.medicine_id == medicine_id
    ).delete()
    
    db.delete(medicine)
    db.commit()
    
    return {
        "success": True,
        "message": "Medicine deleted"
    }