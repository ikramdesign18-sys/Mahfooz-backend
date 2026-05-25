# app/services/database_seeder.py
# Pre-populates local database with verified medical data
# Data sourced from OpenFDA, Wikidoc, UMLS (simulated for demo)

from app.models.medical_db_models import (
    MedicineTable, DiseaseTable, LabMetricTable, 
    MedicalAbbreviation, DrugInteraction, Base
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Create local medical database
DATABASE_URL = "sqlite:///./mahfooz_medical.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def create_tables():
    """Create all medical database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Medical database tables created!")

def seed_medicines():
    """Seed medicine database with common drugs"""
    db = SessionLocal()
    
    medicines = [
        MedicineTable(
            brand_name="Panadol", generic_name="Paracetamol",
            manufacturer="GSK", drug_class="Analgesic",
            indications="Fever, Mild to moderate pain, Headache, Toothache, Body ache",
            contraindications="Severe liver disease, Alcoholism",
            side_effects="Rare at normal doses. Overdose causes liver damage.",
            warnings="Maximum 4000mg/day for adults. Overdose can be fatal.",
            boxed_warning="Hepatotoxicity: Risk of severe liver damage with overdose.",
            adult_dosage="500-1000mg every 4-6 hours, max 4000mg/day",
            child_dosage="10-15mg/kg every 4-6 hours, max 5 doses/day",
            pregnancy_category="B", breastfeeding_safety="Safe",
            route="Oral", frequency="Every 4-6 hours as needed",
            overdose_symptoms="Nausea, vomiting, abdominal pain, liver damage (24-72 hours later)",
            overdose_treatment="Seek emergency care immediately. N-acetylcysteine antidote within 8 hours.",
            source_database="OpenFDA"
        ),
        MedicineTable(
            brand_name="Brufen", generic_name="Ibuprofen",
            manufacturer="Abbott", drug_class="NSAID",
            indications="Pain, Inflammation, Fever, Arthritis, Menstrual pain, Toothache",
            contraindications="Stomach ulcer, Severe heart failure, 3rd trimester pregnancy",
            side_effects="Stomach pain, Heartburn, Nausea, Dizziness",
            warnings="Take with food. Avoid in pregnancy 3rd trimester. Caution in asthma.",
            adult_dosage="200-400mg every 6-8 hours, max 1200mg/day OTC",
            child_dosage="5-10mg/kg every 6-8 hours (over 6 months)",
            pregnancy_category="C (D in 3rd trimester)", breastfeeding_safety="Safe short-term",
            route="Oral", frequency="Every 6-8 hours",
            source_database="OpenFDA"
        ),
        MedicineTable(
            brand_name="Glucophage", generic_name="Metformin",
            manufacturer="Merck", drug_class="Biguanide",
            indications="Type 2 diabetes, PCOS, Insulin resistance",
            contraindications="Severe kidney disease (eGFR <30), Metabolic acidosis",
            side_effects="Nausea, Diarrhea, Metallic taste, Loss of appetite (usually temporary)",
            warnings="Take with meals. Stop before contrast dye procedures. Monitor kidney function.",
            boxed_warning="Lactic Acidosis: Rare but serious. Risk increased with alcohol, kidney/liver problems.",
            adult_dosage="500mg 2-3 times daily or 850mg twice daily with meals",
            child_dosage="Not recommended under 10 years",
            elderly_dosage="Start low, monitor kidney function",
            pregnancy_category="B", breastfeeding_safety="Safe",
            route="Oral", frequency="2-3 times daily with meals",
            monitoring_required="Blood sugar daily, HbA1c every 3 months, kidney function annually",
            molecular_formula="C4H11N5", molecular_weight=129.16,
            source_database="OpenFDA + ChEMBL"
        ),
    ]
    
    for med in medicines:
        db.add(med)
    
    db.commit()
    db.close()
    print(f"✅ Seeded {len(medicines)} medicines!")

def seed_diseases():
    """Seed disease database"""
    db = SessionLocal()
    
    diseases = [
        DiseaseTable(
            condition_name="Type 2 Diabetes Mellitus",
            icd10_code="E11", category="Endocrine",
            is_chronic=True,
            definition="A chronic condition where the body becomes resistant to insulin or doesn't produce enough insulin.",
            pathophysiology="Insulin resistance in peripheral tissues leads to hyperglycemia. Beta cells eventually fail.",
            causes="Genetics, Obesity, Sedentary lifestyle, Poor diet, Age >45",
            risk_factors="Family history, Obesity (BMI>30), Physical inactivity, High BP, High cholesterol",
            primary_symptoms="Frequent urination, Extreme thirst, Hunger, Fatigue, Blurry vision",
            secondary_symptoms="Slow healing wounds, Tingling in hands/feet, Recurrent infections",
            diagnostic_criteria="Fasting glucose ≥126 mg/dL OR HbA1c ≥6.5% OR OGTT ≥200 mg/dL",
            lab_tests="Fasting blood sugar, HbA1c, Oral glucose tolerance test, C-peptide",
            first_line_treatment="Metformin + Lifestyle changes (diet, exercise)",
            second_line_treatment="Sulfonylureas, DPP-4 inhibitors, GLP-1 agonists, Insulin",
            lifestyle_changes="Weight loss (5-10%), 150 min exercise/week, Low-carb diet, Monitor sugar",
            common_complications="Heart disease, Kidney failure, Blindness, Nerve damage, Foot amputation", rare_complications="Diabetic ketoacidosis, Hyperosmolar coma",
            prevention_methods="Maintain healthy weight, Regular exercise, Balanced diet, Regular screening after 45",
            source="Wikidoc"
        ),
        DiseaseTable(
            condition_name="Hypertension (High Blood Pressure)",
            icd10_code="I10", category="Cardiovascular",
            is_chronic=True,
            definition="Persistent elevation of blood pressure above 130/80 mmHg.",
            causes="Genetics, High salt diet, Obesity, Stress, Kidney disease, Thyroid problems",
            risk_factors="Age >40, Family history, Obesity, Smoking, High salt intake, Alcohol, Stress",
            primary_symptoms="Often NO symptoms (silent killer), Headaches (severe), Nosebleeds (rare)",
            diagnostic_criteria="BP ≥130/80 mmHg on 2 separate occasions",
            lab_tests="Blood pressure monitoring, Kidney function, Electrolytes, ECG, Echocardiogram",
            first_line_treatment="Lifestyle changes + ACE inhibitors or ARBs or CCBs",
            lifestyle_changes="DASH diet, Reduce salt (<5g/day), Exercise, Limit alcohol, Quit smoking",
            common_complications="Heart attack, Stroke, Kidney failure, Vision loss, Dementia", rare_complications="Hypertensive crisis, Aortic dissection",
            prevention_methods="Healthy diet, Regular exercise, No smoking, Limit alcohol, Regular BP checks",
            source="Wikidoc"
        ),
    ]
    
    for disease in diseases:
        db.add(disease)
    
    db.commit()
    db.close()
    print(f"✅ Seeded {len(diseases)} diseases!")

def seed_lab_metrics():
    """Seed lab metrics database"""
    db = SessionLocal()
    
    metrics = [
        LabMetricTable(
            test_name="Hemoglobin", abbreviation="Hb",
            loinc_code="718-7",
            normal_range_low=13.5, normal_range_high=17.5, unit="g/dL",
            male_range_low=13.5, male_range_high=17.5,
            female_range_low=12.0, female_range_high=15.5,
            pediatric_range="11-16 g/dL (varies by age)",
            critical_low=7.0, critical_high=20.0,
            high_means="Dehydration, Smoking, Living at high altitudes, Polycythemia",
            low_means="Anemia - iron deficiency, B12 deficiency, Blood loss, Bone marrow problems",
            test_purpose="Measures oxygen-carrying capacity of blood",
            simple_explanation="Hemoglobin is like a delivery truck that carries oxygen from your lungs to every part of your body.",
            food_tips="Iron-rich foods: spinach, red meat, liver, beans, dates, pomegranate. Take with Vitamin C.",
            panel_name="CBC (Complete Blood Count)",
            source="OpenFDA + Wikidoc"
        ),
        LabMetricTable(
            test_name="HbA1c (Glycated Hemoglobin)", abbreviation="HbA1c",
            loinc_code="4548-4",
            normal_range_low=4.0, normal_range_high=5.6, unit="%",
            critical_low=4.0, critical_high=9.0,
            high_means="Diabetes or poor diabetes control. Shows average blood sugar over 3 months.",
            low_means="Risk of hypoglycemia episodes",
            test_purpose="Shows average blood sugar over past 2-3 months",
            simple_explanation="HbA1c is like a report card showing how well your blood sugar has been controlled over the last 3 months.",
            food_tips="Low-carb diet, regular exercise, monitor sugar, take medicines as prescribed",
            panel_name="Diabetes Monitoring",
            source="Wikidoc"
        ),
        LabMetricTable(
            test_name="Creatinine", abbreviation="Cr",
            loinc_code="2160-0",
            normal_range_low=0.7, normal_range_high=1.3, unit="mg/dL",
            male_range_low=0.7, male_range_high=1.3,
            female_range_low=0.6, female_range_high=1.1,
            critical_low=0.2, critical_high=5.0,
            high_means="Kidney damage or failure, Dehydration, High protein diet, Muscle damage",
            low_means="Low muscle mass, Malnutrition, Pregnancy",
            test_purpose="Measures kidney function - how well kidneys filter waste",
            simple_explanation="Creatinine is like trash that your muscles make. Healthy kidneys clean it out. High levels mean kidneys need help.",
            food_tips="Drink plenty water, reduce salt, moderate protein, avoid painkillers without doctor",
            panel_name="Kidney Function Test (KFT)",
            source="OpenFDA"
        ),
    ]
    
    for metric in metrics:
        db.add(metric)
    
    db.commit()
    db.close()
    print(f"✅ Seeded {len(metrics)} lab metrics!")

def seed_abbreviations():
    """Seed medical abbreviations"""
    db = SessionLocal()
    
    abbreviations = [
        MedicalAbbreviation(abbreviation="BID", full_form="Twice a day", category="Prescription", common_usage="Take medicine twice daily"),
        MedicalAbbreviation(abbreviation="TID", full_form="Three times a day", category="Prescription", common_usage="Take medicine three times daily"),
        MedicalAbbreviation(abbreviation="QID", full_form="Four times a day", category="Prescription", common_usage="Take medicine four times daily"),
        MedicalAbbreviation(abbreviation="PRN", full_form="As needed", category="Prescription", common_usage="Take only when required"),
        MedicalAbbreviation(abbreviation="HS", full_form="At bedtime", category="Prescription", common_usage="Take before sleeping"),
        MedicalAbbreviation(abbreviation="PC", full_form="After meals", category="Prescription", common_usage="Take after eating"),
        MedicalAbbreviation(abbreviation="AC", full_form="Before meals", category="Prescription", common_usage="Take before eating"),
        MedicalAbbreviation(abbreviation="PO", full_form="By mouth", category="Administration", common_usage="Take orally"),
        MedicalAbbreviation(abbreviation="NPO", full_form="Nothing by mouth", category="Administration", common_usage="No food or drink"),
        MedicalAbbreviation(abbreviation="HTN", full_form="Hypertension", category="Diagnosis", common_usage="High blood pressure"),
        MedicalAbbreviation(abbreviation="DM", full_form="Diabetes Mellitus", category="Diagnosis", common_usage="Diabetes"),
        MedicalAbbreviation(abbreviation="CVA", full_form="Cerebrovascular Accident", category="Diagnosis", common_usage="Stroke"),
        MedicalAbbreviation(abbreviation="MI", full_form="Myocardial Infarction", category="Diagnosis", common_usage="Heart attack"),
        MedicalAbbreviation(abbreviation="SOB", full_form="Shortness of Breath", category="Symptom", common_usage="Difficulty breathing"),
        MedicalAbbreviation(abbreviation="Fx", full_form="Fracture", category="Diagnosis", common_usage="Broken bone"),
    ]
    
    for abbr in abbreviations:
        db.add(abbr)
    
    db.commit()
    db.close()
    print(f"✅ Seeded {len(abbreviations)} abbreviations!")

def seed_interactions():
    """Seed drug interactions"""
    db = SessionLocal()
    
    interactions = [
        DrugInteraction(drug1="Warfarin", drug2="Aspirin", severity="MAJOR", 
                       effect="Severe bleeding risk", mechanism="Both inhibit clotting",
                       recommendation="Avoid combination. Use with extreme caution only under doctor supervision."),
        DrugInteraction(drug1="Metformin", drug2="Alcohol", severity="MODERATE",
                       effect="Increased risk of lactic acidosis", mechanism="Alcohol affects lactate metabolism",
                       recommendation="Limit or avoid alcohol while taking metformin."),
        DrugInteraction(drug1="Paracetamol", drug2="Alcohol", severity="MAJOR",
                       effect="Severe liver damage", mechanism="Alcohol induces toxic paracetamol metabolites",
                       recommendation="Avoid alcohol completely when taking paracetamol."),
    ]
    
    for interaction in interactions:
        db.add(interaction)
    
    db.commit()
    db.close()
    print(f"✅ Seeded {len(interactions)} drug interactions!")

def seed_all():
    """Seed all database tables"""
    print("🏥 Creating MAHFOOZ Medical Database...")
    create_tables()
    seed_medicines()
    seed_diseases()
    seed_lab_metrics()
    seed_abbreviations()
    seed_interactions()
    print("🎉 Medical database ready!")

if __name__ == "__main__":
    seed_all()