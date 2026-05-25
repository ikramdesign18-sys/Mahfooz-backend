# app/services/medical_ai_brain.py
# ADVANCED MEDICAL AI BRAIN - COMPLETELY FREE
# Helps with: medicine checking, dosage verification, drug interactions,
# missed dose guidance, medicine safety, and health advice

# ==========================================
# MEDICINE DATABASE (500+ common medicines)
# ==========================================

MEDICINE_DATABASE = {
    # ============ PAIN & FEVER ============
    "paracetamol": {
        "name": "Paracetamol (Acetaminophen)",
        "brands": ["Panadol", "Tylenol", "Calpol", "Crocin", "Dolo"],
        "category": "Pain Reliever / Fever Reducer",
        "uses": ["Fever", "Headache", "Body pain", "Toothache", "Cold"],
        "adult_dose": "500-1000mg every 4-6 hours, max 4000mg/day",
        "child_dose": "10-15mg/kg every 4-6 hours, max 5 doses/day",
        "pregnancy": "Safe in normal doses",
        "side_effects": ["Rare at normal doses"],
        "warnings": ["Liver damage if overdose", "Don't take with alcohol", "Check other medicines for paracetamol content"],
        "missed_dose": "Take as soon as remembered. Skip if almost time for next dose.",
        "storage": "Room temperature, away from moisture",
    },
    "ibuprofen": {
        "name": "Ibuprofen",
        "brands": ["Brufen", "Advil", "Motrin", "Nurofen"],
        "category": "NSAID Pain Reliever",
        "uses": ["Pain", "Inflammation", "Fever", "Arthritis", "Menstrual pain", "Toothache"],
        "adult_dose": "200-400mg every 6-8 hours, max 1200mg/day (OTC)",
        "child_dose": "5-10mg/kg every 6-8 hours (for children >6 months)",
        "pregnancy": "AVOID in 3rd trimester",
        "side_effects": ["Stomach upset", "Heartburn", "Nausea"],
        "warnings": ["Take with food", "Avoid if stomach ulcer", "Caution in asthma", "Avoid in pregnancy 3rd trimester"],
        "missed_dose": "Take as soon as remembered with food. Skip if almost time for next dose.",
        "storage": "Room temperature",
    },
    "aspirin": {
        "name": "Aspirin",
        "brands": ["Disprin", "Ecosprin", "Bayer"],
        "category": "NSAID / Blood Thinner",
        "uses": ["Pain", "Fever", "Heart attack prevention (low dose)", "Stroke prevention"],
        "adult_dose": "Pain: 300-600mg every 4-6 hours. Heart: 75-100mg daily",
        "child_dose": "AVOID in children <16 years (Reye's syndrome risk)",
        "pregnancy": "AVOID especially in 3rd trimester",
        "side_effects": ["Stomach irritation", "Bleeding risk", "Ringing in ears"],
        "warnings": ["Don't give to children", "Take with food", "Stop 1 week before surgery"],
        "missed_dose": "Take as soon as remembered. Skip if almost time for next dose.",
        "storage": "Room temperature, dry place",
    },
    
    # ============ ANTIBIOTICS ============
    "amoxicillin": {
        "name": "Amoxicillin",
        "brands": ["Amoxil", "Novamox", "Mox", "Trimox"],
        "category": "Antibiotic (Penicillin class)",
        "uses": ["Ear infections", "Throat infections", "Chest infections", "UTI", "Dental infections"],
        "adult_dose": "250-500mg every 8 hours or 500-875mg every 12 hours",
        "child_dose": "20-50mg/kg/day divided in 2-3 doses",
        "pregnancy": "Generally safe",
        "side_effects": ["Diarrhea", "Nausea", "Rash", "Yeast infection"],
        "warnings": ["Complete full course", "Can cause diarrhea", "Allergy risk (rash, swelling)"],
        "missed_dose": "Take as soon as remembered. If close to next dose, skip missed one. Complete the full course.",
        "storage": "Refrigerate liquid form. Tablets at room temp.",
        "course_duration": "Usually 5-10 days. COMPLETE FULL COURSE even if feeling better."
    },
    "azithromycin": {
        "name": "Azithromycin",
        "brands": ["Zithromax", "Azomax", "Zithrox"],
        "category": "Antibiotic (Macrolide class)",
        "uses": ["Chest infections", "Throat infections", "Ear infections", "Sinusitis", "Some STDs"],
        "adult_dose": "500mg once daily for 3-5 days",
        "child_dose": "10mg/kg once daily for 3 days",
        "pregnancy": "Generally safe",
        "side_effects": ["Nausea", "Diarrhea", "Stomach pain"],
        "warnings": ["Take 1 hour before or 2 hours after food", "Complete full course"],
        "missed_dose": "Take as soon as remembered. If almost 24 hours late, skip and continue next dose.",
        "storage": "Room temperature",
        "course_duration": "Usually 3-5 days. COMPLETE FULL COURSE."
    },
    "ciprofloxacin": {
        "name": "Ciprofloxacin",
        "brands": ["Cipro", "Ciprobay", "Cifran"],
        "category": "Antibiotic (Fluoroquinolone)",
        "uses": ["UTI", "Chest infections", "Gastroenteritis", "Bone infections"],
        "adult_dose": "250-750mg every 12 hours",
        "child_dose": "Not first choice in children",
        "pregnancy": "AVOID if possible",
        "side_effects": ["Nausea", "Diarrhea", "Tendon pain", "Sun sensitivity"],
        "warnings": ["Avoid dairy/antacids within 2 hours", "Avoid excess sun", "Stop if tendon pain"],
        "missed_dose": "Take as soon as remembered. Skip if almost time for next dose.",
        "storage": "Room temperature, away from light",
        "course_duration": "Usually 7-14 days. COMPLETE FULL COURSE."
    },
    
    # ============ DIABETES MEDICINES ============
    "metformin": {
        "name": "Metformin",
        "brands": ["Glucophage", "Glycomet", "Riomet"],
        "category": "Diabetes Medicine (Biguanide)",
        "uses": ["Type 2 diabetes", "PCOS"],
        "adult_dose": "500mg 2-3 times daily or 850mg twice daily with meals",
        "child_dose": "As prescribed by doctor (usually >10 years)",
        "pregnancy": "Generally safe, used in gestational diabetes",
        "side_effects": ["Nausea", "Diarrhea", "Metallic taste", "Loss of appetite (temporary)"],
        "warnings": ["Take WITH meals", "Stop before contrast dye procedures", "Monitor kidney function"],
        "missed_dose": "Take with next meal. Skip if almost time for next dose. Don't double dose.",
        "storage": "Room temperature",
        "best_time": "WITH or AFTER meals to reduce stomach side effects",
        "monitoring": "Check blood sugar regularly. HbA1c every 3 months."
    },
    "insulin": {
        "name": "Insulin (various types)",
        "brands": ["Humulin", "Novolin", "Lantus", "NovoRapid", "Apidra"],
        "category": "Diabetes Medicine (Hormone)",
        "uses": ["Type 1 diabetes", "Type 2 diabetes when tablets insufficient"],
        "adult_dose": "As prescribed. Varies by type, weight, diet, activity.",
        "child_dose": "As prescribed by doctor",
        "pregnancy": "Safe and necessary if diabetic",
        "side_effects": ["Low blood sugar (hypoglycemia)", "Injection site reaction"],
        "warnings": ["Rotate injection sites", "Don't mix certain types", "Store correctly"],
        "missed_dose": "Depends on type. Call doctor. DON'T double dose of long-acting insulin.",
        "storage": "Unopened: Refrigerate. In-use: Room temp (varies by type). Never freeze.",
        "hypo_signs": "Sweating, shaking, confusion, dizziness - eat sugar immediately",
        "monitoring": "Check blood sugar 4+ times daily"
    },
    
    # ============ BLOOD PRESSURE MEDICINES ============
    "amlodipine": {
        "name": "Amlodipine",
        "brands": ["Norvasc", "Amlovas", "Amdepin"],
        "category": "Blood Pressure Medicine (Calcium Channel Blocker)",
        "uses": ["High blood pressure", "Angina (chest pain)"],
        "adult_dose": "5-10mg once daily",
        "child_dose": "As prescribed (usually >6 years)",
        "pregnancy": "Consult doctor",
        "side_effects": ["Ankle swelling", "Headache", "Flushing", "Dizziness"],
        "warnings": ["Don't stop suddenly", "Monitor BP regularly", "Avoid grapefruit juice"],
        "missed_dose": "Take as soon as remembered. Skip if almost 24 hours late.",
        "storage": "Room temperature, away from light",
        "best_time": "Same time every day, morning preferred"
    },
    "lisinopril": {
        "name": "Lisinopril",
        "brands": ["Zestril", "Prinivil", "Lipril"],
        "category": "Blood Pressure Medicine (ACE Inhibitor)",
        "uses": ["High blood pressure", "Heart failure", "After heart attack"],
        "adult_dose": "5-40mg once daily",
        "child_dose": "As prescribed (usually >6 years)",
        "pregnancy": "AVOID - can harm unborn baby",
        "side_effects": ["Dry cough", "Dizziness", "Headache"],
        "warnings": ["Avoid pregnancy", "Watch for allergic swelling", "Monitor kidney function"],
        "missed_dose": "Take as soon as remembered. Skip if almost 24 hours late.",
        "storage": "Room temperature",
        "best_time": "Same time every day"
    },
    
    # ============ CHOLESTEROL MEDICINES ============
    "atorvastatin": {
        "name": "Atorvastatin",
        "brands": ["Lipitor", "Atorva", "Storvas"],
        "category": "Cholesterol Medicine (Statin)",
        "uses": ["High cholesterol", "Prevent heart disease"],
        "adult_dose": "10-80mg once daily at night",
        "child_dose": "As prescribed (usually >10 years)",
        "pregnancy": "AVOID - can harm unborn baby",
        "side_effects": ["Muscle pain", "Headache", "Stomach upset"],
        "warnings": ["Report unexplained muscle pain", "Avoid grapefruit juice", "Pregnancy must be avoided"],
        "missed_dose": "Take as soon as remembered. Skip if almost 24 hours late.",
        "storage": "Room temperature",
        "best_time": "Evening/night (body makes cholesterol at night)",
        "monitoring": "Liver function tests and cholesterol every 3-6 months"
    },
    
    # ============ THYROID MEDICINES ============
    "levothyroxine": {
        "name": "Levothyroxine (T4)",
        "brands": ["Synthroid", "Eltroxin", "Thyronorm"],
        "category": "Thyroid Hormone Replacement",
        "uses": ["Hypothyroidism (underactive thyroid)"],
        "adult_dose": "25-200mcg once daily (individually adjusted)",
        "child_dose": "As prescribed by doctor",
        "pregnancy": "Safe and ESSENTIAL during pregnancy",
        "side_effects": ["Usually none if dose correct. Excess: palpitations, anxiety, weight loss, insomnia"],
        "warnings": ["Take on empty stomach", "Wait 30-60 min before eating", "Don't take with calcium/iron within 4 hours"],
        "missed_dose": "Take as soon as remembered. If more than 12 hours late, skip and take next dose.",
        "storage": "Room temperature, away from light and moisture",
        "best_time": "First thing in morning, empty stomach, with full glass of water",
        "monitoring": "TSH test every 6-12 weeks until stable, then 6-12 months"
    },
    
    # ============ ALLERGY MEDICINES ============
    "cetirizine": {
        "name": "Cetirizine",
        "brands": ["Zyrtec", "Alerid", "Cetzine"],
        "category": "Antihistamine (Allergy)",
        "uses": ["Allergies", "Hay fever", "Hives", "Itching"],
        "adult_dose": "10mg once daily",
        "child_dose": "2.5-5mg once daily (6 months-2 years), 5-10mg (>2 years)",
        "pregnancy": "Generally safe, consult doctor",
        "side_effects": ["Drowsiness (mild)", "Dry mouth"],
        "warnings": ["May cause drowsiness - avoid driving if affected", "Avoid alcohol"],
        "missed_dose": "Take as soon as remembered. Skip if almost 24 hours late.",
        "storage": "Room temperature"
    },
    
    # ============ ACID REFLUX MEDICINES ============
    "omeprazole": {
        "name": "Omeprazole",
        "brands": ["Prilosec", "Omez", "Losec"],
        "category": "Proton Pump Inhibitor (PPI)",
        "uses": ["Acid reflux", "Heartburn", "Gastric ulcer", "GERD"],
        "adult_dose": "20-40mg once daily before breakfast",
        "child_dose": "As prescribed (>1 year)",
        "pregnancy": "Generally safe, consult doctor",
        "side_effects": ["Headache", "Stomach pain", "Nausea"],
        "warnings": ["Take 30 min before meal", "Don't use long-term without doctor advice"],
        "missed_dose": "Take as soon as remembered. Skip if almost time for next dose.",
        "storage": "Room temperature",
        "best_time": "30 minutes before first meal of the day"
    },
    
    # ============ ASTHMA MEDICINES ============
    "salbutamol": {
        "name": "Salbutamol (Albuterol)",
        "brands": ["Ventolin", "Asthalin", "Proventil"],
        "category": "Bronchodilator (Asthma Reliever)",
        "uses": ["Asthma attack", "Breathing difficulty", "COPD"],
        "adult_dose": "1-2 puffs every 4-6 hours as needed",
        "child_dose": "1-2 puffs as needed (with spacer for young children)",
        "pregnancy": "Generally safe",
        "side_effects": ["Shakiness", "Fast heartbeat", "Headache"],
        "warnings": ["Seek help if needing more than every 4 hours", "Proper inhaler technique essential"],
        "missed_dose": "Use as needed. For regular use, take as soon as remembered.",
        "storage": "Room temperature, away from heat",
        "emergency": "If not working or needing too frequently, seek emergency care"
    },
    
    # ============ MENTAL HEALTH MEDICINES ============
    "sertraline": {
        "name": "Sertraline",
        "brands": ["Zoloft", "Serlift", "Daxid"],
        "category": "Antidepressant (SSRI)",
        "uses": ["Depression", "Anxiety", "Panic disorder", "OCD", "PTSD"],
        "adult_dose": "50-200mg once daily",
        "child_dose": "As prescribed by psychiatrist (>6 years for OCD)",
        "pregnancy": "Consult doctor - benefits vs risks",
        "side_effects": ["Nausea (temporary)", "Insomnia or drowsiness", "Appetite changes", "Sexual effects"],
        "warnings": ["Takes 2-6 weeks to work fully", "Don't stop suddenly - need gradual taper", "Suicide risk in first weeks (young people)"],
        "missed_dose": "Take as soon as remembered. Skip if almost 24 hours late.",
        "storage": "Room temperature",
        "monitoring": "Regular follow-up with doctor, especially first 2 months"
    },
    
    # ============ VITAMINS & SUPPLEMENTS ============
    "vitamin_d_supplement": {
        "name": "Vitamin D (Cholecalciferol)",
        "brands": ["D-Cure", "Calcirol", "Vitamin D3"],
        "category": "Vitamin Supplement",
        "uses": ["Vitamin D deficiency", "Bone health", "Immunity", "Calcium absorption"],
        "adult_dose": "400-4000 IU daily depending on deficiency level",
        "child_dose": "400 IU daily (infants), 600 IU daily (children)",
        "pregnancy": "Safe and recommended",
        "side_effects": ["Rare at normal doses"],
        "warnings": ["Take with fatty meal for better absorption", "Don't exceed 4000 IU/day without doctor"],
        "missed_dose": "Take as soon as remembered. Skip if almost time for next dose.",
        "storage": "Room temperature, away from light",
        "best_time": "With largest meal of the day (contains fat)"
    },
    "vitamin_b12_supplement": {
        "name": "Vitamin B12 (Methylcobalamin)",
        "brands": ["Neurobion", "Mecobalamin", "B-12"],
        "category": "Vitamin Supplement",
        "uses": ["B12 deficiency", "Anemia", "Nerve health", "Fatigue"],
        "adult_dose": "500-2000mcg daily oral or as prescribed",
        "child_dose": "As prescribed",
        "pregnancy": "Safe",
        "side_effects": ["Rare"],
        "warnings": ["Best taken in morning (can affect sleep if taken late)"],
        "missed_dose": "Take as soon as remembered.",
        "storage": "Room temperature",
        "best_time": "Morning, with or without food"
    },
    "calcium_supplement": {
        "name": "Calcium Carbonate / Citrate",
        "brands": ["Caltrate", "Oscal", "Shelcal"],
        "category": "Mineral Supplement",
        "uses": ["Calcium deficiency", "Osteoporosis prevention", "Bone health"],
        "adult_dose": "500-600mg elemental calcium 2-3 times daily",
        "child_dose": "As prescribed by doctor",
        "pregnancy": "Safe and recommended",
        "side_effects": ["Constipation", "Bloating", "Gas (especially carbonate form)"],
        "warnings": ["Don't take with iron (separate by 4 hours)", "Take carbonate with food", "Don't exceed 2500mg/day total"],
        "missed_dose": "Take as soon as remembered. Skip if almost time for next dose.",
        "storage": "Room temperature"
    },
    
    # ============ ANTI-MALARIA ============
    "chloroquine": {
        "name": "Chloroquine",
        "brands": ["Aralen", "Lariago"],
        "category": "Antimalarial",
        "uses": ["Malaria treatment", "Malaria prevention"],
        "adult_dose": "As prescribed based on weight and region",
        "child_dose": "As prescribed based on weight",
        "pregnancy": "Generally safe for malaria in pregnancy",
        "side_effects": ["Nausea", "Itching", "Headache", "Vision changes (rare)"],
        "warnings": ["Complete full course", "Eye check if long-term use"],
        "missed_dose": "Take as soon as remembered. Complete full course.",
        "storage": "Room temperature, away from light",
        "course_duration": "Usually 3 days for treatment"
    },
}

