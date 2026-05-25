# app/models/pregnancy.py
# PREGNANCY TRACKING SYSTEM

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, ForeignKey
from app.core.database import Base
from datetime import datetime

class PregnancyTracker(Base):
    __tablename__ = "pregnancy_tracker"
    
    id = Column(Integer, primary_key=True, index=True)
    family_member_id = Column(Integer, ForeignKey("family_members.id"))
    
    # Pregnancy details
    start_date = Column(Date)  # LMP or conception date
    due_date = Column(Date)
    current_week = Column(Integer)
    pregnancy_number = Column(Integer, default=1)  # 1st, 2nd pregnancy
    
    # Health metrics
    pre_pregnancy_weight = Column(Float)
    current_weight = Column(Float)
    blood_group = Column(String(5))
    rh_factor = Column(String(5))  # Positive/Negative
    
    # Risk factors
    is_high_risk = Column(Boolean, default=False)
    risk_factors = Column(Text)
    
    # Appointments
    next_appointment = Column(Date)
    doctor_name = Column(String(200))
    hospital_name = Column(String(200))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PregnancyWeek(Base):
    __tablename__ = "pregnancy_weeks"
    
    id = Column(Integer, primary_key=True)
    week_number = Column(Integer, unique=True)
    trimester = Column(Integer)  # 1, 2, or 3
    
    # Baby development
    baby_size = Column(String(100))  # "Size of a poppy seed"
    baby_weight = Column(String(50))  # "1 gram"
    baby_length = Column(String(50))  # "2 mm"
    development_milestone = Column(Text)
    
    # Mother changes
    mother_symptoms = Column(Text)
    mother_body_changes = Column(Text)
    
    # What to do this week
    tasks = Column(Text)
    tests_this_week = Column(Text)
    nutrition_tips = Column(Text)
    exercise_tips = Column(Text)
    
    # Warnings
    warning_signs = Column(Text)
    when_to_call_doctor = Column(Text)

class PregnancySymptom(Base):
    __tablename__ = "pregnancy_symptoms"
    
    id = Column(Integer, primary_key=True)
    tracker_id = Column(Integer, ForeignKey("pregnancy_tracker.id"))
    week = Column(Integer)
    symptom = Column(String(200))
    severity = Column(String(20))  # Mild, Moderate, Severe
    notes = Column(Text)
    recorded_at = Column(DateTime, default=datetime.utcnow)

class PregnancyAppointment(Base):
    __tablename__ = "pregnancy_appointments"
    
    id = Column(Integer, primary_key=True)
    tracker_id = Column(Integer, ForeignKey("pregnancy_tracker.id"))
    appointment_date = Column(Date)
    appointment_type = Column(String(100))  # Ultrasound, Checkup, Blood test
    doctor_name = Column(String(200))
    hospital = Column(String(200))
    findings = Column(Text)
    next_appointment = Column(Date)
    completed = Column(Boolean, default=False)