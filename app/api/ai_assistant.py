# app/api/ai_assistant.py
# WORLD-CLASS MEDICAL AI CHAT - 100% FREE WITH EXTENDED REPORT EXTRACTION

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.report import MedicalReport
from app.services.ai_chat_engine import MedicalChatAI
from app.services.smart_ai import smart_ai
from typing import Optional

router = APIRouter()

# Initialize the AI Chat Engine
ai = MedicalChatAI()

class ChatRequest(BaseModel):
    message: str

class ReportQuery(BaseModel):
    report_id: int
    question: Optional[str] = None

# ==========================================
# 🧠 MAIN CHAT ENDPOINTS
# ==========================================

@router.post("/chat")
def chat_with_ai(request: ChatRequest):
    """
    Chat naturally with MAHFOOZ AI about ANY medical question
    Ask about medicines, symptoms, diet, reports - anything!
    """
    response = ai.chat(request.message)
    return {
        "success": True,
        "your_message": request.message,
        "ai_response": response,
        "note": "⚠️ I provide information only. Always consult a doctor for medical advice."
    }

@router.post("/smart-chat")
def smart_chat(request: ChatRequest):
    """Smart AI that understands any question"""
    response = smart_ai.answer(request.message)
    return {
        "success": True,
        "your_message": request.message,
        "ai_response": response,
        "note": "⚠️ I provide information only. Always consult a doctor."
    }

@router.post("/chat/report")
def chat_about_report(query: ReportQuery, db: Session = Depends(get_db)):
    """Chat about a specific medical report - FULL VISIBILITY FOR GROQ/AI CLARITY"""
    report = db.query(MedicalReport).filter(MedicalReport.id == query.report_id).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report_text = f"Report Title: {report.title}. Type: {report.report_type}."
    if hasattr(report, 'diagnosis') and report.diagnosis:
        report_text += f" Diagnosis: {report.diagnosis}."
        
    # FIX: Removed the [:500] limit so Groq/AI can evaluate the entire scanned laboratory file content
    if report.extracted_text:
        report_text += f" Complete Extracted Details: {report.extracted_text}"
    if hasattr(report, 'test_values') and report.test_values:
        report_text += f" Parsed Test Key Values: {report.test_values}"
    
    question = query.question or "Explain this report to me in simple language, highlight warnings, and verify if values are okay."
    
    full_message = f"""You are the expert medical assistant for the MAHFOOZ ecosystem. 
Review the following complete digital lab extraction:
---
{report_text}
---
Patient Question: {question}

Provide a reassuring, highly detailed response translating medical jargon into clean, plain English."""
    
    response = ai.chat(full_message)
    
    return {
        "success": True,
        "report_title": report.title,
        "your_question": query.question,
        "ai_response": response,
        "note": "⚠️ I provide information only. Always consult a doctor for medical advice."
    }

# ==========================================
# KEEP OLD ENDPOINTS FOR COMPATIBILITY
# ==========================================

@router.post("/explain-report")
def explain_report(query: ReportQuery, db: Session = Depends(get_db)):
    """Explain a medical report in simple language"""
    report = db.query(MedicalReport).filter(MedicalReport.id == query.report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    text = f"Explain this {report.report_type} report titled '{report.title}'"
    if hasattr(report, 'diagnosis') and report.diagnosis:
        text += f" with diagnosis: {report.diagnosis}"
    if report.extracted_text:
        text += f" Here is the document text data: {report.extracted_text}"
    if query.question:
        text += f". Also answer: {query.question}"
    
    response = ai.chat(text)
    return {"success": True, "ai_response": response}

@router.post("/explain-text")
def explain_text(request: ChatRequest):
    """Explain any medical text"""
    response = ai.chat(f"Explain this in simple language: {request.message}")
    return {"success": True, "ai_response": response}

@router.get("/search-term/{term}")
def search_term(term: str):
    """Search for any medical term"""
    response = ai.chat(f"Tell me everything about {term}")
    return {"success": True, "term": term, "ai_response": response}

@router.get("/categories")
def get_categories():
    """Get all medical categories"""
    return {
        "success": True,
        "categories": [
            "Blood Test", "Lipid Profile", "Liver Test", "Kidney Test",
            "Thyroid Test", "Vitamin Test", "Heart Test", "Imaging",
            "Disease", "Symptom", "Emergency", "Prevention",
            "Women's Health", "Children's Health", "Medication", "Infectious Disease"
        ]
    }

@router.get("/health-tips")
def get_health_tips():
    """Get daily health tips"""
    response = ai.chat("Give me 5 practical daily personal health or hygiene tips.")
    return {"success": True, "tips": response}

@router.get("/emergency")
def get_emergency_info(country: str = "pakistan"):
    """Get emergency numbers"""
    return {
        "success": True,
        "country": country,
        "pakistan": {"ambulance": "1122", "police": "15", "fire": "16"},
        "india": {"ambulance": "108", "police": "100", "fire": "101"}
    }

@router.get("/search")
def search_all(query: str = Query(...)):
    """Search across all medical knowledge"""
    response = ai.chat(f"Tell me about {query}")
    return {"success": True, "query": query, "ai_response": response}