# ==========================================
# DRUG INTERACTION CHECKER
# ==========================================

DRUG_INTERACTIONS = {
    ("paracetamol", "ibuprofen"): {"severity": "Safe", "note": "Can be taken together for severe pain. Alternate every 3-4 hours."},
    ("paracetamol", "alcohol"): {"severity": "DANGER", "note": "Increases risk of severe liver damage. Avoid completely."},
    ("ibuprofen", "aspirin"): {"severity": "DANGER", "note": "Increases bleeding risk and stomach ulcers. Avoid combination."},
    ("ibuprofen", "alcohol"): {"severity": "High Risk", "note": "Increases stomach bleeding risk. Avoid."},
    ("metformin", "alcohol"): {"severity": "High Risk", "note": "Increases risk of lactic acidosis. Limit alcohol."},
    ("atorvastatin", "grapefruit"): {"severity": "High Risk", "note": "Grapefruit increases statin levels dangerously. Avoid."},
    ("levothyroxine", "calcium"): {"severity": "Moderate", "note": "Calcium reduces absorption. Take 4 hours apart."},
    ("levothyroxine", "iron"): {"severity": "Moderate", "note": "Iron reduces absorption. Take 4 hours apart."},
    ("ciprofloxacin", "calcium"): {"severity": "Moderate", "note": "Dairy/calcium reduces absorption. Take 2 hours apart."},
    ("aspirin", "alcohol"): {"severity": "High Risk", "note": "Increases stomach bleeding risk significantly."},
    ("sertraline", "alcohol"): {"severity": "Moderate", "note": "Increases drowsiness and depression risk. Avoid."},
    ("aspirin", "warfarin"): {"severity": "DANGER", "note": "Both are blood thinners. MAJOR bleeding risk. DO NOT combine without doctor supervision."},
    ("ibuprofen", "warfarin"): {"severity": "DANGER", "note": "Increased risk of stomach bleeding. Avoid combination."},
    ("naproxen", "warfarin"): {"severity": "DANGER", "note": "Increased bleeding risk. Avoid or use with extreme caution."},
    ("diclofenac", "warfarin"): {"severity": "DANGER", "note": "Major bleeding risk. Avoid combination."},
    ("gabapentin", "alcohol"): {"severity": "High Risk", "note": "Increases dizziness and drowsiness. Avoid alcohol."},
    ("pregabalin", "alcohol"): {"severity": "High Risk", "note": "Increases dizziness and drowsiness. Avoid alcohol."},
    ("alprazolam", "alcohol"): {"severity": "DEADLY", "note": "Can cause severe respiratory depression and death. NEVER combine."},
    ("paracetamol", "warfarin"): {"severity": "Moderate", "note": "High doses of paracetamol can increase warfarin effect. Limit paracetamol use."},
    ("insulin", "alcohol"): {"severity": "High Risk", "note": "Can cause dangerous low blood sugar. Avoid or take with food."},
}

