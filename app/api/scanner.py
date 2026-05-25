# app/api/scanner.py
# PROFESSIONAL DOCUMENT SCANNER API
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
import easyocr

router = APIRouter()
try:
    reader = easyocr.Reader(['en'], gpu=False)
except:
    reader = None

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
    
    temp_filename = f"temp_{uuid.uuid4().hex[:8]}.jpg"
    temp_path = f"uploads/temp/{temp_filename}"
    os.makedirs("uploads/temp", exist_ok=True)
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    result = scanner.scan_document(temp_path, document_type)
    
    if not result["success"]:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=result.get("error", "Scanning failed"))
    
    # Extract text using PaddleOCR (BEST free OCR)
    extracted_text = ""
    try:
        from paddleocr import PaddleOCR
        paddle_ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
        ocr_result = paddle_ocr.ocr(result["enhanced_path"], cls=True)
        if ocr_result and ocr_result[0]:
            lines = []
            for line in ocr_result[0]:
                text = line[1][0]
                confidence = line[1][1]
                if confidence > 0.5:
                    lines.append(text)
            extracted_text = '\n'.join(lines)
    except Exception as e:
        print(f"PaddleOCR error: {e}")
        # Fallback to EasyOCR
        try:
            if reader:
                ocr_results = reader.readtext(result["enhanced_path"])
                extracted_text = ' '.join([r[1] for r in ocr_results if r[2] > 0.3])
        except:
            pass
    
    # Fallback to Tesseract
    if not extracted_text:
        try:
            img = Image.open(result["enhanced_path"])
            extracted_text = pytesseract.image_to_string(img, config='--psm 6')
        except:
            extracted_text = "Text extraction failed"
    
    # Extract test values - try table format first
    test_values = {}
    
    # Parse table format: lines with numbers in columns
    lines = extracted_text.split('\n')
    for line in lines:
        # Look for patterns like: "HbA1c    5    4.0-6.0    %"
        # Match: text then number then number-range then unit
        match = re.search(r'([A-Za-z\s]+)\s+(\d+\.?\d*)\s+.*?(\d+\.?\d*\s*-\s*\d+\.?\d*)\s+(\S+)', line)
        if match:
            name = match.group(1).strip()
            value = match.group(2)
            ref_range = match.group(3)
            unit = match.group(4)
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
    
    # Build biomarkers
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
    
    # Find medicines
    medicines_found = []
    for med in ["paracetamol", "ibuprofen", "metformin", "amoxicillin", "omeprazole", "aspirin"]:
        if med in extracted_text.lower(): medicines_found.append(med)
    
    # Save to database
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
    
    # AI Analysis via Groq
    ai_analysis = None
    if extracted_text and len(extracted_text) > 50:
        try:
            from app.services.groq_llm import ask_groq
            prompt = f"""Analyze this medical report and tell the patient:
1. Is this report normal or abnormal?
2. What are the key findings in simple language?
3. What should they do next?
4. Any emergency warnings?

Report text: {extracted_text[:500]}
Test values found: {test_values}"""

            ai_analysis = ask_groq(prompt)
        except:
            ai_analysis = None
    
    if not ai_analysis:
        if biomarkers:
            abnormal = [b for b in biomarkers if b['status'] not in ['Normal']]
            if abnormal:
                ai_analysis = f"⚠️ Found {len(abnormal)} abnormal values: {', '.join(b['parameter'] for b in abnormal)}. Please consult a doctor."
            else:
                ai_analysis = "✅ All test values appear normal. Keep up the good health!"
        else:
            ai_analysis = "📄 Report scanned. Original document saved. AI could not extract biomarkers from this image."
    
    return {
        "success": True, "message": "Document scanned successfully",
        "ai_analysis": ai_analysis,
        "report_id": report.id, "quality_score": result["quality_score"],
        "scanned_preview": f"/api/scanner/preview/{report.id}",
        "pdf_download": f"/api/scanner/download-pdf/{report.id}",
        "extracted_text": extracted_text, "test_values": test_values,
        "biomarkers": biomarkers,
        "ai_analysis": ai_analysis,
        "ai_interpretation": f"Found {len(biomarkers)} biomarkers. {len(medicines_found)} medicines detected." if biomarkers or medicines_found else "No biomarkers detected. Try a clearer image.",
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
    """Get complete report data for sharing"""
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
        "diagnosis": report.diagnosis,
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
        # Try enhanced first, then scanned, then original
        for path_attr in ['scanned_image_path', 'original_image_path']:
            path = getattr(report, path_attr, None)
            if path and os.path.exists(path):
                return FileResponse(path, media_type="image/jpeg", 
                                  filename=f"MAHFOOZ_Report_{report.id}.jpg",
                                  headers={"Content-Disposition": f"attachment; filename=MAHFOOZ_Report_{report.id}.jpg"})
    raise HTTPException(status_code=404, detail="Report file not found")
