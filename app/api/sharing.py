# app/api/sharing.py
# Share reports via links, PDF generation, QR codes

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.report import MedicalReport
from app.models.doctor_note import DoctorNote
from datetime import datetime
import os
import uuid
import json

router = APIRouter()

# Store shared links temporarily
shared_links = {}

# Generate shareable link for a report
@router.get("/generate-link/{report_id}")
def generate_share_link(
    report_id: int,
    expiry_hours: int = 24,
    db: Session = Depends(get_db)
):
    report = db.query(MedicalReport).filter(MedicalReport.id == report_id).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Generate unique share ID
    share_id = str(uuid.uuid4())[:8]
    
    # Store link data
    shared_links[share_id] = {
        "report_id": report_id,
        "created_at": datetime.utcnow(),
        "expires_in": expiry_hours,
        "accessed": 0
    }
    
    share_url = f"https://mahfooz.app/share/{share_id}"
    
    return {
        "success": True,
        "share_id": share_id,
        "share_url": share_url,
        "expires_in": f"{expiry_hours} hours",
        "report_title": report.title
    }

# View shared report via link
@router.get("/view/{share_id}")
def view_shared_report(share_id: str, db: Session = Depends(get_db)):
    if share_id not in shared_links:
        raise HTTPException(status_code=404, detail="Link expired or invalid")
    
    link_data = shared_links[share_id]
    
    # Check expiry
    hours_passed = (datetime.utcnow() - link_data["created_at"]).total_seconds() / 3600
    if hours_passed > link_data["expires_in"]:
        del shared_links[share_id]
        raise HTTPException(status_code=410, detail="Link expired")
    
    # Get report
    report = db.query(MedicalReport).filter(
        MedicalReport.id == link_data["report_id"]
    ).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Track access
    shared_links[share_id]["accessed"] += 1
    
    return {
        "success": True,
        "report": {
            "id": report.id,
            "title": report.title,
            "report_type": report.report_type,
            "report_date": str(report.report_date),
            "hospital_name": report.hospital_name,
            "doctor_name": report.doctor_name,
            "diagnosis": report.diagnosis,
            "test_values": report.test_values,
            "medicines_prescribed": report.medicines_prescribed,
            "extracted_text": report.extracted_text
        },
        "shared_via": "MAHFOOZ Secure Link",
        "accessed_count": shared_links[share_id]["accessed"]
    }

# Download report as PDF (simple version)
@router.get("/download-pdf/{report_id}")
def download_report_pdf(report_id: int, db: Session = Depends(get_db)):
    report = db.query(MedicalReport).filter(MedicalReport.id == report_id).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # If PDF already exists, return it
    if report.pdf_path and os.path.exists(report.pdf_path):
        return FileResponse(
            report.pdf_path,
            media_type="application/pdf",
            filename=f"report_{report.id}.pdf"
        )
    
    # If original image exists, return it
    if report.original_image_path and os.path.exists(report.original_image_path):
        return FileResponse(
            report.original_image_path,
            filename=f"report_{report.id}.jpg"
        )
    
    raise HTTPException(status_code=404, detail="No file available for download")

# Share report data as JSON for WhatsApp/Email
@router.get("/share-data/{report_id}")
def share_report_data(report_id: int, db: Session = Depends(get_db)):
    report = db.query(MedicalReport).filter(MedicalReport.id == report_id).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Create shareable text
    share_text = f"""
📄 *Medical Report*
━━━━━━━━━━━━━━━━━
📋 *Title:* {report.title}
📅 *Date:* {report.report_date}
🏥 *Hospital:* {report.hospital_name or 'N/A'}
👨‍⚕️ *Doctor:* {report.doctor_name or 'N/A'}
📂 *Type:* {report.report_type}

🔬 *Diagnosis:* {report.diagnosis or 'Not specified'}

💊 *Medicines:* {report.medicines_prescribed or 'None'}

━━━━━━━━━━━━━━━━━
Shared via *MAHFOOZ* - Family Medical Wallet
"""
    
    return {
        "success": True,
        "share_text": share_text,
        "whatsapp_url": f"https://wa.me/?text={share_text}",
        "report_data": {
            "title": report.title,
            "date": str(report.report_date),
            "hospital": report.hospital_name,
            "doctor": report.doctor_name,
            "diagnosis": report.diagnosis,
            "medicines": report.medicines_prescribed
        }
    }

# Share doctor note
@router.get("/share-note/{note_id}")
def share_note_data(note_id: int, db: Session = Depends(get_db)):
    note = db.query(DoctorNote).filter(DoctorNote.id == note_id).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    share_text = f"""
🏥 *Doctor Visit Note*
━━━━━━━━━━━━━━━━━
👨‍⚕️ *Doctor:* {note.doctor_name}
🏥 *Hospital:* {note.hospital_name or 'N/A'}
📅 *Date:* {note.visit_date}

📋 *Reason:* {note.reason}

🔬 *Diagnosis:* {note.diagnosis or 'Not specified'}

📝 *Notes:* {note.notes or 'None'}

💊 *Prescription:* {note.prescription or 'None'}

📅 *Next Visit:* {note.next_visit_date or 'Not scheduled'}

━━━━━━━━━━━━━━━━━
Shared via *MAHFOOZ* - Family Medical Wallet
"""
    
    return {
        "success": True,
        "share_text": share_text,
        "whatsapp_url": f"https://wa.me/?text={share_text}"
    }

# Generate QR code data for report
@router.get("/qr-data/{report_id}")
def generate_qr_data(report_id: int, db: Session = Depends(get_db)):
    report = db.query(MedicalReport).filter(MedicalReport.id == report_id).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Generate share link first
    share_id = str(uuid.uuid4())[:8]
    shared_links[share_id] = {
        "report_id": report_id,
        "created_at": datetime.utcnow(),
        "expires_in": 48,
        "accessed": 0
    }
    
    qr_data = {
        "type": "medical_report",
        "app": "MAHFOOZ",
        "share_id": share_id,
        "view_url": f"https://mahfooz.app/share/{share_id}",
        "report_title": report.title,
        "patient_name": "Confidential",
        "date": str(report.report_date)
    }
    
    return {
        "success": True,
        "qr_data": json.dumps(qr_data),
        "share_url": qr_data["view_url"]
    }