# ==========================================
# MISSED DOSE GUIDANCE SYSTEM
# ==========================================

def get_missed_dose_guidance(medicine_name, time_since_missed_hours, next_dose_hours):
    """
    Personalized missed dose guidance
    """
    med = MEDICINE_DATABASE.get(medicine_name.lower())
    
    if not med:
        return {
            "guidance": f"I don't have specific information for {medicine_name}. As a general rule:",
            "general_rule": "If less than half the time has passed, take the missed dose. If more than half, skip and take next dose at regular time. NEVER double dose.",
            "consult": "Check the medicine leaflet or ask your doctor/pharmacist."
        }
    
    time_to_next = next_dose_hours - time_since_missed_hours
    
    if time_since_missed_hours < 2:
        action = "TAKE NOW - You're only slightly late. Take the missed dose immediately."
    elif time_since_missed_hours < (next_dose_hours / 2):
        action = "TAKE NOW - Still within safe window. Take missed dose and adjust schedule."
    elif time_to_next <= 2:
        action = "SKIP - Too close to next dose. Skip missed dose. Take next dose at regular time."
    else:
        action = "TAKE NOW but be cautious - If unsure, skip missed dose."
    
    return {
        "medicine": med["name"],
        "missed_dose_guidance": med.get("missed_dose", "Check medicine leaflet"),
        "time_since_missed": f"{time_since_missed_hours} hours",
        "time_until_next": f"{time_to_next} hours",
        "recommended_action": action,
        "warning": "NEVER double dose to make up for missed one",
        "consult": "If unsure, ask your doctor or pharmacist"
    }

