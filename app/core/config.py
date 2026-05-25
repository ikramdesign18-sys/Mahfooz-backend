# app/core/config.py
import os
import tempfile

APP_NAME = "MAHFOOZ Family Medical Wallet"
APP_VERSION = "1.0.0"

# FORCE SQLite to write to a safe, cloud-permitted folder path
if os.environ.get("RENDER"):
    base_dir = tempfile.gettempdir()
    DATABASE_URL = f"sqlite:///{os.path.join(base_dir, 'mahfooz.db')}"
    UPLOAD_FOLDER = os.path.join(base_dir, "uploads")
else:
    DATABASE_URL = "sqlite:///./mahfooz.db"
    UPLOAD_FOLDER = "uploads"

OTP_EXPIRE_MINUTES = 5
SECRET_KEY = "mahfooz-secret-key-change-this-later"

# Create folders safely
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, "reports"), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, "profiles"), exist_ok=True)
