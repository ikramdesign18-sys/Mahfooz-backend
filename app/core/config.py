# app/core/config.py
# This file stores all settings for your app

import os

# App Settings
APP_NAME = "MAHFOOZ Family Medical Wallet"
APP_VERSION = "1.0.0"

# Database Settings (we'll use SQLite - no setup needed!)
DATABASE_URL = "sqlite:///./mahfooz.db"

# Upload Folder for Scanned Reports
UPLOAD_FOLDER = "uploads"

# OTP Settings (for phone login)
OTP_EXPIRE_MINUTES = 5

# Secret Key for Security
SECRET_KEY = "mahfooz-secret-key-change-this-later"

# Create upload folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(f"{UPLOAD_FOLDER}/reports", exist_ok=True)
os.makedirs(f"{UPLOAD_FOLDER}/profiles", exist_ok=True)