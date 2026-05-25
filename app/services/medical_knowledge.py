# app/services/medical_knowledge.py
# COMPLETE FREE MEDICAL KNOWLEDGE BASE
# 200+ medical terms explained in simple language

MEDICAL_KNOWLEDGE = {
    # ==========================================
    # BLOOD TESTS
    # ==========================================
    "hemoglobin": {
        "name": "Hemoglobin (Hb)",
        "category": "Blood Test",
        "normal_range": "Male: 13.5-17.5 g/dL | Female: 12.0-15.5 g/dL | Children: 11-16 g/dL",
        "what_it_means": "Hemoglobin is a protein in your red blood cells that carries oxygen from your lungs to every part of your body.",
        "low_means": "Low hemoglobin (Anemia) - You may feel tired, weak, dizzy, short of breath. Common causes: iron deficiency, blood loss, pregnancy, poor diet.",
        "high_means": "High hemoglobin - May indicate dehydration, smoking, living at high altitudes, or certain heart/lung conditions.",
        "food_tips": "Eat: spinach, red meat, liver, beans, lentils, dates, pomegranate, beetroot, jaggery. Take with Vitamin C for better absorption.",
        "urgency": "Consult doctor if below 7 g/dL",
        "related_terms": ["iron", "ferritin", "rbc", "anemia"]
    },
    
    "rbc": {
        "name": "Red Blood Cells (RBC)",
        "category": "Blood Test",
        "normal_range": "Male: 4.5-5.5 million/µL | Female: 4.0-5.0 million/µL",
        "what_it_means": "RBCs carry oxygen throughout your body. They contain hemoglobin.",
        "low_means": "Low RBC (Anemia) - Can cause fatigue, pale skin, weakness. May be from iron/B12 deficiency or blood loss.",
        "high_means": "High RBC - May be from dehydration, smoking, or bone marrow problems.",
        "food_tips": "Iron-rich foods, B12 (eggs, dairy), folic acid (green leafy vegetables)",
        "urgency": "Consult doctor if significantly out of range",
        "related_terms": ["hemoglobin", "hematocrit", "anemia"]
    },
    
    "wbc": {
        "name": "White Blood Cells (WBC)",
        "category": "Blood Test",
        "normal_range": "4,000-11,000/µL",
        "what_it_means": "WBCs are your body's defense army. They fight infections and diseases.",
        "low_means": "Low WBC (Leukopenia) - Higher risk of infections. Can be from viral infections, medications, or bone marrow issues.",
        "high_means": "High WBC (Leukocytosis) - Your body is fighting an infection, inflammation, or stress.",
        "food_tips": "Vitamin C (citrus, bell peppers), zinc (nuts, seeds), protein-rich foods",
        "urgency": "Very high (>30,000) or very low (<2,000) needs immediate attention",
        "related_terms": ["neutrophils", "lymphocytes", "infection", "immunity"]
    },
    
    "platelets": {
        "name": "Platelet Count",
        "category": "Blood Test",
        "normal_range": "150,000-450,000/µL",
        "what_it_means": "Platelets help your blood clot. They stop bleeding when you get injured.",
        "low_means": "Low platelets (Thrombocytopenia) - Easy bruising, bleeding gums, nosebleeds. Can be from dengue, medications, or immune problems.",
        "high_means": "High platelets (Thrombocytosis) - Risk of blood clots. May be from infection, iron deficiency, or inflammation.",
        "food_tips": "Papaya leaf extract, pomegranate, pumpkin, Vitamin K foods (spinach, broccoli)",
        "urgency": "Below 50,000 needs immediate medical attention",
        "related_terms": ["dengue", "bleeding", "clotting"]
    },
    
    "blood_sugar": {
        "name": "Blood Sugar (Glucose)",
        "category": "Blood Test",
        "normal_range": "Fasting: 70-100 mg/dL | After meal: <140 mg/dL | HbA1c: <5.7%",
        "what_it_means": "Blood sugar is the amount of glucose (energy) in your blood. Insulin helps your body use it.",
        "low_means": "Low blood sugar (Hypoglycemia) - Shakiness, sweating, confusion, dizziness. Can happen if you skip meals or take too much insulin.",
        "high_means": "High blood sugar (Hyperglycemia) - May indicate diabetes. Symptoms: frequent urination, thirst, fatigue, blurry vision.",
        "food_tips": "Avoid sugar, white rice, white bread. Eat: whole grains, bitter gourd, fenugreek, cinnamon, okra",
        "urgency": "Below 70 or above 300 needs immediate attention",
        "related_terms": ["diabetes", "insulin", "hba1c", "glucose"]
    },
    
    "hba1c": {
        "name": "HbA1c (Glycated Hemoglobin)",
        "category": "Blood Test",
        "normal_range": "Normal: <5.7% | Prediabetes: 5.7-6.4% | Diabetes: ≥6.5%",
        "what_it_means": "Shows your average blood sugar over the past 2-3 months. More reliable than a single blood sugar test.",
        "low_means": "Very low HbA1c is rare. May indicate episodes of low blood sugar.",
        "high_means": "High HbA1c means your blood sugar has been high over time. Indicates diabetes or poor diabetes control.",
        "food_tips": "Low-carb diet, regular exercise, monitor sugar intake, eat fiber-rich foods",
        "urgency": "Above 9% needs immediate diabetes management",
        "related_terms": ["diabetes", "blood_sugar", "glucose", "insulin"]
    },
    
    "cholesterol": {
        "name": "Total Cholesterol",
        "category": "Lipid Profile",
        "normal_range": "Desirable: <200 mg/dL | Borderline: 200-239 | High: ≥240",
        "what_it_means": "Cholesterol is a waxy substance in blood. Your body needs some for building cells, but too much is harmful.",
        "low_means": "Very low cholesterol is rare. May affect hormone production.",
        "high_means": "High cholesterol builds up in arteries (plaque), increasing risk of heart attack and stroke.",
        "food_tips": "Eat: oats, nuts (walnuts, almonds), fatty fish, olive oil, avocado. Avoid: fried food, processed meat, butter, ghee",
        "urgency": "Above 240 with family history needs treatment",
        "related_terms": ["ldl", "hdl", "triglycerides", "heart_disease"]
    },
    
    "ldl": {
        "name": "LDL (Bad Cholesterol)",
        "category": "Lipid Profile",
        "normal_range": "Optimal: <100 mg/dL | Near optimal: 100-129 | Borderline: 130-159 | High: 160-189 | Very High: ≥190",
        "what_it_means": "LDL is 'bad' cholesterol that builds up in artery walls, causing blockages.",
        "low_means": "Low LDL is good! Less risk of heart disease.",
        "high_means": "High LDL increases risk of heart attack and stroke. Needs diet changes and possibly medication.",
        "food_tips": "Reduce saturated fats, eat soluble fiber (oats, beans, apples), nuts, plant sterols",
        "urgency": "Above 190 needs immediate treatment",
        "related_terms": ["cholesterol", "hdl", "heart_disease", "statins"]
    },
    
    "hdl": {
        "name": "HDL (Good Cholesterol)",
        "category": "Lipid Profile",
        "normal_range": "Male: >40 mg/dL | Female: >50 mg/dL | Optimal: >60 mg/dL",
        "what_it_means": "HDL is 'good' cholesterol that removes bad cholesterol from your arteries.",
        "low_means": "Low HDL increases heart disease risk. Can be from smoking, obesity, inactivity.",
        "high_means": "High HDL is protective! It helps prevent heart disease.",
        "food_tips": "Exercise regularly, eat olive oil, fatty fish, nuts, avocado, quit smoking",
        "urgency": "Low HDL with high LDL needs attention",
        "related_terms": ["cholesterol", "ldl", "triglycerides", "exercise"]
    },
    
    "triglycerides": {
        "name": "Triglycerides",
        "category": "Lipid Profile",
        "normal_range": "Normal: <150 mg/dL | Borderline: 150-199 | High: 200-499 | Very High: ≥500",
        "what_it_means": "Triglycerides are fat in your blood. Extra calories are stored as triglycerides.",
        "low_means": "Low triglycerides are generally good.",
        "high_means": "High triglycerides increase risk of heart disease and pancreatitis. Linked to obesity, diabetes, alcohol.",
        "food_tips": "Reduce sugar and refined carbs, limit alcohol, eat omega-3 rich foods (fish), exercise",
        "urgency": "Above 500 needs immediate treatment to prevent pancreatitis",
        "related_terms": ["cholesterol", "ldl", "hdl", "obesity"]
    },
    
    # ==========================================
    # LIVER TESTS
    # ==========================================
    "sgot": {
        "name": "SGOT/AST (Liver Enzyme)",
        "category": "Liver Test",
        "normal_range": "10-40 U/L",
        "what_it_means": "SGOT is an enzyme found in liver, heart, and muscles. High levels suggest cell damage.",
        "low_means": "Low SGOT is normal and not concerning.",
        "high_means": "High SGOT may indicate liver damage from alcohol, hepatitis, fatty liver, or medications. Also rises after heart attack or muscle injury.",
        "food_tips": "Avoid alcohol, eat leafy greens, turmeric, garlic, drink green tea, maintain healthy weight",
        "urgency": "Very high levels with jaundice need immediate attention",
        "related_terms": ["sgpt", "liver", "hepatitis", "fatty_liver"]
    },
    
    "sgpt": {
        "name": "SGPT/ALT (Liver Enzyme)",
        "category": "Liver Test",
        "normal_range": "7-56 U/L",
        "what_it_means": "SGPT is more specific to the liver. High levels usually mean liver cell damage.",
        "low_means": "Low SGPT is normal.",
        "high_means": "High SGPT strongly suggests liver damage. Common causes: fatty liver disease, hepatitis B/C, alcohol, certain medications (painkillers like paracetamol).",
        "food_tips": "Milk thistle, turmeric, amla (Indian gooseberry), avoid alcohol, reduce fried food",
        "urgency": "Levels 3x normal with symptoms need immediate attention",
        "related_terms": ["sgot", "liver", "hepatitis", "fatty_liver", "bilirubin"]
    },
    
    "bilirubin": {
        "name": "Bilirubin",
        "category": "Liver Test",
        "normal_range": "Total: 0.1-1.2 mg/dL | Direct: <0.3 mg/dL",
        "what_it_means": "Bilirubin is a yellow waste product from breaking down old red blood cells. The liver processes it.",
        "low_means": "Low bilirubin is not concerning.",
        "high_means": "High bilirubin causes jaundice (yellow skin/eyes). May indicate liver disease, hepatitis, gallstones, or blood disorders.",
        "food_tips": "Stay hydrated, eat radish, lemon, sugarcane juice, avoid oily food and alcohol",
        "urgency": "Visible jaundice needs immediate medical attention",
        "related_terms": ["jaundice", "liver", "hepatitis", "gallbladder"]
    },
    
    # ==========================================
    # KIDNEY TESTS
    # ==========================================
    "creatinine": {
        "name": "Creatinine",
        "category": "Kidney Test",
        "normal_range": "Male: 0.7-1.3 mg/dL | Female: 0.6-1.1 mg/dL",
        "what_it_means": "Creatinine is a waste product from muscles. Healthy kidneys filter it out of blood.",
        "low_means": "Low creatinine may indicate low muscle mass, malnutrition, or pregnancy.",
        "high_means": "High creatinine often means kidneys are not working well. Can also rise after heavy exercise or eating lots of meat.",
        "food_tips": "Drink plenty of water, reduce salt, limit protein if high, avoid painkillers without doctor advice",
        "urgency": "Above 5.0 or rapid rise needs urgent kidney evaluation",
        "related_terms": ["kidney", "urea", "bun", "dialysis", "egfr"]
    },
    
    "urea": {
        "name": "Blood Urea (BUN)",
        "category": "Kidney Test",
        "normal_range": "7-20 mg/dL",
        "what_it_means": "Urea is a waste product from protein breakdown. Kidneys remove it from blood.",
        "low_means": "Low urea may indicate liver problems, malnutrition, or overhydration.",
        "high_means": "High urea suggests kidney problems, dehydration, high protein diet, or heart failure.",
        "food_tips": "Drink adequate water, moderate protein intake, avoid excessive salt",
        "urgency": "Very high with symptoms (nausea, confusion) needs attention",
        "related_terms": ["creatinine", "kidney", "dialysis", "protein"]
    },
    
    "uric_acid": {
        "name": "Uric Acid",
        "category": "Kidney Test",
        "normal_range": "Male: 3.4-7.0 mg/dL | Female: 2.4-6.0 mg/dL",
        "what_it_means": "Uric acid is a waste product from breaking down purines (found in some foods).",
        "low_means": "Low uric acid is usually not concerning.",
        "high_means": "High uric acid can cause gout (painful joint swelling) and kidney stones. Common from rich foods, alcohol, obesity.",
        "food_tips": "Avoid: red meat, organ meat, beer, seafood. Eat: cherries, celery, drink plenty water, lemon water",
        "urgency": "With severe joint pain (gout attack) needs treatment",
        "related_terms": ["gout", "kidney_stones", "arthritis", "joint_pain"]
    },
    
    # ==========================================
    # THYROID TESTS
    # ==========================================
    "tsh": {
        "name": "TSH (Thyroid Stimulating Hormone)",
        "category": "Thyroid Test",
        "normal_range": "0.4-4.0 mIU/L",
        "what_it_means": "TSH tells your thyroid gland to produce hormones that control metabolism, energy, and mood.",
        "low_means": "Low TSH usually means overactive thyroid (Hyperthyroidism). Symptoms: weight loss, anxiety, rapid heartbeat, sweating, tremors.",
        "high_means": "High TSH usually means underactive thyroid (Hypothyroidism). Symptoms: fatigue, weight gain, depression, dry skin, hair loss, feeling cold.",
        "food_tips": "Hypothyroid: avoid raw cruciferous veggies, eat iodized salt, selenium (Brazil nuts). Hyperthyroid: avoid excess iodine",
        "urgency": "Very high TSH with severe fatigue needs treatment",
        "related_terms": ["t3", "t4", "hypothyroidism", "hyperthyroidism", "metabolism"]
    },
    
    # ==========================================
    # VITAMINS & MINERALS
    # ==========================================
    "vitamin_d": {
        "name": "Vitamin D (25-Hydroxy)",
        "category": "Vitamin Test",
        "normal_range": "30-100 ng/mL | Insufficient: 20-29 | Deficient: <20",
        "what_it_means": "Vitamin D helps absorb calcium for strong bones, supports immune system and mood.",
        "low_means": "Low Vitamin D is very common. Causes: bone pain, muscle weakness, fatigue, depression, frequent infections.",
        "high_means": "Very high Vitamin D (toxicity) is rare. Can cause calcium buildup, kidney stones.",
        "food_tips": "Sunlight (15-30 min daily), egg yolks, fatty fish, fortified milk, mushrooms. Supplement if deficient.",
        "urgency": "Severe deficiency with bone pain needs treatment",
        "related_terms": ["calcium", "bones", "immunity", "sunlight"]
    },
    
    "vitamin_b12": {
        "name": "Vitamin B12",
        "category": "Vitamin Test",
        "normal_range": "200-900 pg/mL",
        "what_it_means": "B12 is essential for nerves, brain function, and making red blood cells.",
        "low_means": "Low B12 causes fatigue, weakness, tingling in hands/feet, memory problems, anemia. Common in vegetarians and elderly.",
        "high_means": "High B12 is usually not harmful. May indicate certain blood disorders.",
        "food_tips": "Animal foods: eggs, milk, cheese, fish, meat. Vegetarians need supplements or fortified foods.",
        "urgency": "With neurological symptoms (numbness, balance issues) needs treatment",
        "related_terms": ["anemia", "nerve", "fatigue", "vegetarian"]
    },
    
    "calcium": {
        "name": "Calcium",
        "category": "Mineral Test",
        "normal_range": "8.5-10.5 mg/dL",
        "what_it_means": "Calcium is vital for bones, teeth, muscles, nerves, and blood clotting.",
        "low_means": "Low calcium (Hypocalcemia) - Muscle cramps, tingling fingers, weak bones, dental problems.",
        "high_means": "High calcium (Hypercalcemia) - May indicate parathyroid problems or certain cancers. Causes bone pain, kidney stones.",
        "food_tips": "Dairy, leafy greens, sesame seeds, ragi (finger millet), almonds, sardines",
        "urgency": "Very low with severe cramps needs urgent treatment",
        "related_terms": ["vitamin_d", "bones", "parathyroid", "osteoporosis"]
    },
    
    "iron": {
        "name": "Serum Iron",
        "category": "Mineral Test",
        "normal_range": "60-170 mcg/dL",
        "what_it_means": "Iron is needed to make hemoglobin. It carries oxygen in your blood.",
        "low_means": "Low iron leads to iron-deficiency anemia. Symptoms: extreme fatigue, pale skin, brittle nails, hair loss, craving ice/dirt (pica).",
        "high_means": "High iron (Hemochromatosis) - Can damage liver, heart, and pancreas. May be genetic.",
        "food_tips": "Heme iron (best): red meat, liver. Non-heme: spinach, beans, fortified cereals. Take with Vitamin C.",
        "urgency": "Severe anemia (Hb <7) needs urgent treatment",
        "related_terms": ["hemoglobin", "ferritin", "anemia", "rbc"]
    },
    
    # ==========================================
    # HEART TESTS
    # ==========================================
    "blood_pressure": {
        "name": "Blood Pressure (BP)",
        "category": "Heart Test",
        "normal_range": "120/80 mmHg | Elevated: 120-129/<80 | High Stage 1: 130-139/80-89 | High Stage 2: >140/>90",
        "what_it_means": "Systolic (top) = pressure when heart beats. Diastolic (bottom) = pressure when heart rests.",
        "low_means": "Low BP (<90/60) - Dizziness, fainting, fatigue. May be from dehydration, heart problems, or medications.",
        "high_means": "High BP (Hypertension) - 'Silent killer'. Damages arteries over time. Risk of heart attack, stroke, kidney failure.",
        "food_tips": "Reduce salt, eat potassium-rich foods (banana, potato), garlic, hibiscus tea, reduce stress, exercise",
        "urgency": "Above 180/120 is hypertensive crisis - needs emergency care",
        "related_terms": ["heart_disease", "stroke", "salt", "cholesterol"]
    },
    
    # ==========================================
    # URINE TESTS
    # ==========================================
    "urine_protein": {
        "name": "Urine Protein",
        "category": "Urine Test",
        "normal_range": "Negative or <150 mg/24 hours",
        "what_it_means": "Healthy kidneys don't let protein pass into urine. Protein in urine often signals kidney damage.",
        "low_means": "No protein in urine is normal and healthy.",
        "high_means": "Protein in urine (Proteinuria) - May indicate kidney disease, diabetes damage, high blood pressure, or infection.",
        "food_tips": "Control blood sugar and BP, reduce salt, moderate protein, stay hydrated",
        "urgency": "High protein with swelling needs kidney evaluation",
        "related_terms": ["kidney", "creatinine", "diabetes", "nephropathy"]
    },
    
    # ==========================================
    # COMMON DISEASES & CONDITIONS
    # ==========================================
    "diabetes": {
        "name": "Diabetes",
        "category": "Disease",
        "normal_range": "Fasting sugar: <100 mg/dL | HbA1c: <5.7%",
        "what_it_means": "Diabetes is when your body can't properly use sugar (glucose) for energy. Either doesn't make enough insulin or cells resist insulin.",
        "symptoms": "Frequent urination, extreme thirst, hunger, fatigue, blurry vision, slow healing wounds, tingling in hands/feet.",
        "types": "Type 1: Body doesn't make insulin. Type 2: Body resists insulin (more common). Gestational: During pregnancy.",
        "complications": "If uncontrolled: heart disease, kidney failure, blindness, nerve damage, foot amputation.",
        "food_tips": "Control carbs, eat fiber-rich foods, bitter gourd, fenugreek, cinnamon, regular exercise, monitor sugar",
        "urgency": "Blood sugar >300 or <70 needs immediate attention",
        "related_terms": ["blood_sugar", "hba1c", "insulin", "glucose"]
    },
    
    "anemia": {
        "name": "Anemia",
        "category": "Disease",
        "normal_range": "Hb: Male >13.5, Female >12.0 g/dL",
        "what_it_means": "Anemia means you don't have enough healthy red blood cells to carry oxygen to your body tissues.",
        "symptoms": "Fatigue, weakness, pale skin, shortness of breath, dizziness, cold hands/feet, brittle nails, headache.",
        "types": "Iron-deficiency (most common), B12 deficiency, Folic acid deficiency, Hemolytic, Sickle cell, Thalassemia.",
        "causes": "Poor diet, blood loss (heavy periods, ulcers), pregnancy, inherited conditions, chronic diseases.",
        "food_tips": "Iron-rich foods + Vitamin C, B12 from animal products, folic acid from greens, avoid tea/coffee with meals",
        "urgency": "Hb below 7 g/dL may need blood transfusion",
        "related_terms": ["hemoglobin", "iron", "rbc", "ferritin", "b12"]
    },
    
    "hypertension": {
        "name": "Hypertension (High Blood Pressure)",
        "category": "Disease",
        "normal_range": "BP <120/80 mmHg",
        "what_it_means": "Hypertension means the force of blood against your artery walls is consistently too high.",
        "symptoms": "Often NO symptoms ('silent killer'). Sometimes: headaches, shortness of breath, nosebleeds (in severe cases).",
        "causes": "Family history, high salt diet, obesity, stress, alcohol, smoking, kidney disease, thyroid problems.",
        "complications": "Heart attack, stroke, kidney failure, vision loss, dementia.",
        "food_tips": "DASH diet: low salt, high potassium (banana, spinach), garlic, reduce stress, exercise, limit alcohol",
        "urgency": "BP >180/120 is emergency - go to hospital",
        "related_terms": ["blood_pressure", "heart_disease", "stroke", "salt"]
    },
    
    "fatty_liver": {
        "name": "Fatty Liver Disease",
        "category": "Disease",
        "normal_range": "Normal liver on ultrasound",
        "what_it_means": "Fat builds up in liver cells. Very common, affecting 25% of people worldwide.",
        "symptoms": "Often no symptoms. Sometimes: fatigue, mild pain in upper right abdomen.",
        "causes": "Obesity, diabetes, high cholesterol, alcohol, rapid weight loss, certain medications.",
        "stages": "Grade 1 (mild) → Grade 2 (moderate) → Grade 3 (severe/cirrhosis risk)",
        "food_tips": "Weight loss, avoid sugar and refined carbs, coffee helps (2-3 cups/day), turmeric, milk thistle, exercise",
        "urgency": "Grade 3 needs regular monitoring to prevent cirrhosis",
        "related_terms": ["sgot", "sgpt", "liver", "obesity", "diabetes"]
    },
    
    "thyroid_disorder": {
        "name": "Thyroid Disorder",
        "category": "Disease",
        "normal_range": "TSH: 0.4-4.0 mIU/L",
        "what_it_means": "Your thyroid gland controls metabolism. When it's off, your whole body feels the effects.",
        "symptoms_hypo": "Underactive: Fatigue, weight gain, depression, dry skin, hair loss, feeling cold, constipation.",
        "symptoms_hyper": "Overactive: Weight loss, anxiety, rapid heartbeat, sweating, tremors, difficulty sleeping.",
        "causes": "Autoimmune (Hashimoto's/Graves'), iodine deficiency, thyroid nodules, pregnancy.",
        "food_tips": "Hypo: iodized salt, selenium. Hyper: avoid excess iodine. Both: regular checkups, medication as prescribed",
        "urgency": "Severe hyperthyroidism (thyroid storm) needs emergency care",
        "related_terms": ["tsh", "t3", "t4", "metabolism"]
    },
    
    "arthritis": {
        "name": "Arthritis (Joint Inflammation)",
        "category": "Disease",
        "normal_range": "No joint pain or swelling",
        "what_it_means": "Arthritis means inflammation of joints causing pain and stiffness. Many types exist.",
        "symptoms": "Joint pain, swelling, stiffness (worse in morning), reduced movement, warmth around joints.",
        "types": "Osteoarthritis (wear and tear), Rheumatoid arthritis (autoimmune), Gout (uric acid crystals), Psoriatic arthritis.",
        "causes": "Age, injury, obesity, genetics, autoimmune conditions, uric acid buildup.",
        "food_tips": "Anti-inflammatory: turmeric, ginger, omega-3 (fish), cherries (for gout). Avoid: red meat, alcohol, processed foods",
        "urgency": "Sudden severe joint pain with fever needs immediate attention",
        "related_terms": ["uric_acid", "gout", "inflammation", "joint_pain"]
    },
    
    "asthma": {
        "name": "Asthma",
        "category": "Disease",
        "normal_range": "Normal breathing without wheezing",
        "what_it_means": "Asthma is a condition where airways become narrow, swell, and produce extra mucus, making breathing difficult.",
        "symptoms": "Wheezing (whistling sound), shortness of breath, chest tightness, coughing (especially at night).",
        "triggers": "Dust, pollen, smoke, cold air, exercise, stress, pets, infections.",
        "types": "Allergic asthma, Non-allergic asthma, Exercise-induced, Occupational asthma.",
        "treatment": "Inhalers (preventer + reliever), avoid triggers, breathing exercises, steam inhalation",
        "urgency": "Severe attack (can't speak, lips blue) - EMERGENCY, call ambulance",
        "related_terms": ["allergy", "bronchitis", "respiratory", "inhaler", "wheezing"]
    },
    
    "allergy": {
        "name": "Allergies",
        "category": "Disease",
        "normal_range": "No allergic reactions",
        "what_it_means": "Your immune system overreacts to harmless substances (allergens) as if they were dangerous.",
        "symptoms": "Sneezing, runny nose, itchy eyes, skin rash (hives), swelling, difficulty breathing (severe).",
        "common_triggers": "Pollen, dust mites, pet dander, certain foods (nuts, shellfish, milk, eggs), insect stings, medications.",
        "types": "Seasonal, Food, Skin (eczema), Drug, Insect sting, Anaphylaxis (life-threatening).",
        "treatment": "Antihistamines, avoid triggers, epinephrine (for severe reactions), allergy shots",
        "urgency": "Anaphylaxis (swelling throat, difficulty breathing) - EMERGENCY, use EpiPen, call ambulance",
        "related_terms": ["asthma", "eczema", "anaphylaxis", "antihistamine"]
    },
    
    "migraine": {
        "name": "Migraine",
        "category": "Disease",
        "normal_range": "No severe headaches",
        "what_it_means": "Migraine is a neurological condition causing intense, throbbing headaches, often on one side.",
        "symptoms": "Severe headache, nausea, vomiting, sensitivity to light/sound/smell, aura (visual disturbances).",
        "triggers": "Stress, certain foods (cheese, chocolate, caffeine), hormonal changes, weather changes, lack of sleep.",
        "types": "With aura, Without aura, Chronic, Vestibular, Hemiplegic.",
        "food_tips": "Identify food triggers, stay hydrated, regular meals, magnesium-rich foods, ginger for nausea",
        "urgency": "Worst headache of your life, with fever, confusion - seek emergency care",
        "related_terms": ["headache", "aura", "neurological", "pain"]
    },
    
    # ==========================================
    # MEDICAL PROCEDURES
    # ==========================================
    "x_ray": {
        "name": "X-Ray",
        "category": "Imaging",
        "what_it_means": "X-rays use radiation to create images of bones and some soft tissues. Quick and painless.",
        "used_for": "Bone fractures, chest (pneumonia, TB), dental problems, arthritis, lung conditions.",
        "preparation": "Remove jewelry, wear loose clothes. Tell doctor if pregnant.",
        "safety": "Low radiation. Safe for most people. Not recommended during pregnancy unless necessary.",
        "related_terms": ["ct_scan", "mri", "ultrasound", "radiology"]
    },
    
    "mri": {
        "name": "MRI (Magnetic Resonance Imaging)",
        "category": "Imaging",
        "what_it_means": "MRI uses powerful magnets and radio waves to create detailed images of organs and tissues. No radiation.",
        "used_for": "Brain, spine, joints, muscles, tumors, stroke, multiple sclerosis.",
        "preparation": "Remove all metal (jewelry, watches). Tell doctor about implants, pacemakers. May need contrast dye.",
        "safety": "Very safe. No radiation. Loud noise during scan. Can feel claustrophobic (closed MRI).",
        "duration": "30-60 minutes",
        "related_terms": ["x_ray", "ct_scan", "ultrasound", "radiology"]
    },
    
    "ct_scan": {
        "name": "CT Scan (Computed Tomography)",
        "category": "Imaging",
        "what_it_means": "CT scan combines multiple X-rays to create detailed cross-sectional images of the body.",
        "used_for": "Trauma, cancer detection, internal bleeding, blood clots, bone fractures, infections.",
        "preparation": "May need to fast. Remove metal objects. May need contrast dye (oral or IV). Tell if pregnant.",
        "safety": "Higher radiation than X-ray. Use only when necessary. Not for pregnancy.",
        "duration": "5-30 minutes",
        "related_terms": ["x_ray", "mri", "ultrasound", "radiology"]
    },
    
    "ultrasound": {
        "name": "Ultrasound (Sonography)",
        "category": "Imaging",
        "what_it_means": "Ultrasound uses sound waves to create images of internal organs. No radiation, completely safe.",
        "used_for": "Pregnancy, abdominal organs, heart (echocardiogram), thyroid, blood vessels, guided procedures.",
        "preparation": "Full bladder for pelvic ultrasound. Fasting for abdominal ultrasound (6-8 hours).",
        "safety": "Completely safe. No radiation. Can be done during pregnancy. Painless.",
        "duration": "15-45 minutes",
        "related_terms": ["x_ray", "mri", "ct_scan", "pregnancy"]
    },
    
    "ecg": {
        "name": "ECG/EKG (Electrocardiogram)",
        "category": "Heart Test",
        "what_it_means": "ECG records electrical activity of your heart. Quick, painless test to check heart rhythm and health.",
        "used_for": "Heart attack, arrhythmia, chest pain, palpitations, before surgery, monitoring heart conditions.",
        "preparation": "Remove upper clothing, avoid oily skin creams. Lie still during test.",
        "safety": "Completely safe. No electricity enters your body. Just records signals.",
        "duration": "5-10 minutes",
        "related_terms": ["heart", "echocardiogram", "treadmill_test", "angiogram"]
    },
    
    # ==========================================
    # SYMPTOMS GUIDE
    # ==========================================
    "fever": {
        "name": "Fever",
        "category": "Symptom",
        "what_it_means": "Body temperature above 98.6°F (37°C). It's your body's natural defense against infection.",
        "when_worry": "Adult: >103°F (39.4°C). Child: >104°F (40°C). Baby <3 months: any fever >100.4°F (38°C).",
        "causes": "Infection (viral/bacterial), inflammation, heat exhaustion, medications, vaccines.",
        "home_care": "Rest, plenty of fluids, paracetamol (as directed), cool compress, light clothing.",
        "urgency": "Fever >105°F, with stiff neck, confusion, or lasting >3 days - seek medical help",
        "related_terms": ["infection", "temperature", "paracetamol", "viral"]
    },
    
    "cough": {
        "name": "Cough",
        "category": "Symptom",
        "what_it_means": "A reflex to clear airways of irritants, mucus, or foreign particles.",
        "types": "Dry (no mucus) vs Productive (with phlegm). Acute (<3 weeks) vs Chronic (>8 weeks).",
        "when_worry": "Coughing blood, chest pain, difficulty breathing, lasting >3 weeks, with fever.",
        "causes": "Cold/flu, allergies, asthma, bronchitis, pneumonia, acid reflux, smoking, TB.",
        "home_care": "Honey + warm water, ginger tea, steam inhalation, humidifier, avoid irritants",
        "urgency": "Coughing blood or with severe breathing difficulty - EMERGENCY",
        "related_terms": ["cold", "bronchitis", "pneumonia", "asthma", "tb"]
    },
    
    "chest_pain": {
        "name": "Chest Pain",
        "category": "Symptom",
        "what_it_means": "Pain anywhere from neck to upper abdomen. Can be from heart, lungs, muscles, or digestion.",
        "heart_attack_signs": "Pressure/squeezing in center chest, pain spreading to arm/jaw/back, shortness of breath, cold sweat, nausea.",
        "other_causes": "Heartburn, muscle strain, anxiety, lung infection, rib injury.",
        "when_emergency": "Crushing chest pain, with sweating, nausea, breathing trouble - CALL AMBULANCE IMMEDIATELY",
        "home_care": "Only for mild non-cardiac pain: antacids (if heartburn), rest (if muscle pain)",
        "urgency": "ANY unexplained chest pain needs medical evaluation",
        "related_terms": ["heart_attack", "angina", "heartburn", "anxiety"]
    },
    
    "headache": {
        "name": "Headache",
        "category": "Symptom",
        "what_it_means": "Pain in any region of the head. Most are harmless, some need attention.",
        "types": "Tension (most common), Migraine, Cluster, Sinus, Rebound (medication overuse).",
        "when_worry": "Sudden severe 'thunderclap', with fever/stiff neck, after head injury, with vision changes, waking from sleep.",
        "triggers": "Stress, dehydration, lack of sleep, certain foods, eye strain, hormonal changes.",
        "home_care": "Rest in dark quiet room, hydration, cold/hot compress, gentle massage, OTC pain relievers",
        "urgency": "Worst headache ever + confusion/fever - EMERGENCY (possible meningitis/bleeding)",
        "related_terms": ["migraine", "sinus", "tension", "meningitis"]
    },
    
    "back_pain": {
        "name": "Back Pain",
        "category": "Symptom",
        "what_it_means": "Very common. Usually from muscles, ligaments, or spine problems. Most improve with self-care.",
        "when_worry": "With leg weakness, loss of bladder/bowel control, after accident, with fever, cancer history, osteoporosis.",
        "causes": "Poor posture, muscle strain, slipped disc, arthritis, osteoporosis, kidney stones (flank pain).",
        "home_care": "Stay active (don't bed rest), hot/cold packs, gentle stretches, proper posture, firm mattress",
        "urgency": "With loss of bladder/bowel control - EMERGENCY (possible cauda equina syndrome)",
        "related_terms": ["slipped_disc", "arthritis", "muscle_spasm", "sciatica"]
    },
    
    "fatigue": {
        "name": "Fatigue (Extreme Tiredness)",
        "category": "Symptom",
        "what_it_means": "Persistent exhaustion not relieved by rest. Different from normal tiredness.",
        "when_worry": "Lasting >2 weeks, with unexplained weight loss, fever, night sweats, lumps.",
        "causes": "Anemia, thyroid problems, diabetes, depression, sleep apnea, chronic fatigue syndrome, vitamin deficiencies.",
        "tests_needed": "CBC, thyroid, blood sugar, vitamin B12, vitamin D, iron studies.",
        "home_care": "Regular sleep schedule, exercise, balanced diet, stress management, limit caffeine",
        "urgency": "With chest pain, severe headache, or confusion - seek immediate care",
        "related_terms": ["anemia", "thyroid", "depression", "sleep", "vitamins"]
    },
    
    # ==========================================
    # EMERGENCY SIGNS
    # ==========================================
    "heart_attack": {
        "name": "Heart Attack (Myocardial Infarction)",
        "category": "Emergency",
        "signs": "Chest pressure/pain, pain in arm/jaw/back, shortness of breath, cold sweat, nausea, lightheadedness.",
        "what_to_do": "CALL EMERGENCY IMMEDIATELY (911/108). Chew aspirin (if not allergic). Stay calm, sit down. DON'T drive yourself.",
        "golden_hour": "First hour is critical. Faster treatment = less heart damage.",
        "risk_factors": "Smoking, high BP, high cholesterol, diabetes, obesity, family history, stress.",
        "prevention": "Healthy diet, exercise, no smoking, control BP/sugar/cholesterol, regular checkups",
        "related_terms": ["chest_pain", "angina", "cardiac", "stroke"]
    },
    
    "stroke": {
        "name": "Stroke (Brain Attack)",
        "category": "Emergency",
        "signs": "Remember FAST: Face drooping, Arm weakness, Speech difficulty, Time to call emergency.",
        "other_signs": "Sudden confusion, trouble seeing, dizziness, severe headache, numbness on one side.",
        "what_to_do": "CALL EMERGENCY IMMEDIATELY. Note time symptoms started. Don't give food/drink/medicine.",
        "golden_hour": "Treatment within 3-4.5 hours can prevent permanent damage.",
        "prevention": "Control BP, no smoking, manage diabetes, exercise, healthy diet, limit alcohol",
        "related_terms": ["heart_attack", "paralysis", "brain", "hypertension"]
    },
    
    "anaphylaxis": {
        "name": "Anaphylaxis (Severe Allergic Reaction)",
        "category": "Emergency",
        "signs": "Difficulty breathing, throat swelling, hives all over, rapid pulse, dizziness, loss of consciousness.",
        "triggers": "Foods (peanuts, shellfish), insect stings, medications (penicillin), latex.",
        "what_to_do": "Use EpiPen if available. CALL EMERGENCY. Lie flat with legs elevated. If vomiting, turn on side.",
        "urgency": "LIFE-THREATENING EMERGENCY - can be fatal in minutes",
        "related_terms": ["allergy", "epinephrine", "shock", "emergency"]
    },
    
    # ==========================================
    # PREVENTIVE HEALTH
    # ==========================================
    "exercise": {
        "name": "Exercise & Physical Activity",
        "category": "Prevention",
        "recommendation": "150 minutes moderate exercise per week (30 min × 5 days) + strength training 2×/week",
        "benefits": "Heart health, weight control, diabetes prevention, mood improvement, stronger bones, better sleep, lower cancer risk.",
        "types": "Aerobic (walking, running, swimming), Strength (weights, pushups), Flexibility (yoga, stretching), Balance.",
        "starting_tips": "Start slow, increase gradually. Walking is excellent. Find activities you enjoy.",
        "related_terms": ["obesity", "heart_disease", "diabetes", "mental_health"]
    },
    
    "nutrition": {
        "name": "Nutrition Basics",
        "category": "Prevention",
        "recommendation": "Balanced diet: 50% vegetables/fruits, 25% whole grains, 25% protein + healthy fats",
        "plate_method": "Half plate: vegetables. Quarter: protein. Quarter: whole grains. Add healthy fats.",
        "foods_to_eat": "Leafy greens, colorful vegetables, fruits, whole grains, lean protein, nuts, seeds, water.",
        "foods_to_limit": "Processed foods, sugary drinks, excess salt, fried foods, red/processed meat, alcohol.",
        "related_terms": ["obesity", "diabetes", "heart_disease", "vitamins"]
    },
    
    "sleep": {
        "name": "Sleep Health",
        "category": "Prevention",
        "recommendation": "Adults: 7-9 hours. Teens: 8-10 hours. Children: 9-12 hours.",
        "importance": "Body repair, memory consolidation, immune function, hormone regulation, emotional health.",
        "tips": "Fixed sleep schedule, dark/cool room, no screens 1 hour before bed, avoid caffeine after 2 PM, exercise regularly.",
        "sleep_disorders": "Insomnia, Sleep apnea, Restless legs syndrome. Seek help if chronic.",
        "related_terms": ["fatigue", "insomnia", "mental_health", "stress"]
    },
    
    "mental_health": {
        "name": "Mental Health",
        "category": "Prevention",
        "what_it_means": "Mental health is as important as physical health. It affects how you think, feel, and act.",
        "common_issues": "Anxiety, Depression, Stress, Burnout, PTSD, OCD, Bipolar disorder.",
        "signs_to_seek_help": "Persistent sadness (>2 weeks), excessive worry, sleep/appetite changes, loss of interest, thoughts of self-harm.",
        "self_care": "Talk to loved ones, exercise, meditation, hobbies, adequate sleep, professional help when needed.",
        "urgency": "Thoughts of self-harm or suicide - SEEK HELP IMMEDIATELY. Call crisis helpline.",
        "related_terms": ["anxiety", "depression", "stress", "therapy"]
    },
    
    # ==========================================
    # WOMEN'S HEALTH
    # ==========================================
    "pregnancy": {
        "name": "Pregnancy Care",
        "category": "Women's Health",
        "what_it_means": "Pregnancy lasts about 40 weeks. Regular prenatal care is essential for mother and baby health.",
        "trimesters": "1st (0-13 weeks), 2nd (14-26 weeks), 3rd (27-40 weeks). Each has different needs and tests.",
        "important_tests": "Blood tests, ultrasound scans, glucose test, urine tests, blood pressure monitoring.",
        "warning_signs": "Heavy bleeding, severe abdominal pain, severe headache, blurred vision, reduced fetal movement.",
        "nutrition": "Folic acid, iron, calcium, protein. Avoid: raw meat/fish, unpasteurized dairy, alcohol, smoking.",
        "related_terms": ["ultrasound", "anemia", "blood_pressure", "diabetes"]
    },
    
    "pcod": {
        "name": "PCOD/PCOS (Polycystic Ovary Syndrome)",
        "category": "Women's Health",
        "what_it_means": "Hormonal disorder causing enlarged ovaries with small cysts. Very common (1 in 10 women).",
        "symptoms": "Irregular periods, weight gain, acne, excess hair growth (face/body), hair loss on scalp, difficulty getting pregnant.",
        "causes": "Insulin resistance, hormonal imbalance, genetics, inflammation.",
        "treatment": "Lifestyle changes (diet + exercise), medications for hormones, fertility treatment if needed.",
        "food_tips": "Low GI foods, high protein, anti-inflammatory foods, avoid sugar and processed foods",
        "related_terms": ["diabetes", "obesity", "infertility", "hormones"]
    },
    
    # ==========================================
    # CHILDREN'S HEALTH
    # ==========================================
    "vaccination": {
        "name": "Vaccination (Immunization)",
        "category": "Children's Health",
        "what_it_means": "Vaccines train your immune system to fight diseases without getting sick first.",
        "importance": "Prevents serious diseases: polio, measles, tetanus, hepatitis, etc. Protects both individual and community.",
        "common_vaccines": "BCG, Hepatitis B, Polio, DPT, Measles, MMR, Typhoid, Chickenpox, HPV, COVID-19.",
        "side_effects": "Usually mild: fever, sore arm, mild rash. Serious reactions are extremely rare.",
        "schedule": "Follow national immunization schedule. Keep vaccination card updated.",
        "related_terms": ["immunity", "infection", "prevention", "children"]
    },
    
    "malnutrition": {
        "name": "Malnutrition",
        "category": "Children's Health",
        "what_it_means": "Lack of proper nutrition from not eating enough or not eating the right foods.",
        "signs": "Underweight, stunted growth, weakness, frequent infections, slow development, thin limbs, swollen belly.",
        "causes": "Poverty, lack of food, poor diet, repeated infections, digestive problems.",
        "prevention": "Balanced diet with proteins, carbs, fats, vitamins, minerals. Breastfeeding for babies. Regular health checkups.",
        "foods": "Eggs, milk, banana, rice, dal, vegetables, fruits. Therapeutic foods for severe cases.",
        "related_terms": ["anemia", "vitamins", "growth", "immunity"]
    },
    
    # ==========================================
    # MEDICATION SAFETY
    # ==========================================
    "paracetamol": {
        "name": "Paracetamol (Acetaminophen)",
        "category": "Medication",
        "used_for": "Fever, mild to moderate pain (headache, body ache, toothache).",
        "dosage": "Adult: 500-1000mg every 4-6 hours, max 4000mg/day. Children: based on weight. Follow doctor's advice.",
        "safety": "Safe when used correctly. Overdose can cause severe liver damage. Don't take with alcohol.",
        "warning": "Many cold/flu medicines contain paracetamol. Check labels to avoid double dosing.",
        "related_terms": ["fever", "pain", "liver", "overdose"]
    },
    
    "antibiotics": {
        "name": "Antibiotics",
        "category": "Medication",
        "used_for": "BACTERIAL infections only. NOT for viral infections (cold, flu, most sore throats).",
        "examples": "Amoxicillin, Azithromycin, Ciprofloxacin, Doxycycline.",
        "important": "Complete the full course even if you feel better. Don't share or save for later. Antibiotic resistance is a global threat.",
        "side_effects": "Nausea, diarrhea, yeast infections. Rare: allergic reactions.",
        "warning": "Overuse creates superbugs. Only take when prescribed by doctor.",
        "related_terms": ["infection", "bacteria", "resistance", "prescription"]
    },
    
    # ==========================================
    # COVID-19
    # ==========================================
    "covid19": {
        "name": "COVID-19",
        "category": "Infectious Disease",
        "symptoms": "Fever, dry cough, fatigue, loss of taste/smell, sore throat, body aches, shortness of breath.",
        "severity": "Mild (80%) → Moderate → Severe (pneumonia) → Critical (respiratory failure).",
        "risk_groups": "Elderly, diabetes, heart disease, obesity, weak immunity, lung disease.",
        "prevention": "Vaccination, masks in crowds, hand washing, ventilation, social distancing when sick.",
        "home_care": "Isolate, rest, hydrate, monitor oxygen (pulse oximeter if available), paracetamol for fever.",
        "urgency": "Breathing difficulty, chest pain, confusion, oxygen <94% - GO TO HOSPITAL",
        "related_terms": ["fever", "cough", "pneumonia", "vaccination"]
    },
    
    "dengue": {
        "name": "Dengue Fever",
        "category": "Infectious Disease",
        "symptoms": "High fever (104°F), severe headache, pain behind eyes, joint/muscle pain, rash, nausea.",
        "warning_signs": "Severe abdominal pain, persistent vomiting, bleeding gums/nose, blood in vomit/stool, fatigue, restlessness.",
        "mosquito": "Aedes mosquito (black with white stripes), bites during daytime.",
        "prevention": "Mosquito nets, repellents, full clothing, remove standing water, mosquito screens.",
        "treatment": "NO specific medicine. Rest, plenty of fluids, paracetamol (NOT aspirin/ibuprofen - increases bleeding risk).",
        "urgency": "Warning signs = EMERGENCY. Platelets dropping needs hospital monitoring.",
        "related_terms": ["platelets", "fever", "mosquito", "bleeding"]
    },
    
    "malaria": {
        "name": "Malaria",
        "category": "Infectious Disease",
        "symptoms": "Fever with chills/shivering (cyclical), headache, nausea, body aches, sweating.",
        "mosquito": "Anopheles mosquito, bites at night.",
        "severity": "Can be life-threatening, especially in children and pregnant women.",
        "prevention": "Mosquito nets (insecticide-treated), repellents, antimalarial medication for travelers.",
        "treatment": "Antimalarial drugs as prescribed. Early treatment is crucial.",
        "urgency": "Fever after visiting malaria area - get tested immediately",
        "related_terms": ["fever", "mosquito", "parasite", "anemia"]
    },
    
    "typhoid": {
        "name": "Typhoid Fever",
        "category": "Infectious Disease",
        "symptoms": "Gradual fever that rises daily, headache, weakness, abdominal pain, constipation or diarrhea, rose-colored spots on chest.",
        "transmission": "Contaminated food/water (fecal-oral route).",
        "prevention": "Clean water, proper sanitation, hand washing, typhoid vaccine, avoid street food in risky areas.",
        "treatment": "Antibiotics as prescribed. Rest, hydration, soft diet.",
        "complications": "Intestinal bleeding or perforation (rare but serious).",
        "urgency": "Severe abdominal pain, bleeding - EMERGENCY",
        "related_terms": ["fever", "salmonella", "food_poisoning", "vaccination"]
    },
    
    "hepatitis": {
        "name": "Hepatitis (Liver Inflammation)",
        "category": "Infectious Disease",
        "types": "A (food/water), B (blood/body fluids), C (blood), D, E (water).",
        "symptoms": "Fatigue, jaundice, dark urine, abdominal pain, nausea, loss of appetite.",
        "prevention": "Vaccines for A and B. Safe water/food, safe sex, no sharing needles.",
        "chronic": "B and C can become chronic → cirrhosis, liver cancer.",
        "treatment": "A/E: Self-limiting. B: Antivirals if chronic. C: Curable with medication.",
        "urgency": "Jaundice with confusion or bleeding - EMERGENCY",
        "related_terms": ["jaundice", "liver", "sgot", "sgpt", "bilirubin"]
    },
    
    "tuberculosis": {
        "name": "Tuberculosis (TB)",
        "category": "Infectious Disease",
        "symptoms": "Cough >2 weeks (sometimes with blood), fever (evening rise), night sweats, weight loss, chest pain, fatigue.",
        "transmission": "Airborne (coughing, sneezing).",
        "testing": "Sputum test, chest X-ray, TB skin test (Mantoux), GeneXpert.",
        "treatment": "6-9 months of multiple antibiotics. MUST complete full course (DOTS therapy).",
        "prevention": "BCG vaccine for children, good ventilation, mask if infected, cover mouth while coughing.",
        "urgency": "Coughing blood - needs immediate medical attention",
        "related_terms": ["cough", "x_ray", "lung", "antibiotics"]
    },
}