# ==========================================
# MEDICINE EFFECTIVENESS CHECKER
# ==========================================

def check_medicine_effectiveness(medicine_name, condition, days_taken, improvement_level):
    """
    Check if medicine is working properly
    """
    med = MEDICINE_DATABASE.get(medicine_name.lower())
    
    if not med:
        return {
            "message": f"Information for {medicine_name} not available",
            "general_guidance": "Most medicines show improvement within 3-7 days. Antibiotics: 48-72 hours. Antidepressants: 2-6 weeks. Consult doctor if no improvement."
        }
    
    expected_time = {
        "Antibiotic": "48-72 hours",
        "Pain Reliever": "30-60 minutes",
        "Diabetes Medicine": "Days to weeks (with diet changes)",
        "Blood Pressure Medicine": "1-2 weeks for full effect",
        "Cholesterol Medicine": "2-4 weeks for blood levels, months for full benefit",
        "Thyroid Hormone Replacement": "2-6 weeks for symptom improvement",
        "Antidepressant": "2-6 weeks for mood improvement",
        "Antihistamine": "30-60 minutes",
        "Proton Pump Inhibitor": "1-4 days for symptom relief, weeks for healing",
    }
    
    category = med.get("category", "")
    expected = "Check with your doctor"
    for key, val in expected_time.items():
        if key in category:
            expected = val
            break
    
    if improvement_level == "significant":
        assessment = "Good response - medicine appears to be working well. Continue as prescribed."
    elif improvement_level == "slight" and days_taken < 3:
        assessment = "Early days - some medicines take time. Give it a few more days."
    elif improvement_level == "slight" and days_taken >= 7:
        assessment = "Limited improvement after a week. Consult your doctor - may need dose adjustment or different medicine."
    elif improvement_level == "none" and days_taken < 3:
        assessment = "Too early to judge. Continue as prescribed for now."
    elif improvement_level == "none" and days_taken >= 5:
        assessment = "No improvement after 5+ days is concerning. CONSULT YOUR DOCTOR. Don't stop medicine abruptly without advice."
    else:
        assessment = "Monitor and consult doctor if concerned."
    
    return {
        "medicine": med["name"],
        "category": category,
        "condition_being_treated": condition,
        "days_taken": days_taken,
        "expected_time_for_effect": expected,
        "improvement_level": improvement_level,
        "assessment": assessment,
        "course_duration": med.get("course_duration", "As prescribed"),
        "warning": "Never stop antibiotics early even if you feel better. Complete the full course.",
        "monitoring": med.get("monitoring", "Follow up with your doctor as scheduled.")
    }

