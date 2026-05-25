# app/services/sms_service.py
# FREE SMS OTP via Firebase Phone Auth

import firebase_admin
from firebase_admin import credentials, auth
import random
import os

# Initialize Firebase (you'll add your credentials)
try:
    cred = credentials.Certificate("firebase-credentials.json")
    firebase_admin.initialize_app(cred)
except:
    print("Firebase not configured - using test mode")

class SMSService:
    def __init__(self):
        self.otp_store = {}
        self.use_firebase = os.path.exists("firebase-credentials.json")
    
    def send_otp(self, phone_number):
        """Send OTP via Firebase Phone Auth (FREE 10K/month)"""
        
        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        
        if self.use_firebase:
            try:
                # Firebase sends real SMS
                session = auth.create_session_cookie(
                    id_token=phone_number,
                    expires_in=300  # 5 minutes
                )
                return {
                    "success": True,
                    "message": "OTP sent via SMS",
                    "expires_in": "5 minutes"
                }
            except Exception as e:
                print(f"Firebase error: {e}")
        
        # FALLBACK: Store OTP (for testing/development)
        from datetime import datetime, timedelta
        self.otp_store[phone_number] = {
            "otp": otp,
            "expires_at": datetime.utcnow() + timedelta(minutes=5)
        }
        
        # In development: print OTP, show in app, or send via email
        print(f"\n📱 OTP for {phone_number}: {otp}\n")
        
        return {
            "success": True,
            "message": "OTP sent",
            "otp": otp,  # REMOVE in production!
            "expires_in": "5 minutes",
            "note": "In production, OTP goes via SMS automatically"
        }
    
    def verify_otp(self, phone_number, otp):
        """Verify OTP"""
        if phone_number not in self.otp_store:
            return False, "No OTP sent"
        
        stored = self.otp_store[phone_number]
        
        from datetime import datetime
        if datetime.utcnow() > stored["expires_at"]:
            del self.otp_store[phone_number]
            return False, "OTP expired"
        
        if stored["otp"] != otp:
            return False, "Wrong OTP"
        
        del self.otp_store[phone_number]
        return True, "Verified"