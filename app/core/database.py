# app/core/database.py
# Independent database connection loader

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Completely independent fallback mechanism (ignores config.py completely)
FINAL_DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./medical_wallet_local.db")

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
