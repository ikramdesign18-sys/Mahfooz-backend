# app/api/family.py
# Add and manage family members

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.family import FamilyMember
from typing import Optional
from datetime import date

router = APIRouter()

# Request models
class FamilyMemberCreate(BaseModel):
    user_id: int
    name: str
    relation: str  # father, mother, son, daughter, etc.
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    allergies: Optional[str] = None
    chronic_diseases: Optional[str] = None
    emergency_contact: Optional[str] = None

class FamilyMemberUpdate(BaseModel):
    name: Optional[str] = None
    relation: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    allergies: Optional[str] = None
    chronic_diseases: Optional[str] = None
    emergency_contact: Optional[str] = None

# Add family member
@router.post("/add")
def add_family_member(request: FamilyMemberCreate, db: Session = Depends(get_db)):
    # Convert date string to date object
    dob = None
    if request.date_of_birth:
        try:
            dob = date.fromisoformat(request.date_of_birth)
        except:
            pass
    
    member = FamilyMember(
        user_id=request.user_id,
        name=request.name,
        relation=request.relation,
        date_of_birth=dob,
        gender=request.gender,
        blood_group=request.blood_group,
        height=request.height,
        weight=request.weight,
        allergies=request.allergies,
        chronic_diseases=request.chronic_diseases,
        emergency_contact=request.emergency_contact
    )
    
    db.add(member)
    db.commit()
    db.refresh(member)
    
    return {
        "success": True,
        "message": "Family member added",
        "member_id": member.id,
        "name": member.name
    }

# Get all family members for a user
@router.get("/list/{user_id}")
def get_family_members(user_id: int, db: Session = Depends(get_db)):
    members = db.query(FamilyMember).filter(
        FamilyMember.user_id == user_id
    ).all()
    
    result = []
    for member in members:
        result.append({
            "id": member.id,
            "name": member.name,
            "relation": member.relation,
            "gender": member.gender,
            "blood_group": member.blood_group,
            "age": member.date_of_birth,
            "allergies": member.allergies,
            "chronic_diseases": member.chronic_diseases,
            "emergency_contact": member.emergency_contact
        })
    
    return {
        "success": True,
        "family_members": result,
        "total": len(result)
    }

# Get single family member details
@router.get("/member/{member_id}")
def get_family_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(FamilyMember).filter(FamilyMember.id == member_id).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    return {
        "id": member.id,
        "user_id": member.user_id,
        "name": member.name,
        "relation": member.relation,
        "date_of_birth": str(member.date_of_birth) if member.date_of_birth else None,
        "gender": member.gender,
        "blood_group": member.blood_group,
        "height": member.height,
        "weight": member.weight,
        "allergies": member.allergies,
        "chronic_diseases": member.chronic_diseases,
        "emergency_contact": member.emergency_contact,
        "created_at": str(member.created_at)
    }

# Update family member
@router.put("/update/{member_id}")
def update_family_member(
    member_id: int, 
    request: FamilyMemberUpdate, 
    db: Session = Depends(get_db)
):
    member = db.query(FamilyMember).filter(FamilyMember.id == member_id).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Update only provided fields
    if request.name is not None:
        member.name = request.name
    if request.relation is not None:
        member.relation = request.relation
    if request.date_of_birth is not None:
        try:
            member.date_of_birth = date.fromisoformat(request.date_of_birth)
        except:
            pass
    if request.gender is not None:
        member.gender = request.gender
    if request.blood_group is not None:
        member.blood_group = request.blood_group
    if request.height is not None:
        member.height = request.height
    if request.weight is not None:
        member.weight = request.weight
    if request.allergies is not None:
        member.allergies = request.allergies
    if request.chronic_diseases is not None:
        member.chronic_diseases = request.chronic_diseases
    if request.emergency_contact is not None:
        member.emergency_contact = request.emergency_contact
    
    db.commit()
    
    return {
        "success": True,
        "message": "Family member updated"
    }

# Delete family member
@router.delete("/delete/{member_id}")
def delete_family_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(FamilyMember).filter(FamilyMember.id == member_id).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    db.delete(member)
    db.commit()
    
    return {
        "success": True,
        "message": "Family member deleted"
    }