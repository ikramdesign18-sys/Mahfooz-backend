# app/models/doctor_note.py
# This creates the DOCTOR NOTES table in database

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from app.core.database import Base
from datetime import datetime

class DoctorNote(Base):
    __tablename__ = "doctor_notes"

    id = Column(Integer, primary_key=True, index=True)
    family_member_id = Column(Integer, ForeignKey("family_members.id"))
    doctor_name = Column(String)
    hospital_name = Column(String, default="")
    visit_date = Column(Date)
    reason = Column(String)
    diagnosis = Column(Text, default="")
    notes = Column(Text, default="")
    prescription = Column(Text, default="")
    next_visit_date = Column(Date, default=None)
    attachments = Column(String, default="")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)