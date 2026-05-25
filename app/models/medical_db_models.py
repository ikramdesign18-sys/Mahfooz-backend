# app/models/medical_db_models.py
# COMPREHENSIVE LOCAL MEDICAL DATABASE
# Stores downloaded data from OpenFDA, Wikidoc, UMLS

from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os

Base = declarative_base()

# ==========================================
# TABLE 1: MEDICINES (OpenFDA + ChEMBL)
# ==========================================
class MedicineTable(Base):
    __tablename__ = "medicine_database"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    brand_name = Column(String(200), index=True)
    generic_name = Column(String(200), index=True)
    manufacturer = Column(String(200))
    drug_class = Column(String(100))
    
    # Core Information
    indications = Column(Text)  # What it treats
    contraindications = Column(Text)  # When NOT to use
    side_effects = Column(Text)
    warnings = Column(Text)
    boxed_warning = Column(Text)  # FDA black box warning
    
    # Dosage
    adult_dosage = Column(Text)
    child_dosage = Column(Text)
    elderly_dosage = Column(Text)
    pregnancy_category = Column(String(5))  # A, B, C, D, X
    breastfeeding_safety = Column(Text)
    
    # Administration
    route = Column(String(50))  # oral, IV, IM, topical
    frequency = Column(String(100))
    duration = Column(String(100))
    storage = Column(Text)
    
    # Safety
    overdose_symptoms = Column(Text)
    overdose_treatment = Column(Text)
    monitoring_required = Column(Text)
    
    # Chemical Properties (from ChEMBL)
    molecular_formula = Column(String(100))
    molecular_weight = Column(Float)
    half_life = Column(String(50))
    
    # Source
    fda_application_number = Column(String(50))
    source_database = Column(String(50))  # OpenFDA, ChEMBL, etc.

# ==========================================
# TABLE 2: DISEASES & CONDITIONS (Wikidoc + UMLS)
# ==========================================
class DiseaseTable(Base):
    __tablename__ = "disease_database"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    condition_name = Column(String(200), index=True)
    umls_code = Column(String(50), unique=True)  # UMLS concept ID
    snomed_ct = Column(String(50))  # SNOMED code
    icd10_code = Column(String(20))  # ICD-10 billing code
    
    # Classification
    category = Column(String(100))  # Cardiovascular, Respiratory, etc.
    subcategory = Column(String(100))
    is_emergency = Column(Boolean, default=False)
    is_contagious = Column(Boolean, default=False)
    is_chronic = Column(Boolean, default=False)
    
    # Clinical Information
    definition = Column(Text)
    pathophysiology = Column(Text)  # How disease works
    causes = Column(Text)
    risk_factors = Column(Text)
    
    # Symptoms
    primary_symptoms = Column(Text)
    secondary_symptoms = Column(Text)
    atypical_symptoms = Column(Text)
    symptom_onset = Column(String(100))  # sudden, gradual, etc.
    symptom_duration = Column(String(100))
    
    # Diagnosis
    diagnostic_criteria = Column(Text)
    lab_tests = Column(Text)
    imaging_studies = Column(Text)
    differential_diagnosis = Column(Text)
    
    # Treatment
    first_line_treatment = Column(Text)
    second_line_treatment = Column(Text)
    surgical_options = Column(Text)
    lifestyle_changes = Column(Text)
    
    # Prognosis
    expected_outcome = Column(Text)
    recovery_time = Column(String(100))
    mortality_rate = Column(String(50))
    recurrence_rate = Column(String(50))
    
    # Prevention
    prevention_methods = Column(Text)
    screening_guidelines = Column(Text)
    vaccination = Column(Text)
    
    # Special Populations
    pregnancy_considerations = Column(Text)
    pediatric_considerations = Column(Text)
    elderly_considerations = Column(Text)
    
    # Complications
    common_complications = Column(Text)
    rare_complications = Column(Text)
    warning_signs = Column(Text)
    
    # Source
    source = Column(String(50))  # Wikidoc, UMLS, etc.
    last_updated = Column(String(50))

# ==========================================
# TABLE 3: LAB METRICS & TESTS
# ==========================================
class LabMetricTable(Base):
    __tablename__ = "lab_metrics_database"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_name = Column(String(200), index=True)
    abbreviation = Column(String(20), index=True)
    loinc_code = Column(String(20))  # LOINC standard code
    
    # Reference Ranges
    normal_range_low = Column(Float)
    normal_range_high = Column(Float)
    critical_low = Column(Float)
    critical_high = Column(Float)
    unit = Column(String(20))  # mg/dL, mmol/L, etc.
    
    # Population-specific ranges
    male_range_low = Column(Float)
    male_range_high = Column(Float)
    female_range_low = Column(Float)
    female_range_high = Column(Float)
    pediatric_range = Column(String(100))
    elderly_range = Column(String(100))
    pregnancy_range = Column(String(100))
    
    # Interpretation
    high_means = Column(Text)
    low_means = Column(Text)
    high_causes = Column(Text)
    low_causes = Column(Text)
    high_treatment = Column(Text)
    low_treatment = Column(Text)
    
    # Clinical Context
    test_purpose = Column(Text)
    when_to_test = Column(Text)
    preparation_required = Column(Text)
    interfering_factors = Column(Text)
    
    # Related Tests
    related_tests = Column(Text)
    panel_name = Column(String(100))  # CBC, LFT, Lipid Panel, etc.
    
    # Simple Explanation (patient-friendly)
    simple_explanation = Column(Text)
    food_tips = Column(Text)
    
    # Source
    source = Column(String(50))

# ==========================================
# TABLE 4: MEDICAL ABBREVIATIONS (UMLS)
# ==========================================
class MedicalAbbreviation(Base):
    __tablename__ = "medical_abbreviations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    abbreviation = Column(String(20), index=True, unique=True)
    full_form = Column(String(200))
    category = Column(String(50))  # prescription, diagnosis, anatomy, etc.
    context = Column(Text)
    common_usage = Column(Text)

# ==========================================
# TABLE 5: DRUG INTERACTIONS
# ==========================================
class DrugInteraction(Base):
    __tablename__ = "drug_interactions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    drug1 = Column(String(200), index=True)
    drug2 = Column(String(200), index=True)
    severity = Column(String(20))  # MILD, MODERATE, MAJOR, CONTRAINDICATED
    effect = Column(Text)
    mechanism = Column(Text)
    recommendation = Column(Text)
    source = Column(String(100))