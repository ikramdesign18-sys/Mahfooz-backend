# app/services/fact_checker.py
# Medical Fact Verification System
# Prevents AI from giving wrong medical advice

import re

# Verified medical facts that MUST be correct
VERIFIED_FACTS = {
    "paracetamol_max_dose": "4000mg per day for adults. Overdose causes liver damage.",
    "aspirin_children": "NEVER give aspirin to children under 16. Risk of Reye's syndrome.",
    "pregnancy_alcohol": "NO amount of alcohol is safe during pregnancy.",
    "antibiotic_course": "ALWAYS complete the full antibiotic course even if feeling better.",
    "blood_pressure_crisis": "BP above 180/120 is a hypertensive crisis. Seek emergency care.",
    "insulin_missed": "NEVER double dose insulin. Check blood sugar and call doctor.",
    "chest_pain_emergency": "ANY crushing chest pain with sweating/nausea = CALL EMERGENCY.",
    "allergic_swelling": "Swelling of face/tongue/throat after medicine = EMERGENCY.",
    "vaccine_myth": "Vaccines DO NOT cause autism. This is scientifically proven false.",
    "antibiotics_virus": "Antibiotics DO NOT work against viruses (cold, flu, COVID).",
}

# Dangerous medical advice patterns to BLOCK
DANGEROUS_PATTERNS = [
    r"stop taking (your|the) (medicine|medication|pills|tablets)",
    r"don'?t (need|take) (your|the) (medicine|medication)",
    r"skip (your|the) (dose|medicine|medication)",
    r"double (your|the) (dose|dosage)",
    r"take more than (prescribed|recommended)",
    r"alcohol (is|are|being) (safe|okay|fine) with",
    r"natural (remedy|cure) (instead|replaces) (medicine|medication)",
]

class MedicalFactChecker:
    def __init__(self):
        self.facts = VERIFIED_FACTS
        self.dangerous_patterns = DANGEROUS_PATTERNS
    
    def check_response(self, ai_response, user_query):
        """
        Verify AI response doesn't contain dangerous advice
        Returns: (is_safe, warning_message)
        """
        response_lower = ai_response.lower()
        warnings = []
        
        # Check for dangerous patterns
        for pattern in self.dangerous_patterns:
            if re.search(pattern, response_lower):
                warnings.append("⚠️ Response contains potentially dangerous medical advice")
        
        # Check for missing safety disclaimers
        if "consult" not in response_lower and "doctor" not in response_lower:
            if len(ai_response) > 100:  # Only warn for substantial responses
                warnings.append("⚠️ Response missing 'consult doctor' disclaimer")
        
        # Check for specific dangerous claims
        dangerous_claims = {
            "not need": "suggesting medicine is not needed",
            "stop taking": "suggesting to stop medication",
            "natural cure": "suggesting natural remedies replace medicine",
        }
        
        for phrase, warning in dangerous_claims.items():
            if phrase in response_lower:
                warnings.append(f"⚠️ Response may be {warning}")
        
        if warnings:
            return False, "\n".join(warnings)
        
        return True, "Response passed safety check"
    
    def add_safety_disclaimer(self, response):
        """
        Add safety disclaimer if missing
        """
        if "consult" not in response.lower() and "doctor" not in response.lower():
            response += "\n\n⚠️ Always consult a doctor for medical advice. This is educational information only."
        
        return response
    
    def get_verified_fact(self, fact_key):
        """
        Get a verified medical fact
        """
        return self.facts.get(fact_key, "Fact not found in verified database")
    
    def is_emergency(self, user_query):
        """
        Check if query contains emergency keywords
        """
        emergency_keywords = [
            "chest pain", "can't breathe", "heart attack", "stroke",
            "severe bleeding", "unconscious", "suicide", "poison",
            "overdose", "seizure", "anaphylaxis", "allergic reaction",
            "kill myself", "want to die", "end my life", "suicidal",
            "self harm", "self-harm", "hurting myself"
        ]
        
        query_lower = user_query.lower()
        for keyword in emergency_keywords:
            if keyword in query_lower:
                return True, keyword
        
        return False, None