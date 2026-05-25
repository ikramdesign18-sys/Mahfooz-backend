# main.py
# MAHFOOZ Family Medical Wallet - Main Server File

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.models import user, family, medicine, report, doctor_note

# Import all API routes
from app.api import auth, family, medicines, reports, doctor_notes, scanner, ai_assistant, sharing, pregnancy

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="MAHFOOZ Family Medical Wallet",
    description="Complete backend for family health management",
    version="1.0.0"
)

# Allow connections from mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routes
app.include_router(auth.router, prefix="/api/auth", tags=["🔐 Authentication"])
app.include_router(family.router, prefix="/api/family", tags=["👨‍👩‍👧‍👦 Family"])
app.include_router(medicines.router, prefix="/api/medicines", tags=["💊 Medicines"])
app.include_router(reports.router, prefix="/api/reports", tags=["📄 Reports"])
app.include_router(doctor_notes.router, prefix="/api/doctor-notes", tags=["🏥 Doctor Notes"])
app.include_router(scanner.router, prefix="/api/scanner", tags=["📷 Scanner"])
app.include_router(ai_assistant.router, prefix="/api/ai", tags=["🤖 AI Assistant"])
app.include_router(sharing.router, prefix="/api/share", tags=["🔗 Sharing"])
app.include_router(pregnancy.router, prefix="/api/pregnancy", tags=["🤰 Pregnancy"])

# Home page
@app.get("/")
def home():
    return {
        "app": "MAHFOOZ Family Medical Wallet",
        "version": "1.0.0",
        "status": "✅ Server is running",
        "api_docs": "http://127.0.0.1:8000/docs",
        "endpoints": {
            "auth": "/api/auth",
            "family": "/api/family",
            "medicines": "/api/medicines",
            "reports": "/api/reports",
            "doctor_notes": "/api/doctor-notes",
            "scanner": "/api/scanner",
            "ai_assistant": "/api/ai",
            "sharing": "/api/share"
        }
    }

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}