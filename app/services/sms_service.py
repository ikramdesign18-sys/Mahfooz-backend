# app/services/sms_service.py
# FREE SMS OTP (Local Test Mode - Firebase Removed)

import random
import os
from datetime import datetime, timedelta

print("Firebase not configured - using test mode")

class SMSService:
    def __init__(self):
        self.otp_store = {}
        self.use_firebase = False
    
    def send_otp(self, phone_number):
        """Send OTP via local fallback system (No Firebase needed)"""
        
        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        
        # FALLBACK: Store OTP (for testing/development)
        self.otp_store[phone_number] = {
            "otp": otp,
            "expires_at": datetime.utcnow() + timedelta(minutes=5)
        }
        
        # In development: print OTP, show in app
        print(f"\n📱 OTP for {phone_number}: {otp}\n")
        
        return {
            "success": True,
            "message": "OTP sent",
            "otp": otp,  
            "expires_in": "5 minutes",
            "note": "Running in test mode without Firebase"
        }
    
    def verify_otp(self, phone_number, otp):
        """Verify OTP"""
        if phone_number not in self.otp_store:
            return False, "No OTP sent"
        
        stored = self.otp_store[phone_number]
        
        if datetime.utcnow() > stored["expires_at"]:
            del self.otp_store[phone_number]
            return False, "OTP expired"
        
        if stored["otp"] != otp:
            return False, "Wrong OTP"
        
        del self.otp_store[phone_number]
        return True, "Verified"
