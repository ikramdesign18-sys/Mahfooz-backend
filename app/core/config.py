# app/core/config.py
# This file stores all settings for your app safely on Mac and Render

import os
import tempfile

# App Settings
APP_NAME = "MAHFOOZ Family Medical Wallet"
APP_VERSION = "1.0.0"

# Database Settings (we'll use SQLite - no setup needed!)
DATABASE_URL = "sqlite:///./mahfooz.db"

# Dynamic Upload Folder: Uses a temporary directory on Render to bypass permission blocks
if os.environ.get("RENDER"):
    UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "uploads")
else:
    UPLOAD_FOLDER = "uploads"

# OTP Settings (for phone login)
OTP_EXPIRE_MINUTES = 5

# Secret Key for Security
SECRET_KEY = os.environ.get("SECRET_KEY", "mahfooz-secret-key-change-this-later")

# Safely create upload folders inside the permitted directory path
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, "reports"), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, "profiles"), exist_ok=True)