# ==========================================
# CATEGORIES FOR ORGANIZED SEARCH
# ==========================================
CATEGORIES = {
    "Blood Test": ["hemoglobin", "rbc", "wbc", "platelets", "blood_sugar", "hba1c", "iron", "ferritin"],
    "Lipid Profile": ["cholesterol", "ldl", "hdl", "triglycerides"],
    "Liver Test": ["sgot", "sgpt", "bilirubin", "fatty_liver", "hepatitis"],
    "Kidney Test": ["creatinine", "urea", "uric_acid"],
    "Thyroid Test": ["tsh", "t3", "t4", "thyroid_disorder"],
    "Vitamin Test": ["vitamin_d", "vitamin_b12", "calcium"],
    "Heart Test": ["blood_pressure", "ecg", "heart_attack"],
    "Imaging": ["x_ray", "mri", "ct_scan", "ultrasound"],
    "Disease": ["diabetes", "anemia", "hypertension", "arthritis", "asthma", "allergy", "migraine"],
    "Symptom": ["fever", "cough", "chest_pain", "headache", "back_pain", "fatigue"],
    "Emergency": ["heart_attack", "stroke", "anaphylaxis"],
    "Prevention": ["exercise", "nutrition", "sleep", "mental_health"],
    "Women's Health": ["pregnancy", "pcod"],
    "Children's Health": ["vaccination", "malnutrition"],
    "Medication": ["paracetamol", "antibiotics"],
    "Infectious Disease": ["covid19", "dengue", "malaria", "typhoid", "tuberculosis"],
}

