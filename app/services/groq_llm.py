import os
from dotenv import load_dotenv
load_dotenv()
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

def ask_groq(question):
    """Best AI - Llama 3 70B - understands ANYTHING"""
    if not GROQ_API_KEY:
        return None
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "You are MAHFOOZ AI for a free charity medical app in Pakistan/India. Users are poor people who can't afford doctors. Answer in simple English with some Urdu words. Include: medicine uses, dosage, side effects, pregnancy safety, when to see doctor, emergency numbers (Pakistan 1122, India 108). Be compassionate. Keep under 250 words."
                },
                {"role": "user", "content": question}
            ],
            temperature=0.3,
            max_tokens=500,
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq error: {e}")
        return None
