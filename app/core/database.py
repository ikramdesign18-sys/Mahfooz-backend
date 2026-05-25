# app/core/database.py
# This file connects to database safely on Mac and Render

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. First attempt: Look for a database variable directly in Render's dashboard environment
# 2. Second attempt: Fallback to whatever your config file states
# 3. Final fallback: Create a local SQLite file so the app never crashes on boot
try:
    from app.core.config import DATABASE_URL
except ImportError:
    DATABASE_URL = None

FINAL_DATABASE_URL = os.environ.get("DATABASE_URL") or DATABASE_URL or "sqlite:///./medical_wallet_local.db"

# Dynamically adjust connection flags based on the database type
if FINAL_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(FINAL_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(FINAL_DATABASE_URL)

# Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for models
Base = declarative_base()

# Function to get database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
