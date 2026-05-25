# app/models/family.py
# This creates the FAMILY MEMBERS table in database

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from app.core.database import Base
from datetime import datetime

class FamilyMember(Base):
    __tablename__ = "family_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    relation = Column(String)  # father, mother, son, daughter, etc.
    date_of_birth = Column(Date, default=None)
    gender = Column(String, default="")
    blood_group = Column(String, default="")
    height = Column(String, default="")
    weight = Column(String, default="")
    allergies = Column(String, default="")
    chronic_diseases = Column(String, default="")
    emergency_contact = Column(String, default="")
    profile_image = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)