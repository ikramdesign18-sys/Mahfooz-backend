# app/models/report.py
# This creates the MEDICAL REPORTS table in database

from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, ForeignKey
from app.core.database import Base
from datetime import datetime

class MedicalReport(Base):
    __tablename__ = "medical_reports"

    id = Column(Integer, primary_key=True, index=True)
    family_member_id = Column(Integer, ForeignKey("family_members.id"))
    report_type = Column(String)
    title = Column(String)
    report_date = Column(Date)
    hospital_name = Column(String, default="")
    doctor_name = Column(String, default="")
    
    original_image_path = Column(String, default="")
    scanned_image_path = Column(String, default="")
    pdf_path = Column(String, default="")
    
    extracted_text = Column(Text, default="")
    diagnosis = Column(String, default="")
    test_values = Column(Text, default="")
    medicines_prescribed = Column(Text, default="")
    
    category = Column(String, default="")
    folder = Column(String, default="default")
    is_favorite = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)