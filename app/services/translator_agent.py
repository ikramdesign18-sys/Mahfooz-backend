# app/services/translator_agent.py
# Translator Agent - Converts medical jargon to simple language
# Supports: English, Urdu, Hindi, Arabic

# Simple translations for common medical terms
MEDICAL_TRANSLATIONS = {
    "urdu": {
        "medicine": "دوا",
        "doctor": "ڈاکٹر",
        "hospital": "ہسپتال",
        "pain": "درد",
        "fever": "بخار",
        "headache": "سر درد",
        "blood": "خون",
        "heart": "دل",
        "sugar": "شوگر",
        "pressure": "پریشر",
        "tablet": "گولی",
        "dose": "خوراک",
        "morning": "صبح",
        "evening": "شام",
        "night": "رات",
        "food": "کھانا",
        "water": "پانی",
        "sleep": "نیند",
        "exercise": "ورزش",
        "emergency": "ہنگامی",
        "call": "کال کریں",
        "help": "مدد",
    },
    "hindi": {
        "medicine": "दवा",
        "doctor": "डॉक्टर",
        "hospital": "अस्पताल",
        "pain": "दर्द",
        "fever": "बुखार",
        "headache": "सिर दर्द",
        "blood": "खून",
        "heart": "दिल",
        "sugar": "शुगर",
        "pressure": "प्रेशर",
        "tablet": "गोली",
        "dose": "खुराक",
        "morning": "सुबह",
        "evening": "शाम",
        "night": "रात",
        "food": "खाना",
        "water": "पानी",
        "sleep": "नींद",
        "exercise": "व्यायाम",
        "emergency": "आपातकाल",
        "call": "कॉल करें",
        "help": "मदद",
    },
    "arabic": {
        "medicine": "دواء",
        "doctor": "طبيب",
        "hospital": "مستشفى",
        "pain": "ألم",
        "fever": "حمى",
        "headache": "صداع",
        "blood": "دم",
        "heart": "قلب",
        "sugar": "سكر",
        "pressure": "ضغط",
        "tablet": "حبة",
        "dose": "جرعة",
        "morning": "صباح",
        "evening": "مساء",
        "night": "ليل",
        "food": "طعام",
        "water": "ماء",
        "sleep": "نوم",
        "exercise": "رياضة",
        "emergency": "طوارئ",
        "call": "اتصل",
        "help": "مساعدة",
    },
}

class TranslatorAgent:
    def __init__(self):
        self.translations = MEDICAL_TRANSLATIONS
    
    def simplify_medical_text(self, text, language="english"):
        """
        Convert complex medical text to simple language
        """
        # Replace complex medical terms
        simplifications = {
            "myocardial infarction": "heart attack",
            "cerebrovascular accident": "stroke",
            "hypertension": "high blood pressure",
            "hyperglycemia": "high blood sugar",
            "hypoglycemia": "low blood sugar",
            "pyrexia": "fever",
            "cephalalgia": "headache",
            "dyspnea": "difficulty breathing",
            "edema": "swelling",
            "erythema": "redness",
            "pruritus": "itching",
            "nausea": "feeling sick",
            "emesis": "vomiting",
            "diarrhea": "loose motions",
            "constipation": "difficulty passing stool",
            "insomnia": "difficulty sleeping",
            "fatigue": "extreme tiredness",
            "anorexia": "loss of appetite",
            "tachycardia": "fast heartbeat",
            "bradycardia": "slow heartbeat",
            "hemorrhage": "bleeding",
            "neoplasm": "tumor",
            "benign": "not cancer",
            "malignant": "cancerous",
            "metastasis": "cancer spread",
            "prognosis": "expected outcome",
            "contraindication": "reason not to take",
            "adverse reaction": "bad side effect",
            "therapeutic": "healing/treatment",
            "prophylaxis": "prevention",
        }
        
        text_lower = text.lower()
        for complex_term, simple_term in simplifications.items():
            if complex_term in text_lower:
                text = text.replace(complex_term, f"{complex_term} ({simple_term})")
                text = text.replace(complex_term.title(), f"{complex_term.title()} ({simple_term})")
        
        # Translate if needed
        if language != "english" and language in self.translations:
            for eng_word, translated in self.translations[language].items():
                # Add translation after English word
                if eng_word in text_lower:
                    text = re.sub(
                        r'\b' + eng_word + r'\b',
                        f"{eng_word} ({translated})",
                        text,
                        flags=re.IGNORECASE
                    )
        
        return text
    
    def get_welcome_message(self, language="english"):
        """Get welcome message in different languages"""
        messages = {
            "english": "👋 Welcome to MAHFOOZ! I'm your free medical AI assistant. Ask me anything about medicines, symptoms, or health.",
            "urdu": "👋 MAHFOOZ میں خوش آمدید! میں آپ کا مفت طبی اسسٹنٹ ہوں۔ دوائیوں، علامات یا صحت کے بارے میں پوچھیں۔",
            "hindi": "👋 MAHFOOZ में आपका स्वागत है! मैं आपका मुफ्त चिकित्सा सहायक हूं। दवाओं, लक्षणों या स्वास्थ्य के बारे में पूछें।",
            "arabic": "👋 مرحبا بكم في MAHFOOZ! أنا مساعدكم الطبي المجاني. اسألوني عن الأدوية أو الأعراض أو الصحة.",
        }
        return messages.get(language, messages["english"])
    
    def get_emergency_message(self, language="english"):
        """Get emergency message in different languages"""
        messages = {
            "english": "🚨 MEDICAL EMERGENCY! Call ambulance NOW! Pakistan: 1122, India: 108",
            "urdu": "🚨 طبی ایمرجنسی! فوری ایمبولینس کو کال کریں! پاکستان: 1122، بھارت: 108",
            "hindi": "🚨 चिकित्सा आपातकाल! तुरंत एम्बुलेंस बुलाएं! पाकिस्तान: 1122, भारत: 108",
            "arabic": "🚨 حالة طبية طارئة! اتصل بالإسعاف الآن! باكستان: 1122، الهند: 108",
        }
        return messages.get(language, messages["english"])

import re