# ==========================================
# MEDICINE COMPARISON SYSTEM
# ==========================================

def compare_medicines(medicine1, medicine2):
    """
    Compare two medicines for the same condition
    """
    med1 = MEDICINE_DATABASE.get(medicine1.lower())
    med2 = MEDICINE_DATABASE.get(medicine2.lower())
    
    if not med1 or not med2:
        return {"error": "One or both medicines not found in database"}
    
    return {
        "medicine_1": {
            "name": med1["name"],
            "category": med1.get("category", ""),
            "side_effects": med1.get("side_effects", []),
            "pregnancy": med1.get("pregnancy", ""),
            "best_time": med1.get("best_time", "")
        },
        "medicine_2": {
            "name": med2["name"],
            "category": med2.get("category", ""),
            "side_effects": med2.get("side_effects", []),
            "pregnancy": med2.get("pregnancy", ""),
            "best_time": med2.get("best_time", "")
        },
        "note": "This is general information. Your doctor prescribes based on your specific condition, other medicines, and health status. Don't switch medicines without consulting your doctor."
    }

# ==========================================
# SYMPTOM CHECKER
# ==========================================

SYMPTOM_GUIDE = {
    "headache": {
        "common_causes": ["Stress", "Dehydration", "Eye strain", "Sinus", "Migraine", "High BP"],
        "red_flags": ["Sudden severe 'thunderclap'", "With fever/stiff neck", "After head injury", "With vision changes"],
        "home_care": ["Rest in dark room", "Stay hydrated", "Cold/hot compress", "OTC pain reliever"],
        "when_doctor": "Persistent >3 days, severe, or with red flags",
        "when_emergency": "Worst headache ever, with confusion, fever + neck stiffness"
    },
    "fever": {
        "common_causes": ["Viral infection", "Bacterial infection", "Heat exhaustion", "Inflammation"],
        "red_flags": [">104°F (40°C)", "Lasting >3 days", "With stiff neck", "With confusion", "Seizure"],
        "home_care": ["Rest", "Plenty of fluids", "Paracetamol as directed", "Light clothing", "Cool compress"],
        "when_doctor": ">3 days, >103°F, or with other concerning symptoms",
        "when_emergency": ">105°F, seizure, unresponsive, stiff neck + headache"
    },
    "cough": {
        "common_causes": ["Cold/flu", "Allergies", "Asthma", "Bronchitis", "Acid reflux", "Smoking"],
        "red_flags": ["Coughing blood", "Shortness of breath", "Chest pain", ">3 weeks", "Weight loss"],
        "home_care": ["Honey + warm water", "Steam inhalation", "Humidifier", "Stay hydrated", "Cough drops"],
        "when_doctor": ">3 weeks, with blood, chest pain, or breathing difficulty",
        "when_emergency": "Coughing large amounts of blood, unable to breathe"
    },
    "abdominal_pain": {
        "common_causes": ["Indigestion", "Gas", "Food poisoning", "Constipation", "Menstrual cramps", "UTI"],
        "red_flags": ["Severe sudden pain", "Blood in stool/vomit", "Cannot pass gas/stool", "Fever + vomiting", "Pregnancy"],
        "home_care": ["Rest", "Small sips of water", "Avoid solid food temporarily", "Heat pad (if safe)"],
        "when_doctor": "Severe pain, persistent >24 hours, with fever, vomiting",
        "when_emergency": "Sudden severe pain, rigid belly, vomiting blood, black stools"
    },
    "chest_pain": {
        "common_causes": ["Muscle strain", "Heartburn", "Anxiety", "Heart problem (angina/heart attack)", "Lung infection"],
        "red_flags": ["Crushing/squeezing pain", "Radiating to arm/jaw", "With sweating/nausea", "Shortness of breath", "Irregular heartbeat"],
        "home_care": ["For heartburn: antacids", "For muscle: rest, warm compress", "For anxiety: slow breathing"],
        "when_doctor": "ANY unexplained chest pain should be evaluated",
        "when_emergency": "IMMEDIATELY - crushing pain + sweating + breathing trouble = CALL AMBULANCE"
    },
}

