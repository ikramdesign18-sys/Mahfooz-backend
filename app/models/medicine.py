# app/models/medicine.py
# This creates the MEDICINES table in database

from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from app.core.database import Base
from datetime import datetime

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    family_member_id = Column(Integer, ForeignKey("family_members.id"))
    medicine_name = Column(String)
    dosage = Column(String)
    frequency = Column(String)  # once_daily, twice_daily
    timing = Column(String)  # "08:00, 20:00"
    start_date = Column(Date)
    end_date = Column(Date, default=None)
    reminder_enabled = Column(Boolean, default=True)
    notes = Column(String, default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class MedicineReminder(Base):
    __tablename__ = "medicine_reminders"

    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id"))
    reminder_time = Column(String)
    is_taken = Column(Boolean, default=False)
    taken_at = Column(DateTime, default=None)
    reminder_date = Column(Date)