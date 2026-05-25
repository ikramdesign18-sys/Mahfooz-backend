# app/api/doctor_notes.py
# Doctor visit notes and history

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.doctor_note import DoctorNote
from typing import Optional
from datetime import date

router = APIRouter()

# Request models
class DoctorNoteCreate(BaseModel):
    family_member_id: int
    doctor_name: str
    hospital_name: Optional[str] = None
    visit_date: str
    reason: str
    diagnosis: Optional[str] = None
    notes: Optional[str] = None
    prescription: Optional[str] = None
    next_visit_date: Optional[str] = None

class DoctorNoteUpdate(BaseModel):
    doctor_name: Optional[str] = None
    hospital_name: Optional[str] = None
    diagnosis: Optional[str] = None
    notes: Optional[str] = None
    prescription: Optional[str] = None
    next_visit_date: Optional[str] = None

# Add doctor note
@router.post("/add")
def add_note(request: DoctorNoteCreate, db: Session = Depends(get_db)):
    try:
        visit_date = date.fromisoformat(request.visit_date)
    except:
        visit_date = date.today()
    
    next_visit = None
    if request.next_visit_date:
        try:
            next_visit = date.fromisoformat(request.next_visit_date)
        except:
            pass
    
    note = DoctorNote(
        family_member_id=request.family_member_id,
        doctor_name=request.doctor_name,
        hospital_name=request.hospital_name,
        visit_date=visit_date,
        reason=request.reason,
        diagnosis=request.diagnosis,
        notes=request.notes,
        prescription=request.prescription,
        next_visit_date=next_visit
    )
    
    db.add(note)
    db.commit()
    db.refresh(note)
    
    return {
        "success": True,
        "message": "Doctor note added",
        "note_id": note.id
    }

# Get all doctor notes for a family member
@router.get("/list/{member_id}")
def get_notes(
    member_id: int,
    search: Optional[str] = Query(None, description="Search in doctor name, hospital, reason"),
    db: Session = Depends(get_db)
):
    query = db.query(DoctorNote).filter(
        DoctorNote.family_member_id == member_id
    )
    
    # Search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (DoctorNote.doctor_name.ilike(search_term)) |
            (DoctorNote.hospital_name.ilike(search_term)) |
            (DoctorNote.reason.ilike(search_term)) |
            (DoctorNote.diagnosis.ilike(search_term))
        )
    
    notes = query.order_by(DoctorNote.visit_date.desc()).all()
    
    result = []
    for note in notes:
        result.append({
            "id": note.id,
            "doctor_name": note.doctor_name,
            "hospital_name": note.hospital_name,
            "visit_date": str(note.visit_date),
            "reason": note.reason,
            "diagnosis": note.diagnosis,
            "notes": note.notes,
            "prescription": note.prescription,
            "next_visit_date": str(note.next_visit_date) if note.next_visit_date else None
        })
    
    return {
        "success": True,
        "notes": result,
        "total": len(result)
    }

# Get single note
@router.get("/note/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(DoctorNote).filter(DoctorNote.id == note_id).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return {
        "id": note.id,
        "family_member_id": note.family_member_id,
        "doctor_name": note.doctor_name,
        "hospital_name": note.hospital_name,
        "visit_date": str(note.visit_date),
        "reason": note.reason,
        "diagnosis": note.diagnosis,
        "notes": note.notes,
        "prescription": note.prescription,
        "next_visit_date": str(note.next_visit_date) if note.next_visit_date else None,
        "created_at": str(note.created_at)
    }

# Update doctor note
@router.put("/update/{note_id}")
def update_note(note_id: int, request: DoctorNoteUpdate, db: Session = Depends(get_db)):
    note = db.query(DoctorNote).filter(DoctorNote.id == note_id).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if request.doctor_name is not None:
        note.doctor_name = request.doctor_name
    if request.hospital_name is not None:
        note.hospital_name = request.hospital_name
    if request.diagnosis is not None:
        note.diagnosis = request.diagnosis
    if request.notes is not None:
        note.notes = request.notes
    if request.prescription is not None:
        note.prescription = request.prescription
    if request.next_visit_date is not None:
        try:
            note.next_visit_date = date.fromisoformat(request.next_visit_date)
        except:
            pass
    
    db.commit()
    
    return {"success": True, "message": "Note updated"}

# Delete doctor note
@router.delete("/delete/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(DoctorNote).filter(DoctorNote.id == note_id).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()
    
    return {"success": True, "message": "Note deleted"}

# Get upcoming appointments
@router.get("/upcoming/{member_id}")
def get_upcoming(member_id: int, db: Session = Depends(get_db)):
    today = date.today()
    
    notes = db.query(DoctorNote).filter(
        DoctorNote.family_member_id == member_id,
        DoctorNote.next_visit_date >= today
    ).order_by(DoctorNote.next_visit_date).all()
    
    result = []
    for note in notes:
        result.append({
            "id": note.id,
            "doctor_name": note.doctor_name,
            "hospital_name": note.hospital_name,
            "next_visit_date": str(note.next_visit_date),
            "reason": note.reason
        })
    
    return {
        "success": True,
        "upcoming_appointments": result,
        "total": len(result)
    }