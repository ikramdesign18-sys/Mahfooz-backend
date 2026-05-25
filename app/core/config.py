# app/core/config.py
# This file stores all settings safely across Mac and Render environments

import os
import tempfile

# App Settings
APP_NAME = "MAHFOOZ Family Medical Wallet"
APP_VERSION = "1.0.0"

# Dynamic Environment Routing
if os.environ.get("RENDER"):
    base_dir = tempfile.gettempdir()
    # Correct format for Linux absolute file generation paths
    DATABASE_URL = f"sqlite:///{os.path.join(base_dir, 'mahfooz.db')}"
    UPLOAD_FOLDER = os.path.join(base_dir, "uploads")
else:
    # Safe local relative path layout for your Mac
    DATABASE_URL = "sqlite:///./mahfooz.db"
    UPLOAD_FOLDER = "uploads"

# OTP Settings (for phone login)
OTP_EXPIRE_MINUTES = 5

# Secret Key for Security
SECRET_KEY = os.environ.get("SECRET_KEY", "mahfooz-secret-key-change-this-later")

# Safely create upload folders inside the permitted directory path
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, "reports"), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, "profiles"), exist_ok=True)
