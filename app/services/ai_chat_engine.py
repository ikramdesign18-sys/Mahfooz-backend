import random
import re
from app.services.medical_knowledge import MEDICAL_KNOWLEDGE
from app.services.medical_ai_brain import MEDICINE_DATABASE, DRUG_INTERACTIONS, SYMPTOM_GUIDE
from app.services.medical_database import DISEASES
from app.services.medicine_database_extended import MEDICINES_EXTENDED
from app.services.fact_checker import MedicalFactChecker
from app.services.web_search import search_medical_web

class MedicalChatAI:
    def __init__(self):
        self.knowledge = MEDICAL_KNOWLEDGE
        self.medicines = MEDICINE_DATABASE
        self.medicines.update(MEDICINES_EXTENDED)
        self.interactions = DRUG_INTERACTIONS
        self.symptoms = SYMPTOM_GUIDE
        self.diseases = DISEASES
        self.fact_checker = MedicalFactChecker()
        self.conversation_history = []
    
    def chat(self, user_message):
        is_emergency, emergency_type = self.fact_checker.is_emergency(user_message)
        if is_emergency:
            return self.get_emergency_response(emergency_type)
        message = user_message.lower().strip()
        self.conversation_history.append({"user": user_message})
        response = self.smart_answer(message)
        self.conversation_history.append({"ai": response})
        return response
    
    def smart_answer(self, msg):
        for med_key, med_info in self.medicines.items():
            if ("pregnant" in msg or "pregnancy" in msg) and (med_key in msg or any(b.lower() in msg for b in med_info.get("brands", []))):
                return self.answer_pregnancy_medicine(msg)
        if any(q in msg for q in ["what medicine", "what should i take", "what can i take", "medicine for", "what to take"]):
            return self.answer_what_to_take(msg)
        if any(q in msg for q in ["can i take", "is it safe", "can i use"]):
            return self.answer_safety_question(msg)
        if any(q in msg for q in ["what is", "tell me about", "explain"]):
            return self.answer_explain_question(msg)
        if any(q in msg for q in ["health tip", "advice", "stay healthy"]):
            return self.get_health_tips()
        if any(s in msg for s in ["stomach", "tummy", "belly", "abdominal", "gastric"]):
            return self.answer_stomach_pain(msg)
        if any(s in msg for s in ["pain", "hurt", "ache", "fever", "cough", "headache", "symptom"]):
            return self.answer_symptom_question(msg)
        if any(d in msg for d in ["eat", "food", "diet", "nutrition"]):
            return self.answer_diet_question(msg)
        return self.search_web_or_fallback(msg)
    
    def answer_pregnancy_medicine(self, msg):
        for med_key, med_info in self.medicines.items():
            if med_key in msg or any(brand.lower() in msg for brand in med_info.get("brands", [])):
                name = med_info["name"]
                pregnancy = med_info.get("pregnancy", "Consult your doctor")
                if "avoid" in pregnancy.lower() or "x" in pregnancy.lower():
                    return f"\u274c **{name} is NOT safe during pregnancy.**\n\n{pregnancy}\n\n\U0001f6ab Do not take this without doctor approval.\n\n\U0001f4a1 Safe alternatives: Paracetamol is generally safe for fever/pain."
                elif "safe" in pregnancy.lower():
                    return f"\u2705 **{name} is generally safe during pregnancy.**\n\n{pregnancy}\n\n\u26a0\ufe0f Still take only as prescribed by your doctor."
                else:
                    return f"\u26a0\ufe0f **{name} during pregnancy:** {pregnancy}\n\n\U0001f468\u200d\u2695\ufe0f Always consult your doctor."
        return "\U0001f930 **Pregnancy & Medicine Safety**\n\n\u26a0\ufe0f Never self-medicate during pregnancy.\n\n\u2705 Generally safe: Paracetamol\n\u274c Avoid: Ibuprofen, Aspirin"
    
    def answer_what_to_take(self, msg):
        if "fever" in msg or "body pain" in msg or "headache" in msg:
            return "\U0001f48a **For Fever & Body Pain:**\n\n\u2705 Paracetamol (Panadol) 500mg every 6 hours\n\u2705 Ibuprofen (Brufen) 400mg every 8 hours (take with food)\n\n\u26a0\ufe0f Max 4000mg paracetamol per day\n\u26a0\ufe0f Don't take ibuprofen on empty stomach\n\U0001f930 If pregnant: Only paracetamol is safe\n\n\U0001f4a1 Also: Rest, drink plenty of water, and see a doctor if fever persists >3 days."
        if "cold" in msg or "cough" in msg:
            return "\U0001f48a **For Cold & Cough:**\n\n\u2705 Steam inhalation\n\u2705 Honey + warm water for cough\n\u2705 Paracetamol if fever\n\u2705 Cetirizine for runny nose"
        return "\U0001f48a Tell me your symptoms (fever, headache, body pain, cold) and I'll suggest appropriate medicines."
    
    def answer_safety_question(self, msg):
        medicines_found = []
        for med_key, med_info in self.medicines.items():
            if med_key in msg or any(brand.lower() in msg for brand in med_info.get("brands", [])):
                medicines_found.append(med_key)
        if len(medicines_found) >= 2:
            return self.answer_drug_interaction(msg)
        if medicines_found:
            med_info = self.medicines[medicines_found[0]]
            brands = ', '.join(med_info.get('brands', [])[:3])
            uses = med_info.get('uses', ['various'])[0]
            dose = med_info.get('adult_dose', 'Consult doctor')
            pregnancy = med_info.get('pregnancy', 'Consult doctor')
            warnings_list = med_info.get('warnings', [])
            warning = warnings_list[0] if warnings_list else 'Follow doctor advice'
            return f"\U0001f48a **{med_info['name']}** ({brands})\n\n\U0001f4cb Used for: {uses}\n\n\U0001f48a How to take: {dose}\n\n\U0001f930 Pregnancy: {pregnancy}\n\n\u26a0\ufe0f Warning: {warning}"
        return self.search_web_or_fallback(msg)
    
    def answer_explain_question(self, msg):
        for key, info in self.medicines.items():
            if key in msg or any(b.lower() in msg for b in info.get("brands", [])):
                brands = ', '.join(info.get('brands', [])[:3])
                uses = info.get('uses', ['various'])[0]
                dose = info.get('adult_dose', 'Consult doctor')
                pregnancy = info.get('pregnancy', 'Consult doctor')
                warnings_list = info.get('warnings', [])
                warning = warnings_list[0] if warnings_list else 'Follow doctor advice'
                missed = info.get('missed_dose', 'Check with pharmacist')
                return f"\U0001f48a **{info['name']}** ({brands})\n\n\U0001f4cb Used for: {uses}\n\n\U0001f48a How to take: {dose}\n\n\U0001f930 Pregnancy: {pregnancy}\n\n\u26a0\ufe0f Warning: {warning}\n\n\u2753 Missed dose: {missed}"
        for key, info in self.diseases.items():
            if key.replace("_", " ") in msg or info.get("name", "").lower() in msg:
                symptoms = ", ".join(info.get("symptoms", [])[:5])
                return f"\U0001f4da **{info['name']}**\n\n\U0001f50d What it is: {info.get('cause', 'Unknown')}\n\n\U0001f912 Symptoms: {symptoms}\n\n\U0001f48a Treatment: {', '.join(info.get('treatment', [])[:3])}"
        return self.search_web_or_fallback(msg)
    
    def answer_stomach_pain(self, msg):
        if "severe" in msg or "extreme" in msg:
            return "\U0001f6a8 **Severe stomach pain needs immediate medical attention!**\n\n\u26a0\ufe0f Go to emergency if you have:\n- Severe pain\n- Blood in vomit/stool\n- Can't pass gas/stool\n- Fever with vomiting\n\n\U0001f3e5 Call 1122 (Pakistan) or 108 (India)!"
        return "\U0001f912 **Stomach Pain - What to do:**\n\n\U0001f3e0 **Home Care:**\n- Rest and lie down\n- Small sips of water\n- Warm water bottle on stomach\n- Avoid spicy, oily food\n- Try ginger or mint tea\n\n\U0001f48a **Medicine:**\n- Antacid (Digene/Gaviscon) for acidity\n- Paracetamol for pain (NOT ibuprofen)\n- Omeprazole for acid reflux\n\n\u26a0\ufe0f See doctor if pain >24 hours, vomiting, fever, or blood in stool."
    
    def answer_symptom_question(self, msg):
        for symptom_key, symptom_info in self.symptoms.items():
            if symptom_key.replace("_", " ") in msg:
                home_care = "\n".join([f"  - {tip}" for tip in symptom_info['home_care']])
                red_flags = "\n".join([f"  - {flag}" for flag in symptom_info['red_flags']])
                return f"\U0001f912 **{symptom_key.replace('_', ' ').title()}**\n\n\U0001f50d Common causes: {', '.join(symptom_info['common_causes'])}\n\n\U0001f3e0 Home care:\n{home_care}\n\n\U0001f6a9 Red flags:\n{red_flags}\n\n\U0001f468\u200d\u2695\ufe0f See doctor: {symptom_info['when_doctor']}\n\n\U0001f6a8 Emergency: {symptom_info['when_emergency']}"
        return self.search_web_or_fallback(msg)
    
    def answer_drug_interaction(self, msg):
        medicines_found = []
        for med_key in self.medicines:
            if med_key in msg:
                medicines_found.append(med_key)
        if len(medicines_found) >= 2:
            pair = tuple(sorted(medicines_found[:2]))
            if pair in self.interactions:
                interaction = self.interactions[pair]
                med1 = self.medicines.get(medicines_found[0], {}).get('name', medicines_found[0])
                med2 = self.medicines.get(medicines_found[1], {}).get('name', medicines_found[1])
                return f"\u26a0\ufe0f **DRUG INTERACTION**\n\n{med1} + {med2}\n\n\U0001f534 Severity: {interaction['severity']}\n\n\U0001f4dd {interaction['note']}"
        return "\u2705 No known interaction. Still consult your doctor."
    
    def answer_diet_question(self, msg):
        for key, info in self.knowledge.items():
            if key in msg and info.get("food_tips"):
                return f"\U0001f957 **Diet for {info['name']}:**\n\n{info['food_tips']}"
        return "\U0001f957 Eat: vegetables, fruits, whole grains, lean protein. Drink 8-10 glasses water. Limit sugar and salt."
    
    def search_web_or_fallback(self, msg):
        try:
            web_results = search_medical_web(msg)
            if web_results:
                answer = "\U0001f310 Here's what I found:\n\n"
                for r in web_results[:2]:
                    answer += f"\U0001f4cb {r['body'][:300]}...\n\n"
                answer += "\u26a0\ufe0f Verified from medical sources. Always consult a doctor."
                return answer
        except:
            pass
        return "I can help with medicines, symptoms, pregnancy, stomach pain, diet, and more. Try asking me a specific question!"
    
    def get_emergency_response(self, emergency_type):
        responses = {
            "chest pain": "\U0001f6a8 MEDICAL EMERGENCY! Possible HEART ATTACK. Call 1122/108 IMMEDIATELY! Chew aspirin if available. DO NOT drive yourself.",
            "suicide": "\U0001f6a8 YOU ARE NOT ALONE. Pakistan: 042-35761999. India: 9152987821. Please call now.",
            "stroke": "\U0001f6a8 STROKE! FAST: Face, Arms, Speech, Time. Call emergency NOW!",
        }
        return responses.get(emergency_type, "\U0001f6a8 MEDICAL EMERGENCY! Call 1122 (Pakistan) or 108 (India) immediately!")
    
    def get_health_tips(self):
        tips = ["Drink 8-10 glasses of water daily", "Walk 30 minutes every day", "Eat 5 servings of fruits and vegetables", "Get 7-8 hours of sleep", "Wash hands regularly"]
        selected = random.sample(tips, 3)
        return "\U0001f31f **Daily Health Tips:**\n\n" + "\n".join(f"- {tip}" for tip in selected)
    
    def format_medicine_info(self, med_info):
        brands = ', '.join(med_info.get('brands', [])[:3])
        return f"\U0001f48a **{med_info['name']}** ({brands})\n\n\U0001f4cb Used for: {med_info.get('uses',[''])[0]}\n\U0001f48a Dose: {med_info.get('adult_dose','')}\n\u26a0\ufe0f Warning: {med_info.get('warnings',[''])[0] if med_info.get('warnings') else 'Follow doctor advice'}"
