# app/services/smart_ai.py
# SMART AI - understands any question, fixes spelling, searches knowledge

import re
from app.services.medical_knowledge import MEDICAL_KNOWLEDGE
from app.services.medical_ai_brain import MEDICINE_DATABASE
from app.services.web_search import search_medical_web
from app.services.free_ai import search_and_answer
from app.services.groq_llm import ask_groq
from app.services.local_ai import ask_local_ai

class SmartAI:
    def save_training(self, question, answer):
        """Save Q&A for future LLM training"""
        import json, os
        file_path = "user_training_data.json"
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except:
            data = []
        
        data.append({"input": question, "output": answer})
        
        # Keep last 1000 entries
        if len(data) > 1000:
            data = data[-1000:]
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    def __init__(self):
        self.knowledge = MEDICAL_KNOWLEDGE
        self.medicines = MEDICINE_DATABASE
    
    def answer(self, question):
        """Smart DIRECT answer for ANY question"""
        q = question.lower().strip()
        q = self.fix_spelling(q)
        
        # TRY GROQ FIRST for complex questions (best AI)
        if len(q.split()) > 3:  # Complex questions go to Groq
            try:
                groq_answer = ask_groq(question)
                if groq_answer and len(groq_answer) > 30:
                    # Save to training data
                    self.save_training(question, groq_answer)
                    return groq_answer
            except:
                pass
        
        # GREETINGS
        if q in ["hi", "hello", "hey", "salam", "assalam", "help"] or len(q.split()) <= 1:
            return "👋 Hello! I'm MAHFOOZ AI, your medical assistant.\n\nI can help with:\n💊 Medicines (Panadol, Brufen, Flagyl, etc.)\n🤒 Symptoms (headache, fever, stomach pain)\n🤰 Pregnancy questions\n🥗 Diet and nutrition\n⚠️ Drug interactions\n\nAsk me anything! Example: 'Can I take Panadol for headache?'"
        
        # FORGOT MEDICINE - direct advice
        if any(w in q for w in ["forgot", "missed", "skip"]) and any(w in q for w in ["medicine", "dose", "tablet", "pill", "take"]):
            if any(w in q for w in ["grandma", "grandfather", "elderly", "old", "75", "80", "70", "65", "60"]):
                return "👴 FORGOT MEDICINE - ELDERLY PATIENT:\n\n1. Take the missed dose NOW if remembered within 12 hours\n2. If more than 12 hours, SKIP missed dose, take next dose at regular time\n3. NEVER double dose - this is dangerous for elderly\n4. Write down the missed dose\n5. Use a pill organizer or phone alarm to prevent future misses\n\n⚠️ For blood pressure medicine: Missing one day is usually not dangerous, but don't make it a habit. Check BP if possible.\n\n👨‍⚕️ If confused or dizzy, contact doctor immediately."
            return "⏰ FORGOT MEDICINE:\n\n1. If remembered within 2 hours → Take NOW\n2. If almost time for next dose → SKIP missed one\n3. NEVER double dose!\n4. Take next dose at regular time\n5. Set phone alarm for future\n\n💊 For most medicines, one missed dose is not dangerous. Complete the remaining course."
        
        # ELDERLY SPECIFIC QUESTIONS
        if any(w in q for w in ["grandma", "grandfather", "elderly", "old age", "75", "80", "70"]) and any(w in q for w in ["medicine", "dose", "blood pressure", "bp", "diabetes", "sugar"]):
            return "👴 ELDERLY MEDICINE TIPS:\n\n1. Use a pill organizer (weekly box)\n2. Set daily phone alarms\n3. Keep medicine list with doses and timings\n4. Regular BP/sugar checks\n5. Doctor review every 3 months\n6. Family member should help track medicines\n\n⚠️ Elderly patients are more sensitive to missed doses and side effects. Report any dizziness, confusion, or falls to doctor."
        
        # PREGNANCY QUESTIONS - direct answers
        if any(w in q for w in ["pregnant", "pregnancy", "breastfeeding"]):
            return self.direct_pregnancy_answer(q)
        
        # MEDICINE QUESTIONS - direct answers
        if any(w in q for w in ["what is", "tell me about", "panadol", "paracetamol", "ibuprofen", "brufen", 
                                 "metformin", "aspirin", "amoxicillin", "omeprazole", "medicine", "tablet", "drug"]):
            return self.direct_medicine_answer(q)
        
        # CAN I / IS IT SAFE
        if any(w in q for w in ["can i", "is it safe", "should i take", "can we"]):
            return self.direct_safety_answer(q)
        
        # SYMPTOM QUESTIONS
        if any(w in q for w in ["pain", "hurt", "ache", "fever", "cough", "headache", "symptom", "feel", "sick"]):
            return self.direct_symptom_answer(q)
        
        # DIET / FOOD
        if any(w in q for w in ["eat", "food", "diet", "drink", "water", "nutrition"]):
            return self.direct_diet_answer(q)
        
        # Search for everything else
        return self.search_everything(q)
    
    def direct_pregnancy_answer(self, q):
        """Direct pregnancy answers"""
        if "water" in q or "drink" in q:
            return "✅ YES! Drinking water during pregnancy is ESSENTIAL. You should drink 8-12 glasses of water daily. It prevents dehydration, helps baby development, and reduces swelling. Warm water is best."
        if ("flagyl" in q or "metronidazole" in q) and ("panadol" in q or "paracetamol" in q):
            return "💊 PANADOL (Paracetamol) + FLAGYL (Metronidazole):\n\n✅ SAFE to take together.\n\nPanadol: For fever/pain. 500mg every 6 hours.\nFlagyl: Antibiotic for infections. 400mg every 8 hours with food.\n\n⚠️ Complete Flagyl course. Avoid alcohol completely with Flagyl (severe reaction).\n⚠️ Flagyl may cause metallic taste (normal).\n\nConsult doctor before combining."
            return "✅ YES! Paracetamol (Panadol) is SAFE during pregnancy for fever and pain. Take 500mg every 6 hours. Max 4000mg/day. Avoid Ibuprofen and Aspirin."
        if "flagyl" in q or "metronidazole" in q:
            return "💊 FLAGYL (Metronidazole) - Antibiotic for bacterial infections, dental infections, diarrhea. Take 400mg every 8 hours with food. 🚫 NEVER drink alcohol with Flagyl - causes severe reaction. Complete full course. Side effects: metallic taste, nausea."
        if "brufen" in q or "ibuprofen" in q:
            return "❌ NO! Ibuprofen (Brufen) is NOT safe during pregnancy, especially in the 3rd trimester. It can harm the baby. Use Paracetamol instead."
        if "exercise" in q or "walk" in q:
            return "✅ Light exercise like walking 30 minutes daily is GOOD during pregnancy. Avoid heavy lifting and high-impact sports. Always listen to your body."
        if "sleep" in q:
            return "Sleep on your LEFT SIDE during pregnancy. This improves blood flow to the baby. Use pillows between your knees for comfort. 7-9 hours recommended."
        return "During pregnancy: ✅ Paracetamol is safe. ❌ Avoid Ibuprofen, Aspirin, alcohol, smoking. 🥗 Eat healthy, drink water, take folic acid. 👨‍⚕️ Always consult your doctor."
    
    def direct_medicine_answer(self, q):
        """Direct medicine answers"""
        if ("flagyl" in q or "metronidazole" in q) and ("panadol" in q or "paracetamol" in q):
            return "💊 PANADOL (Paracetamol) + FLAGYL (Metronidazole):\n\n✅ SAFE to take together.\n\nPanadol: For fever/pain. 500mg every 6 hours.\nFlagyl: Antibiotic for infections. 400mg every 8 hours with food.\n\n⚠️ Complete Flagyl course. Avoid alcohol completely with Flagyl (severe reaction).\n⚠️ Flagyl may cause metallic taste (normal).\n\nConsult doctor before combining."
            return "💊 PANADOL (Paracetamol) - For fever, headache, body pain. Take 500mg every 6 hours. Max 4 tablets (4000mg) per day. Safe in pregnancy. Overdose can damage liver. Never take with alcohol."
        if "flagyl" in q or "metronidazole" in q:
            return "💊 FLAGYL (Metronidazole) - Antibiotic for bacterial infections, dental infections, diarrhea. Take 400mg every 8 hours with food. 🚫 NEVER drink alcohol with Flagyl - causes severe reaction. Complete full course. Side effects: metallic taste, nausea."
        if "brufen" in q or "ibuprofen" in q:
            return "💊 BRUFEN (Ibuprofen) - For pain, inflammation, fever. Take 400mg every 8 hours with food. NOT safe in pregnancy (3rd trimester). Can cause stomach ulcers. Don't take on empty stomach."
        if "metformin" in q:
            return "💊 METFORMIN - For type 2 diabetes. Take 500mg 2-3 times daily WITH meals. Side effects: nausea, diarrhea (temporary). Don't take with alcohol. Monitor blood sugar regularly."
        if "aspirin" in q or "disprin" in q:
            return "💊 ASPIRIN - For pain, fever, blood thinning. Take 300-600mg every 4-6 hours with food. NEVER give to children under 16 (Reye's syndrome risk). Can cause stomach bleeding."
        if "amoxicillin" in q:
            return "💊 AMOXICILLIN - Antibiotic for bacterial infections. Take 500mg every 8 hours. COMPLETE the full course even if feeling better. Side effects: diarrhea, rash. Tell doctor if allergic to penicillin."
        return self.search_everything(q)
    
    def direct_safety_answer(self, q):
        """Direct safety answers"""
        if "alcohol" in q and ("pregnant" in q or "pregnancy" in q):
            return "❌ NO! Alcohol is NEVER safe during pregnancy. Even small amounts can harm your baby's development. Avoid completely."
        if "smoke" in q and "pregnant" in q:
            return "❌ NO! Smoking during pregnancy is extremely harmful. It causes low birth weight, premature birth, and breathing problems in babies. Quit immediately."
        if "paracetamol" in q and "alcohol" in q:
            return "❌ DANGER! Never mix Paracetamol with alcohol. This can cause severe liver damage. Wait at least 24 hours after drinking before taking Paracetamol."
        if "ibuprofen" in q and "aspirin" in q:
            return "❌ DANGER! Never take Ibuprofen and Aspirin together. This increases stomach bleeding risk significantly. Use only one pain reliever at a time."
        return self.search_everything(q)
    
    def direct_symptom_answer(self, q):
        """Direct symptom answers"""
        if "headache" in q:
            return "🤕 HEADACHE: Rest in dark room, drink water, take Paracetamol 500mg. Apply cold compress. If severe, with fever, or lasting >3 days, see a doctor. 🚨 Worst headache ever = EMERGENCY."
        if "fever" in q:
            return "🤒 FEVER: Rest, drink plenty of water (8-10 glasses), take Paracetamol 500mg every 6 hours. Check temperature. If >103°F (39.4°C) or lasting >3 days, see a doctor. Sponge with lukewarm water."
        if "cough" in q or "cold" in q:
            return "😷 COUGH/COLD: Steam inhalation helps. Honey + warm water for cough. Drink warm fluids. Rest. Paracetamol if fever. Antibiotics DON'T work for viral colds. If coughing blood or >3 weeks, see doctor."
        if "stomach" in q or "tummy" in q:
            return "🤢 STOMACH PAIN: Rest, small sips of water. Avoid solid food for few hours. Warm compress on stomach. Antacid for acidity. 🚨 Severe pain, vomiting blood, or can't pass stool = EMERGENCY."
        if "back" in q and "pain" in q:
            return "🏥 BACK PAIN: Apply hot/cold pack. Gentle stretching. Maintain good posture. Paracetamol for pain. If pain spreads down leg, with numbness, or after injury, see a doctor."
        return self.search_everything(q)
    
    def direct_diet_answer(self, q):
        """Direct diet answers"""
        if "water" in q:
            return "💧 Drink 8-10 glasses of water daily. More in hot weather or during exercise. Water helps every organ function, prevents dehydration, and keeps skin healthy. Start your day with 2 glasses."
        if "diabetes" in q or "sugar" in q:
            return "🥗 DIABETES DIET: Eat bitter gourd, fenugreek, whole grains, green vegetables. Avoid sugar, white rice, sweets, sugary drinks. Eat small frequent meals. Exercise 30 minutes daily."
        if "weight" in q or "fat" in q:
            return "⚖️ WEIGHT LOSS: Eat more protein and vegetables. Cut sugar and processed food. Walk 45 minutes daily. Drink water before meals. Sleep 7-8 hours. Be patient - healthy weight loss is 1-2 kg per week."
        if "blood pressure" in q or "bp" in q:
            return "🫀 HIGH BP DIET: Reduce salt (less than 1 teaspoon/day). Eat bananas, potatoes, spinach for potassium. Avoid processed food, chips, pickles. Exercise regularly. Monitor BP weekly."
        return self.search_everything(q)
    
    def fix_spelling(self, text):
        """Fix common spelling mistakes"""
        fixes = {
            "panadol": "panadol", "pandol": "panadol", "panadl": "panadol",
            "paracetmol": "paracetamol", "paracetmol": "paracetamol",
            "ibupofen": "ibuprofen", "brufen": "ibuprofen",
            "metform": "metformin", "metphormin": "metformin",
            "diabtes": "diabetes", "diabetis": "diabetes", "sugar": "diabetes",
            "pragnent": "pregnant", "pregant": "pregnant", "pregnent": "pregnant",
            "headack": "headache", "hedache": "headache",
            "fevr": "fever", "fevar": "fever",
            "medcin": "medicine", "medicin": "medicine",
            "doseg": "dosage", "dosag": "dosage",
        }
        words = text.split()
        fixed = []
        for word in words:
            clean = word.strip('.,?!')
            if clean in fixes:
                fixed.append(fixes[clean])
            else:
                fixed.append(word)
        return ' '.join(fixed)
    
    def understand_intent(self, q):
        """Understand what user really wants"""
        if any(w in q for w in ["what is", "tell me about", "explain", "info"]):
            return "medicine_info"
        if any(w in q for w in ["pain", "hurt", "ache", "fever", "cough", "symptom", "feel"]):
            return "symptom"
        if any(w in q for w in ["pregnant", "pregnancy", "baby", "trimester", "due date"]):
            return "pregnancy"
        if any(w in q for w in ["emergency", "dying", "can't breathe", "heart attack", "stroke"]):
            return "emergency"
        return "general"
    
    def answer_medicine(self, q):
        """Answer medicine questions"""
        for key, info in self.medicines.items():
            if key in q or any(b.lower() in q for b in info.get('brands', [])):
                return f"{info['name']} ({', '.join(info.get('brands', [])[:2])})\n\nUsed for: {info.get('uses', ['various'])[0]}\nDose: {info.get('adult_dose', 'Consult doctor')}\nPregnancy: {info.get('pregnancy', 'Consult doctor')}\n\n⚠️ {info.get('warnings', ['Follow doctor advice'])[0]}"
        return self.search_everything(q)
    
    def answer_symptom(self, q):
        """Answer symptom questions"""
        if "headache" in q or "head" in q:
            return "For headache: Rest in dark room, drink water, take Paracetamol 500mg. If severe or lasting >3 days, see a doctor."
        if "fever" in q:
            return "For fever: Rest, drink plenty of water, take Paracetamol 500mg every 6 hours. If fever >103°F or lasting >3 days, see a doctor."
        if "stomach" in q or "tummy" in q:
            return "For stomach pain: Rest, sip water, avoid spicy food. Take antacid for acidity. If severe pain, vomiting, or blood in stool - go to emergency."
        if "cough" in q or "cold" in q:
            return "For cough/cold: Steam inhalation, honey + warm water, rest. Take Paracetamol if fever. Antibiotics don't work for viral colds."
        return self.search_everything(q)
    
    def answer_pregnancy(self, q):
        """Answer pregnancy questions"""
        return "During pregnancy: Paracetamol is safe for fever/pain. Avoid Ibuprofen, Aspirin. Always consult your doctor before taking any medicine. Take folic acid daily."
    
    def emergency_response(self, q):
        """Emergency response"""
        if "chest" in q or "heart" in q:
            return "🚨 CHEST PAIN = POSSIBLE HEART ATTACK! Call 1122 (Pakistan) or 108 (India) NOW! Chew aspirin if available. DO NOT drive."
        if "breathe" in q or "breath" in q:
            return "🚨 BREATHING EMERGENCY! Call ambulance NOW! Sit upright. This is life-threatening."
        return "🚨 MEDICAL EMERGENCY! Call 1122 (Pakistan) or 108 (India) immediately!"
    
    def search_everything(self, q):
        """Search all sources for best answer"""
        
        # Try Groq FIRST (best AI)
        try:
            groq_answer = ask_groq(q)
            if groq_answer and len(groq_answer) > 20:
                return groq_answer
        except:
            pass
        
        # Try local AI
        try:
            local_answer = ask_local_ai(q)
            if local_answer and len(local_answer) > 30:
                return local_answer
        except:
            pass
        
        # Try FREE AI model
        try:
            ai_answer = search_and_answer(q)
            if ai_answer and len(ai_answer) > 30:
                return ai_answer
        except:
            pass
        
        # Try web search
        try:
            results = search_medical_web(q)
            if results:
                return f"I found this information:\n\n{results[0]['body'][:400]}...\n\n⚠️ From medical sources. Verify with a doctor."
        except:
            pass
        
        # Try local knowledge
        for key, info in self.knowledge.items():
            if any(word in q for word in key.split('_')):
                return f"{info['name']}: {info.get('what_it_means', '')[:300]}..."
        
        # General response
        return f"I understand you're asking about '{q[:100]}'. For the most accurate answer, please ask your doctor or pharmacist. I can help with medicines, symptoms, pregnancy, and general health questions."

# Create singleton
smart_ai = SmartAI()