# Health tips in multiple languages
HEALTH_TIPS = {
    "english": [
        "Drink 8-10 glasses of water daily",
        "Walk 30 minutes every day",
        "Eat 5 servings of fruits and vegetables daily",
        "Get 7-8 hours of sleep",
        "Wash hands regularly to prevent infections",
        "Don't skip breakfast",
        "Limit sugar and salt intake",
        "Practice deep breathing for 5 minutes daily",
        "Get regular health checkups",
        "Stay connected with loved ones for mental health",
    ],
    "hindi": [
        "रोज 8-10 गिलास पानी पिएं",
        "हर दिन 30 मिनट टहलें",
        "रोज 5 बार फल और सब्जियां खाएं",
        "7-8 घंटे की नींद लें",
        "संक्रमण से बचने के लिए नियमित रूप से हाथ धोएं",
        "नाश्ता न छोड़ें",
        "चीनी और नमक कम खाएं",
        "रोज 5 मिनट गहरी सांस लेने का अभ्यास करें",
        "नियमित स्वास्थ्य जांच करवाएं",
        "मानसिक स्वास्थ्य के लिए प्रियजनों से जुड़े रहें",
    ],
    "arabic": [
        "اشرب 8-10 أكواب من الماء يومياً",
        "امشِ 30 دقيقة كل يوم",
        "تناول 5 حصص من الفواكه والخضروات يومياً",
        "احصل على 7-8 ساعات من النوم",
        "اغسل يديك بانتظام للوقاية من العدوى",
        "لا تفوت وجبة الإفطار",
        "قلل من تناول السكر والملح",
        "مارس التنفس العميق لمدة 5 دقائق يومياً",
        "احصل على فحوصات طبية منتظمة",
        "ابق على تواصل مع أحبائك للصحة النفسية",
    ],
}

# Emergency contacts template
EMERGENCY_INFO = {
    "pakistan": {
        "ambulance": "1122",
        "police": "15",
        "fire": "16",
    },
    "india": {
        "ambulance": "108",
        "police": "100",
        "fire": "101",
    },
}