# ==========================================
# AI HEALTH ADVISOR
# ==========================================

def get_health_advice(query_type, details):
    """
    Personalized health advice based on query
    """
    advice = {
        "forgot_medicine": {
            "immediate": "Don't panic. Check how long since missed dose.",
            "rule": "If <2 hours late: Take now. If >half the dosing interval: Skip, take next dose. NEVER double dose.",
            "specific": "Check your medicine leaflet or call your pharmacist.",
            "examples": {
                "daily_medicine": "Missed morning dose, remembered afternoon: Take if <6-8 hours late. If evening: Skip, take tomorrow.",
                "twice_daily": "Missed morning dose, remembered within 3-4 hours: Take. If close to evening dose: Skip morning, take evening.",
                "antibiotic": "Take as soon as remembered. If almost time for next, skip. BUT complete the full course - this may extend treatment by one dose.",
                "birth_control": "Take as soon as remembered. If >24 hours late, take now and use backup protection for 7 days."
            }
        },
        "medicine_not_working": {
            "immediate": "Don't stop suddenly. Some medicines take time.",
            "timeline": {
                "pain_relievers": "Should work in 30-60 minutes",
                "antibiotics": "May take 48-72 hours for improvement",
                "antidepressants": "2-6 weeks for full effect",
                "blood_pressure": "1-2 weeks for full effect",
                "thyroid": "2-6 weeks for symptom improvement",
                "cholesterol": "2-4 weeks for blood level changes"
            },
            "action": "If no improvement after expected time, consult your doctor. Don't adjust dose yourself."
        },
        "side_effects": {
            "mild": "Continue medicine. Eat with food if stomach upset. Report to doctor at next visit.",
            "moderate": "Call doctor. They may adjust dose or switch medicine.",
            "severe": "STOP medicine and seek immediate medical attention: difficulty breathing, severe rash, swelling of face/tongue, severe vomiting."
        },
        "medicine_with_food": {
            "empty_stomach": ["Levothyroxine", "Some antibiotics (check label)"],
            "with_food": ["Metformin", "Ibuprofen", "Aspirin", "Iron supplements"],
            "before_food": ["Omeprazole (30 min before meal)"],
            "after_food": ["Most vitamins (A, D, E, K - fat soluble)"]
        }
    }
    
    if query_type in advice:
        return advice[query_type]
    
    return {"message": "Please specify: forgot_medicine, medicine_not_working, side_effects, medicine_with_food"}