# app/models/medical_reference.py
# COMPLETE LOCAL MEDICAL REFERENCE SYSTEM
# Based on: LOINC, RxNorm, OpenFDA, RadGraph

from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# ==========================================
# 1. LOCAL DRUG DICTIONARY (RxNorm + OpenFDA)
# ==========================================
class DrugDictionary(Base):
    __tablename__ = "drug_dictionary"
    
    id = Column(Integer, primary_key=True)
    brand_name = Column(String(200), index=True)  # Panadol, Advil, etc.
    generic_name = Column(String(200), index=True)  # Paracetamol, Ibuprofen
    rxnorm_id = Column(String(20), unique=True)  # RxNorm standard ID
    chemical_formula = Column(String(100))
    
    # Regional brand mappings
    pakistan_brand = Column(String(200))  # Local Pakistani name
    india_brand = Column(String(200))  # Local Indian name
    uk_brand = Column(String(200))
    us_brand = Column(String(200))
    
    # Standard Dosages
    adult_dose_min = Column(Float)
    adult_dose_max = Column(Float)
    adult_dose_unit = Column(String(20))
    adult_frequency = Column(String(100))
    child_dose = Column(Text)
    elderly_dose = Column(Text)
    
    # Safety
    pregnancy_category = Column(String(5))  # A, B, C, D, X
    breastfeeding = Column(String(50))
    black_box_warning = Column(Text)  # FDA most serious warning
    contraindications = Column(Text)
    
    # Side Effects by frequency
    common_side_effects = Column(Text)
    rare_side_effects = Column(Text)
    serious_side_effects = Column(Text)
    
    # Overdose
    overdose_symptoms = Column(Text)
    overdose_treatment = Column(Text)
    antidote = Column(String(200))
    
    # Drug class
    drug_class = Column(String(100))
    mechanism_of_action = Column(Text)
    
    # Source
    fda_application = Column(String(50))
    source = Column(String(50))  # OpenFDA, RxNorm

# ==========================================
# 2. LAB TEST REFERENCE (LOINC Standards)
# ==========================================
class LabReference(Base):
    __tablename__ = "lab_reference"
    
    id = Column(Integer, primary_key=True)
    loinc_code = Column(String(20), unique=True, index=True)  # LOINC standard
    test_name = Column(String(200), index=True)
    short_name = Column(String(50))  # Hb, Cr, etc.
    
    # Specimen
    specimen_type = Column(String(50))  # Blood, Urine, etc.
    collection_method = Column(Text)
    
    # Reference Ranges (by population)
    normal_low = Column(Float)
    normal_high = Column(Float)
    unit = Column(String(20))
    
    male_low = Column(Float)
    male_high = Column(Float)
    female_low = Column(Float)
    female_high = Column(Float)
    
    pediatric_low = Column(Float)
    pediatric_high = Column(Float)
    pediatric_age_range = Column(String(50))
    
    elderly_low = Column(Float)
    elderly_high = Column(Float)
    
    pregnancy_low = Column(Float)
    pregnancy_high = Column(Float)
    pregnancy_trimester = Column(String(50))
    
    # Critical values
    critical_low = Column(Float)
    critical_high = Column(Float)
    panic_low = Column(Float)
    panic_high = Column(Float)
    
    # Interpretation
    high_interpretation = Column(Text)
    low_interpretation = Column(Text)
    
    # Simple explanation (6th grade reading level)
    simple_what_is = Column(Text)
    simple_high_means = Column(Text)
    simple_low_means = Column(Text)
    simple_food_tips = Column(Text)
    simple_cartoon_explanation = Column(Text)  # Ultra simple
    
    # Clinical
    test_purpose = Column(Text)
    when_ordered = Column(Text)
    interfering_factors = Column(Text)
    preparation = Column(Text)
    
    # Related
    panel = Column(String(100))  # CBC, LFT, etc.
    related_tests = Column(Text)
    
    source = Column(String(50))  # LOINC, MIMIC

# ==========================================
# 3. RADIOLOGY DICTIONARY (X-Ray, MRI, Ultrasound)
# ==========================================
class RadiologyDictionary(Base):
    __tablename__ = "radiology_dictionary"
    
    id = Column(Integer, primary_key=True)
    term = Column(String(200), index=True)  # Medical term
    category = Column(String(50))  # X-Ray, MRI, CT, Ultrasound
    
    # Body location
    anatomical_region = Column(String(100))  # Chest, Brain, Spine
    anatomical_detail = Column(Text)
    
    # Radiology language
    radiologist_phrase = Column(Text)  # What radiologists write
    simple_translation = Column(Text)  # What it means in simple words
    
    # Findings
    normal_appearance = Column(Text)
    abnormal_findings = Column(Text)
    
    # Conditions detected
    conditions_indicated = Column(Text)
    severity_indicators = Column(Text)
    
    # Patient explanation
    patient_explanation = Column(Text)  # Elderly-friendly
    visual_metaphor = Column(Text)  # "Like a cloudy window"
    
    # Follow-up
    recommended_followup = Column(Text)
    urgency = Column(String(50))  # Routine, Urgent, Emergency
    
    source = Column(String(50))  # RadGraph, CheXpert

# ==========================================
# 4. MASTER LOOKUP TABLE
# ==========================================
class MasterLookup(Base):
    __tablename__ = "master_lookup"
    
    id = Column(Integer, primary_key=True)
    search_term = Column(String(200), index=True, unique=True)
    term_type = Column(String(50))  # medicine, test, disease, radiology
    
    # Cross-references (no foreign keys - standalone)
    drug_id = Column(Integer, nullable=True)
    lab_id = Column(Integer, nullable=True)
    disease_id = Column(Integer, nullable=True)
    radiology_id = Column(Integer, nullable=True)
    
    # Simple answer
    simple_answer = Column(Text)
    detailed_answer = Column(Text)
    
    # Related terms
    synonyms = Column(Text)
    related_terms = Column(Text)
    
    # Language variants
    urdu_term = Column(String(200))
    hindi_term = Column(String(200))
    arabic_term = Column(String(200))