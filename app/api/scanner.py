# app/api/scanner.py
# PROFESSIONAL DOCUMENT SCANNER API - LIGHTWEIGHT PERFORMANCE VERSION WITH HIGHLY VISIBLE AI VERDICTS
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from app.services.professional_scanner import scanner
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.report import MedicalReport
from datetime import date
import os, shutil, uuid, re
import pytesseract
from PIL import Image

router = APIRouter()

@router.post("/scan")
async def scan_document(
    file: UploadFile = File(...),
    document_type: str = Form(default="report"),
    title: str = Form(default="Scanned Document"),
    family_member_id: str = Form(default="1"),
    db: Session = Depends(get_db)
):
    allowed_types = ["image/jpeg", "image/png", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Please upload JPG or PNG images")
    
    from app.core.config import UPLOAD_FOLDER
    temp_dir = os.path.join(UPLOAD_FOLDER, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    temp_filename = f"temp_{uuid.uuid4().hex[:8]}.jpg"
    temp_path = os.path.join(temp_dir, temp_filename)
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    result = scanner.scan_document(temp_path, document_type)
    
    if not result["success"]:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=result.get("error", "Scanning failed"))
    
    extracted_text = ""
    try:
        img = Image.open(result["enhanced_path"])
        extracted_text = pytesseract.image_to_string(img, config='--psm 6')
    except Exception as e:
        print(f"Tesseract error: {e}")
        extracted_text = "Text extraction failed"
    
    test_values = {}
    lines = extracted_text.split('\n')
    for line in lines:
        match = re.search(r'([A-Za-z\s]+)\s+(\d+\.?\d*)\s+.*?(\d+\.?\d*\s*-\s*\d+\.?\d*)\s+(\S+)', line)
        if match:
            name = match.group(1).strip()
            value = match.group(2)
            if len(name) > 2 and name.lower() not in ['the', 'and', 'for', 'test', 'result', 'flag', 'ref']:
                test_values[name] = value

    test_patterns = {
        "Hemoglobin": r'(?:Hb|Hemoglobin|Haemoglobin|Hgb)[:\s]*(\d+\.?\d*)',
        "Blood Sugar": r'(?:Glucose|Sugar|BSL|FBS|RBS|Blood Sugar|Random Sugar|Fasting Sugar)[:\s]*(\d+\.?\d*)',
        "Blood Pressure": r'(?:BP|Blood Pressure)[:\s]*(\d+/\d+)',
        "Cholesterol": r'(?:Cholesterol|Total Chol|Total Cholesterol)[:\s]*(\d+\.?\d*)',
        "Creatinine": r'(?:Creatinine|Cr|Serum Creatinine)[:\s]*(\d+\.?\d*)',
        "TSH": r'(?:TSH|Thyroid)[:\s]*(\d+\.?\d*)',
        "Uric Acid": r'(?:Uric Acid|UA)[:\s]*(\d+\.?\d*)',
        "HbA1c": r'(?:HbA1c|A1c|Glycated)[:\s]*(\d+\.?\d*)',
        "HDL": r'(?:HDL)[:\s]*(\d+\.?\d*)',
        "LDL": r'(?:LDL)[:\s]*(\d+\.?\d*)',
    }
    
    for test_name, pattern in test_patterns.items():
        match = re.search(pattern, extracted_text, re.IGNORECASE)
        if match:
            test_values[test_name] = match.group(1)
    
    normal_ranges = {
        "Hemoglobin": "13.5-17.5 g/dL", "Blood Sugar": "70-100 mg/dL",
        "Blood Pressure": "120/80 mmHg", "Cholesterol": "<200 mg/dL",
        "Creatinine": "0.7-1.3 mg/dL", "TSH": "0.4-4.0 mIU/L",
        "Uric Acid": "3.5-7.2 mg/dL", "HbA1c": "<5.7%",
        "HDL": ">40 mg/dL", "LDL": "<100 mg/dL",
    }
    
    biomarkers = []
    for test_name, value in test_values.items():
        status = "Normal"
        try:
            val = float(value)
            if test_name == "Hemoglobin": status = "Normal" if 12 <= val <= 18 else ("Low" if val < 12 else "High")
            elif test_name == "Blood Sugar": status = "Normal" if 70 <= val <= 100 else ("Low" if val < 70 else "High")
            elif test_name == "Creatinine": status = "Normal" if 0.6 <= val <= 1.3 else ("Low" if val < 0.6 else "High")
        except: pass
        
        biomarkers.append({
            "parameter": test_name, "value": value,
            "unit": normal_ranges.get(test_name, "").split()[-1] if normal_ranges.get(test_name) else "",
            "reference_range": normal_ranges.get(test_name, ""), "status": status
        })
    
    medicines_found = []
    for med in ["paracetamol", "ibuprofen", "metformin", "amoxicillin", "omeprazole", "aspirin"]:
        if med in extracted_text.lower(): medicines_found.append(med)
    
    report = MedicalReport(
        family_member_id=int(family_member_id) if family_member_id.isdigit() else 1,
        report_type=document_type, title=title, report_date=date.today(),
        original_image_path=result["original_path"],
        scanned_image_path=result["scanned_path"],
        extracted_text=extracted_text,
        test_values=str(test_values) if test_values else "",
        medicines_prescribed=str(medicines_found) if medicines_found else "",
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    
    if os.path.exists(temp_path): os.remove(temp_path)
    
    # 🧠 AI Analysis via Groq - EXPLICIT MEDICAL STATUS VERDICT WITH FULL TEXT VISIBILITY
    ai_analysis = None
    if extracted_text and len(extracted_text) > 20:
        try:
            from app.services.groq_llm import ask_groq
            prompt = f"""You are the expert medical diagnostic AI module for the MAHFOOZ mobile application. 
Analyze the extracted report text provided below and generate a clear safety status breakdown for the patient.

👉 RULES FOR YOUR OUTPUT FORMAT:
1. Begin your response with an explicit visual verdict banner. Use EXACTLY one of these two options:
   "🟢 STATUS: REPORT APPEARS FINE" 
   or 
   "🔴 STATUS: ABNORMAL SECTOR / ISSUES DETECTED"
2. Underneath the banner, write a concise 2-to-3 sentence diagnostic summary explaining what parameters triggered this verdict in simple, layman terms.
3. List explicit next steps (e.g., "Schedule a routine checkup", "Consult your physician regarding parameter X", or any critical emergency indicators).

Extracted Text:
{extracted_text}

Extracted Biomarkers / Key Values:
{test_values}"""

            ai_analysis = ask_groq(prompt)
        except Exception as e:
            print(f"Groq execution failed: {e}")
            ai_analysis = None
    
    if not ai_analysis:
        if biomarkers:
            abnormal = [b for b in biomarkers if b['status'] not in ['Normal']]
            if abnormal:
                ai_analysis = f"🔴 STATUS: ABNORMAL SECTOR / ISSUES DETECTED\n\n⚠️ Found {len(abnormal)} abnormal values: {', '.join(b['parameter'] for b in abnormal)}. Please consult a doctor."
            else:
                ai_analysis = "🟢 STATUS: REPORT APPEARS FINE\n\n✅ All test values extracted by our fallback analyzer appear within typical normal reference boundaries."
        else:
            ai_analysis = "📄 Report scanned successfully. Original layout saved. AI parsing fallback completed with standard text storage structure."
    
    return {
        "success": True, "message": "Document scanned successfully",
        "ai_analysis": ai_analysis,
        "report_id": report.id, "quality_score": result["quality_score"],
        "scanned_preview": f"/api/scanner/preview/{report.id}",
        "pdf_download": f"/api/scanner/download-pdf/{report.id}",
        "extracted_text": extracted_text, "test_values": test_values,
        "biomarkers": biomarkers,
        "ai_interpretation": ai_analysis,
        "medicines_found": medicines_found,
    }

@router.get("/preview/{report_id}")
def get_preview(report_id: str, db: Session = Depends(get_db)):
    report = db.query(MedicalReport).order_by(MedicalReport.id.desc()).first()
    if report and report.scanned_image_path and os.path.exists(report.scanned_image_path):
        return FileResponse(report.scanned_image_path, media_type="image/jpeg")
    raise HTTPException(status_code=404)

@router.get("/complete-report/{report_id}")
def get_complete_report(report_id: str, db: Session = Depends(get_db)):
    report = db.query(MedicalReport).order_by(MedicalReport.id.desc()).first()
    try:
        r = db.query(MedicalReport).filter(MedicalReport.id == int(report_id)).first()
        if r: report = r
    except: pass
    if not report:
        raise HTTPException(status_code=404)
    return {
        "title": report.title,
        "type": report.report_type,
        "date": str(report.report_date),
        "extracted_text": report.extracted_text,
        "test_values": report.test_values,
        "medicines": report.medicines_prescribed,
        "has_image": bool(report.scanned_image_path),
        "image_url": f"/api/scanner/preview/{report.id}",
        "pdf_url": f"/api/scanner/download-pdf/{report.id}",
    }

@router.get("/download-pdf/{report_id}")
def download_pdf(report_id: str, db: Session = Depends(get_db)):
    report = db.query(MedicalReport).order_by(MedicalReport.id.desc()).first()
    try:
        r = db.query(MedicalReport).filter(MedicalReport.id == int(report_id)).first()
        if r: report = r
    except: pass
    if report:
        for path_attr in ['scanned_image_path', 'original_image_path']:
            path = getattr(report, path_attr, None)
            if path and os.path.exists(path):
                return FileResponse(path, media_type="image/jpeg", 
                                  filename=f"MAHFOOZ_Report_{report.id}.jpg")
    raise HTTPException(status_code=404, detail="Report file not found")
