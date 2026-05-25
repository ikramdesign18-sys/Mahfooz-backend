# app/api/reports.py
# Medical reports with search, filter, and categories

from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.report import MedicalReport
from typing import Optional
from datetime import date, datetime
import os
import shutil

router = APIRouter()

# Request models
class ReportCreate(BaseModel):
    family_member_id: int
    report_type: str  # blood_test, x_ray, mri, prescription, etc.
    title: str
    report_date: str
    hospital_name: Optional[str] = None
    doctor_name: Optional[str] = None
    category: Optional[str] = None
    folder: Optional[str] = "default"

class ReportUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    folder: Optional[str] = None
    is_favorite: Optional[bool] = None

# Add report (without file)
@router.post("/add")
def add_report(request: ReportCreate, db: Session = Depends(get_db)):
    try:
        report_date = date.fromisoformat(request.report_date)
    except:
        report_date = date.today()
    
    report = MedicalReport(
        family_member_id=request.family_member_id,
        report_type=request.report_type,
        title=request.title,
        report_date=report_date,
        hospital_name=request.hospital_name,
        doctor_name=request.doctor_name,
        category=request.category or request.report_type,
        folder=request.folder or "default"
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)
    
    return {
        "success": True,
        "message": "Report added",
        "report_id": report.id
    }

# Get all reports for a family member with search & filters
@router.get("/list/{member_id}")
def get_reports(
    member_id: int,
    search: Optional[str] = Query(None, description="Search in title, doctor, hospital"),
    report_type: Optional[str] = Query(None, description="Filter by type: blood_test, x_ray, etc."),
    category: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[str] = Query(None, description="Start date YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="End date YYYY-MM-DD"),
    favorite: Optional[bool] = Query(None, description="Show favorites only"),
    db: Session = Depends(get_db)
):
    # Start query
    query = db.query(MedicalReport).filter(
        MedicalReport.family_member_id == member_id
    )
    
    # Apply search filter (searches in title, doctor, hospital, diagnosis)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (MedicalReport.title.ilike(search_term)) |
            (MedicalReport.doctor_name.ilike(search_term)) |
            (MedicalReport.hospital_name.ilike(search_term)) |
            (MedicalReport.diagnosis.ilike(search_term)) |
            (MedicalReport.extracted_text.ilike(search_term))
        )
    
    # Filter by report type
    if report_type:
        query = query.filter(MedicalReport.report_type == report_type)
    
    # Filter by category
    if category:
        query = query.filter(MedicalReport.category == category)
    
    # Filter by date range
    if start_date:
        try:
            start = date.fromisoformat(start_date)
            query = query.filter(MedicalReport.report_date >= start)
        except:
            pass
    
    if end_date:
        try:
            end = date.fromisoformat(end_date)
            query = query.filter(MedicalReport.report_date <= end)
        except:
            pass
    
    # Filter favorites
    if favorite:
        query = query.filter(MedicalReport.is_favorite == True)
    
    # Order by date (newest first)
    reports = query.order_by(MedicalReport.report_date.desc()).all()
    
    result = []
    for report in reports:
        result.append({
            "id": report.id,
            "report_type": report.report_type,
            "title": report.title,
            "report_date": str(report.report_date),
            "hospital_name": report.hospital_name,
            "doctor_name": report.doctor_name,
            "diagnosis": report.diagnosis,
            "category": report.category,
            "folder": report.folder,
            "is_favorite": report.is_favorite,
            "has_image": bool(report.scanned_image_path),
            "has_pdf": bool(report.pdf_path)
        })
    
    return {
        "success": True,
        "reports": result,
        "total": len(result),
        "filters_applied": {
            "search": search,
            "report_type": report_type,
            "category": category,
            "start_date": start_date,
            "end_date": end_date,
            "favorite": favorite
        }
    }

# Get report categories (for tabs)
@router.get("/categories/{member_id}")
def get_categories(member_id: int, db: Session = Depends(get_db)):
    reports = db.query(MedicalReport).filter(
        MedicalReport.family_member_id == member_id
    ).all()
    
    categories = {}
    for report in reports:
        cat = report.report_type or "other"
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1
    
    # Category display names
    category_names = {
        "blood_test": "Blood Test",
        "x_ray": "X-Ray",
        "mri": "MRI",
        "ct_scan": "CT Scan",
        "ultrasound": "Ultrasound",
        "ecg": "ECG",
        "prescription": "Prescription",
        "dental": "Dental",
        "eye_test": "Eye Test",
        "other": "Other"
    }
    
    result = []
    for key, count in categories.items():
        result.append({
            "type": key,
            "name": category_names.get(key, key),
            "count": count
        })
    
    return {
        "success": True,
        "categories": result,
        "total_reports": len(reports)
    }

# Get single report details
@router.get("/report/{report_id}")
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(MedicalReport).filter(MedicalReport.id == report_id).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return {
        "id": report.id,
        "family_member_id": report.family_member_id,
        "report_type": report.report_type,
        "title": report.title,
        "report_date": str(report.report_date),
        "hospital_name": report.hospital_name,
        "doctor_name": report.doctor_name,
        "diagnosis": report.diagnosis,
        "test_values": report.test_values,
        "medicines_prescribed": report.medicines_prescribed,
        "extracted_text": report.extracted_text,
        "category": report.category,
        "folder": report.folder,
        "is_favorite": report.is_favorite,
        "original_image_path": report.original_image_path,
        "scanned_image_path": report.scanned_image_path,
        "pdf_path": report.pdf_path,
        "created_at": str(report.created_at)
    }

# Update report
@router.put("/update/{report_id}")
def update_report(report_id: int, request: ReportUpdate, db: Session = Depends(get_db)):
    report = db.query(MedicalReport).filter(MedicalReport.id == report_id).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if request.title is not None:
        report.title = request.title
    if request.category is not None:
        report.category = request.category
    if request.folder is not None:
        report.folder = request.folder
    if request.is_favorite is not None:
        report.is_favorite = request.is_favorite
    
    db.commit()
    
    return {"success": True, "message": "Report updated"}

# Delete report
@router.delete("/delete/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(MedicalReport).filter(MedicalReport.id == report_id).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Delete files if exist
    if report.original_image_path and os.path.exists(report.original_image_path):
        os.remove(report.original_image_path)
    if report.scanned_image_path and os.path.exists(report.scanned_image_path):
        os.remove(report.scanned_image_path)
    if report.pdf_path and os.path.exists(report.pdf_path):
        os.remove(report.pdf_path)
    
    db.delete(report)
    db.commit()
    
    return {"success": True, "message": "Report deleted"}