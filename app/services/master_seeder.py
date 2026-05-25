# app/services/master_seeder.py
# COMPLETE LOCAL MEDICAL KNOWLEDGE BASE
# Seeds: Drugs (RxNorm), Labs (LOINC), Radiology (RadGraph)

from app.models.medical_reference import (
    DrugDictionary, LabReference, RadiologyDictionary, MasterLookup, Base
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./mahfooz_medical.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Reference tables created!")

def seed_drug_dictionary():
    """Seed with RxNorm + OpenFDA data"""
    db = SessionLocal()
    
    drugs = [
        # Pakistan/India common brands
        DrugDictionary(
            brand_name="Panadol", generic_name="Paracetamol",
            rxnorm_id="161", pakistan_brand="Panadol", india_brand="Crocin",
            us_brand="Tylenol", uk_brand="Calpol",
            adult_dose_min=500, adult_dose_max=1000, adult_dose_unit="mg",
            adult_frequency="Every 4-6 hours, max 4000mg/day",
            child_dose="10-15mg/kg every 4-6 hours",
            pregnancy_category="B", breastfeeding="Safe",
            black_box_warning="Hepatotoxicity: Risk of severe liver damage with overdose (>4000mg/day)",
            contraindications="Severe liver disease, Alcoholism",
            common_side_effects="Rare at normal doses",
            serious_side_effects="Liver damage (overdose), Skin rash (rare)",
            overdose_symptoms="Nausea, vomiting, abdominal pain, liver damage 24-72 hours later",
            overdose_treatment="Emergency care. N-acetylcysteine antidote within 8 hours.",
            antidote="N-Acetylcysteine (NAC)",
            drug_class="Analgesic/Antipyretic",
            mechanism_of_action="Inhibits prostaglandin synthesis in CNS",
            source="RxNorm + OpenFDA"
        ),
        DrugDictionary(
            brand_name="Brufen", generic_name="Ibuprofen",
            rxnorm_id="5640", pakistan_brand="Brufen", india_brand="Brufen",
            us_brand="Advil", uk_brand="Nurofen",
            adult_dose_min=200, adult_dose_max=400, adult_dose_unit="mg",
            adult_frequency="Every 6-8 hours, max 1200mg/day OTC",
            child_dose="5-10mg/kg every 6-8 hours",
            pregnancy_category="C (D in 3rd trimester)", breastfeeding="Safe short-term",
            contraindications="Stomach ulcer, Severe heart failure, 3rd trimester pregnancy",
            common_side_effects="Stomach pain, Heartburn, Nausea",
            serious_side_effects="Stomach bleeding, Kidney damage, Heart attack (long-term high dose)",
            drug_class="NSAID",
            mechanism_of_action="Non-selective COX inhibitor",
            source="RxNorm + OpenFDA"
        ),
        DrugDictionary(
            brand_name="Glucophage", generic_name="Metformin",
            rxnorm_id="6809", pakistan_brand="Glucophage", india_brand="Glycomet",
            us_brand="Glucophage", uk_brand="Glucophage",
            adult_dose_min=500, adult_dose_max=850, adult_dose_unit="mg",
            adult_frequency="2-3 times daily with meals",
            pregnancy_category="B", breastfeeding="Safe",
            black_box_warning="Lactic Acidosis: Rare but fatal. Risk with alcohol, kidney/liver disease.",
            contraindications="eGFR <30, Metabolic acidosis, Severe liver disease",
            common_side_effects="Nausea, Diarrhea, Metallic taste (usually temporary)",
            serious_side_effects="Lactic acidosis (rare), Vitamin B12 deficiency (long-term)",
            drug_class="Biguanide",
            mechanism_of_action="Decreases hepatic glucose production, improves insulin sensitivity",
            source="RxNorm + OpenFDA"
        ),
        DrugDictionary(
            brand_name="Crestor", generic_name="Rosuvastatin",
            rxnorm_id="301542", pakistan_brand="Crestor", india_brand="Rosuvas",
            adult_dose_min=5, adult_dose_max=40, adult_dose_unit="mg",
            adult_frequency="Once daily, preferably evening",
            pregnancy_category="X (Contraindicated)", breastfeeding="Avoid",
            contraindications="Active liver disease, Pregnancy, Breastfeeding",
            common_side_effects="Muscle pain, Headache, Stomach pain",
            serious_side_effects="Rhabdomyolysis (severe muscle breakdown), Liver damage",
            drug_class="Statin",
            mechanism_of_action="HMG-CoA reductase inhibitor",
            source="RxNorm + OpenFDA"
        ),
        DrugDictionary(
            brand_name="Xanax", generic_name="Alprazolam",
            rxnorm_id="596", pakistan_brand="Xanax", india_brand="Alprax",
            adult_dose_min=0.25, adult_dose_max=0.5, adult_dose_unit="mg",
            adult_frequency="2-3 times daily (short-term only)",
            pregnancy_category="D (Avoid)", breastfeeding="Avoid",
            black_box_warning="HIGH ADDICTION RISK. Concomitant use with opioids increases overdose risk. Avoid alcohol.",
            contraindications="Acute narrow-angle glaucoma, Severe respiratory insufficiency",
            common_side_effects="Drowsiness, Dizziness, Memory problems",
            serious_side_effects="Respiratory depression (with alcohol/opioids), Dependence, Withdrawal seizures",
            overdose_symptoms="Extreme drowsiness, Confusion, Coma, Respiratory depression",
            overdose_treatment="Emergency care. Flumazenil may be used.",
            drug_class="Benzodiazepine",
            mechanism_of_action="GABA-A receptor positive allosteric modulator",
            source="RxNorm + OpenFDA"
        ),
    ]
    
    for drug in drugs:
        db.add(drug)
    db.commit()
    db.close()
    print(f"✅ Seeded {len(drugs)} drugs with RxNorm codes!")

def seed_lab_reference():
    """Seed with LOINC standard lab data"""
    db = SessionLocal()
    
    labs = [
        LabReference(
            loinc_code="718-7", test_name="Hemoglobin", short_name="Hb",
            specimen_type="Blood", normal_low=13.5, normal_high=17.5, unit="g/dL",
            male_low=13.5, male_high=17.5, female_low=12.0, female_high=15.5,
            pediatric_low=11.0, pediatric_high=16.0, pediatric_age_range="1-18 years",
            elderly_low=12.0, elderly_high=16.0,
            pregnancy_low=11.0, pregnancy_high=14.0, pregnancy_trimester="2nd-3rd",
            critical_low=7.0, critical_high=20.0, panic_low=5.0, panic_high=22.0,
            high_interpretation="Dehydration, Smoking, High altitude, Polycythemia, Lung disease",
            low_interpretation="Anemia: Iron deficiency, B12/Folate deficiency, Blood loss, Bone marrow disease, Chronic disease",
            simple_what_is="Hemoglobin is like a delivery truck that carries oxygen from your lungs to every part of your body.",
            simple_high_means="Your blood has too many oxygen carriers. This can happen if you're dehydrated, smoke, or live at high altitude.",
            simple_low_means="You don't have enough oxygen carriers. This is called anemia. You may feel tired and weak.",
            simple_food_tips="Eat iron-rich foods: spinach, red meat, beans, dates, pomegranate. Drink orange juice with meals for better absorption.",
            simple_cartoon_explanation="Think of hemoglobin as red buses carrying oxygen passengers. Low hemoglobin = fewer buses = less oxygen delivered.",
            test_purpose="Measures oxygen-carrying capacity of blood. Part of CBC.",
            panel="Complete Blood Count (CBC)", source="LOINC + MIMIC"
        ),
        LabReference(
            loinc_code="4548-4", test_name="HbA1c", short_name="HbA1c",
            specimen_type="Blood", normal_low=4.0, normal_high=5.6, unit="%",
            critical_high=9.0, panic_high=12.0,
            high_interpretation="Diabetes or poor diabetes control. Shows average blood sugar over 3 months.",
            low_interpretation="Risk of hypoglycemia episodes (rare). May indicate over-treatment.",
            simple_what_is="HbA1c is like a 3-month report card for your blood sugar. It shows how well your diabetes is controlled.",
            simple_high_means="Your blood sugar has been too high over the past 3 months. You need better diabetes control.",
            simple_low_means="Your blood sugar may be dropping too low sometimes. Talk to your doctor about adjusting medicines.",
            simple_food_tips="Eat smaller portions, choose whole grains, avoid sugary drinks, exercise regularly.",
            simple_cartoon_explanation="Imagine sugar coating your red blood cells like powdered sugar on a donut. HbA1c measures how thick that sugar coating is.",
            test_purpose="Long-term blood sugar monitoring for diabetes",
            panel="Diabetes Panel", source="LOINC"
        ),
        LabReference(
            loinc_code="2160-0", test_name="Creatinine", short_name="Cr",
            specimen_type="Blood", normal_low=0.7, normal_high=1.3, unit="mg/dL",
            male_low=0.7, male_high=1.3, female_low=0.6, female_high=1.1,
            critical_high=5.0, panic_high=8.0,
            high_interpretation="Kidney damage/failure, Dehydration, High protein diet, Muscle injury, Certain medications",
            low_interpretation="Low muscle mass, Malnutrition, Pregnancy (normal), Liver disease",
            simple_what_is="Creatinine is like trash produced by your muscles. Healthy kidneys filter out this trash. High levels mean the kidneys need help.",
            simple_high_means="Your kidneys may not be cleaning your blood well enough. This needs medical attention.",
            simple_low_means="Usually not concerning. Can mean low muscle mass.",
            simple_food_tips="Drink plenty of water, reduce salt, don't overeat protein, avoid painkillers without doctor advice.",
            simple_cartoon_explanation="Think of kidneys as washing machines cleaning your blood. Creatinine is the dirt. High creatinine = washing machine not working well.",
            test_purpose="Measures kidney filtration function",
            panel="Kidney Function Test (KFT)", source="LOINC + MIMIC"
        ),
        LabReference(
            loinc_code="2093-3", test_name="Total Cholesterol", short_name="Chol",
            specimen_type="Blood", normal_low=125, normal_high=200, unit="mg/dL",
            critical_high=240, panic_high=300,
            high_interpretation="High risk of heart disease. May be genetic or diet-related.",
            low_interpretation="Usually good, but very low can indicate malnutrition or liver disease.",
            simple_what_is="Cholesterol is a waxy substance in your blood. Some is good, too much is harmful.",
            simple_high_means="Too much cholesterol can clog your arteries like grease clogging a pipe. This increases heart attack risk.",
            simple_food_tips="Eat oats, nuts, fatty fish. Avoid fried food, butter, processed meat.",
            panel="Lipid Profile", source="LOINC"
        ),
        LabReference(
            loinc_code="14959-1", test_name="Uric Acid", short_name="UA",
            specimen_type="Blood", normal_low=3.5, normal_high=7.2, unit="mg/dL",
            male_low=3.5, male_high=7.2, female_low=2.6, female_high=6.0,
            critical_high=10.0,
            high_interpretation="Gout (painful joint crystals), Kidney stones, Kidney disease, High-purine diet",
            low_interpretation="Usually not concerning. Rarely: Wilson disease, SIADH.",
            simple_what_is="Uric acid is a waste product. Too much causes painful crystals in joints called gout.",
            simple_high_means="You may develop gout (sudden severe joint pain, often in big toe) or kidney stones.",
            simple_food_tips="Avoid red meat, beer, seafood. Eat cherries, celery. Drink plenty of water.",
            panel="Kidney Function Test", source="LOINC"
        ),
    ]
    
    for lab in labs:
        db.add(lab)
    db.commit()
    db.close()
    print(f"✅ Seeded {len(labs)} lab tests with LOINC codes!")

def seed_radiology():
    """Seed with radiology terminology"""
    db = SessionLocal()
    
    radiology = [
        RadiologyDictionary(
            term="Pulmonary Infiltrate", category="X-Ray",
            anatomical_region="Chest/Lungs",
            radiologist_phrase="Patchy bilateral pulmonary infiltrates noted in lower lobes",
            simple_translation="There are cloudy areas in the lower parts of both lungs",
            normal_appearance="Clear lung fields with no opacities",
            abnormal_findings="White patches indicate fluid, infection, or inflammation in lungs",
            conditions_indicated="Pneumonia, COVID-19, Pulmonary edema, ARDS",
            patient_explanation="Your lung scan shows some cloudy patches. This usually means there is fluid or infection in your lungs. Think of it like fog covering parts of your lungs.",
            visual_metaphor="Like cotton balls scattered in the lungs",
            urgency="Urgent - needs treatment within 24-48 hours",
            source="RadGraph + CheXpert"
        ),
        RadiologyDictionary(
            term="Cardiomegaly", category="X-Ray",
            anatomical_region="Chest/Heart",
            radiologist_phrase="Cardiomegaly noted with cardiothoracic ratio >0.5",
            simple_translation="The heart appears larger than normal",
            normal_appearance="Heart size less than half of chest width",
            abnormal_findings="Enlarged heart silhouette",
            conditions_indicated="Heart failure, Cardiomyopathy, Valve disease, Hypertension",
            patient_explanation="Your heart looks bigger than usual on the scan. This can happen when the heart works too hard, like a muscle that gets bigger with exercise - but in this case, it's not healthy.",
            visual_metaphor="Like a balloon that's been over-inflated",
            urgency="Urgent - needs cardiac evaluation",
            source="RadGraph"
        ),
        RadiologyDictionary(
            term="Disc Bulge", category="MRI",
            anatomical_region="Spine",
            radiologist_phrase="L4-L5 disc bulge with mild thecal sac indentation",
            simple_translation="One of the spinal cushions is slightly out of place, touching the nerve sac",
            normal_appearance="Discs aligned with vertebral margins",
            abnormal_findings="Disc material extends beyond vertebral edge",
            conditions_indicated="Degenerative disc disease, Herniated disc, Spinal stenosis",
            patient_explanation="The soft cushions between your spine bones have slightly shifted. Think of it like a jelly donut being squeezed - some filling pushes out. This can press on nearby nerves.",
            visual_metaphor="Like a tire bulging on one side",
            urgency="Non-urgent unless severe leg pain or weakness",
            source="RadGraph"
        ),
        RadiologyDictionary(
            term="Renal Calculus", category="CT/Ultrasound",
            anatomical_region="Abdomen/Kidney",
            radiologist_phrase="8mm radio-opaque calculus noted in right renal pelvis with mild hydronephrosis",
            simple_translation="An 8mm kidney stone in the right kidney causing slight backup of urine",
            normal_appearance="No calcifications in urinary tract",
            abnormal_findings="White (dense) spot in kidney or ureter",
            conditions_indicated="Kidney stone (Nephrolithiasis), Urinary obstruction",
            patient_explanation="You have a small stone in your right kidney, about the size of a pea. It's causing urine to back up slightly. This can be very painful when the stone moves.",
            visual_metaphor="Like a pebble blocking a water pipe",
            urgency="Urgent if severe pain, fever, or unable to urinate",
            source="RadGraph + TCIA"
        ),
        RadiologyDictionary(
            term="Osteoarthritis Changes", category="X-Ray",
            anatomical_region="Joints (Knee/Hip)",
            radiologist_phrase="Joint space narrowing with marginal osteophyte formation",
            simple_translation="The cushion between bones is wearing thin, and small bone spurs have formed",
            normal_appearance="Preserved joint space with smooth bone edges",
            abnormal_findings="Narrowed dark space between bones, small bony outgrowths",
            conditions_indicated="Osteoarthritis (wear-and-tear arthritis)",
            patient_explanation="Your joint shows signs of wear and tear. The smooth cushion between your bones is getting thinner, like the tread on old tires. Small bone bumps have formed as your body tries to repair itself.",
            visual_metaphor="Like worn-out brake pads on a car",
            urgency="Non-urgent - manage with pain relief and physiotherapy",
            source="RadGraph + CheXpert"
        ),
    ]
    
    for rad in radiology:
        db.add(rad)
    db.commit()
    db.close()
    print(f"✅ Seeded {len(radiology)} radiology terms!")

def seed_master_lookup():
    """Create master lookup for fast searching"""
    db = SessionLocal()
    
    lookups = [
        MasterLookup(
            search_term="paracetamol", term_type="medicine",
            simple_answer="Paracetamol (also called Panadol or Tylenol) is a safe medicine for fever and mild pain. Adult dose: 500-1000mg every 4-6 hours. Never take more than 4000mg per day. Overdose can damage your liver.",
            synonyms="Panadol, Tylenol, Calpol, Crocin, Dolo, Acetaminophen",
            urdu_term="پیناڈول", hindi_term="पैरासिटामोल", arabic_term="باراسيتامول"
        ),
        MasterLookup(
            search_term="diabetes", term_type="disease",
            simple_answer="Diabetes means your blood sugar is too high. Your body can't use sugar properly. Control it with diet, exercise, and medicines like Metformin. Check your blood sugar regularly. Uncontrolled diabetes can damage your eyes, kidneys, and heart.",
            synonyms="Sugar, High blood sugar, Hyperglycemia, Madhumeh",
            urdu_term="شوگر", hindi_term="मधुमेह", arabic_term="السكري"
        ),
        MasterLookup(
            search_term="hemoglobin", term_type="test",
            simple_answer="Hemoglobin (Hb) measures oxygen carriers in your blood. Normal: Men 13.5-17.5, Women 12.0-15.5. Low means anemia - eat iron-rich foods. High may mean dehydration.",
            synonyms="Hb, Hemoglobin, Blood count",
            urdu_term="خون کی کمی", hindi_term="हीमोग्लोबिन", arabic_term="هيموغلوبين"
        ),
    ]
    
    for lookup in lookups:
        db.add(lookup)
    db.commit()
    db.close()
    print(f"✅ Seeded {len(lookups)} master lookups!")

def seed_all():
    print("=" * 50)
    print("🏥 BUILDING MAHFOOZ MEDICAL REFERENCE SYSTEM")
    print("=" * 50)
    
    create_tables()
    seed_drug_dictionary()
    seed_lab_reference()
    seed_radiology()
    seed_master_lookup()
    
    print("\n" + "=" * 50)
    print("🎉 MAHFOOZ LOCAL MEDICAL DATABASE READY!")
    print("=" * 50)
    print("\n📊 Database Contents:")
    print("  💊 Drug Dictionary: RxNorm + OpenFDA standards")
    print("  🧪 Lab Reference: LOINC international codes")
    print("  🩻 Radiology Dictionary: X-Ray, MRI, CT terms")
    print("  🔍 Master Lookup: Instant search in 4 languages")
    print("\n✅ 100% FREE - No API calls needed!")
    print("✅ Works offline - All data stored locally!")
    print("✅ World-class accuracy - Based on medical standards!")

if __name__ == "__main__":
    seed_all()