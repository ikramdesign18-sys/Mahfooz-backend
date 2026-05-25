# app/services/deepseek_ai.py
# DEEPSEEK AI - World-class understanding, searches everything
# Uses OpenRouter FREE API - no credit card needed

import requests
import json

def ask_deepseek(question):
    """
    Ask DeepSeek AI - understands any question, gives best answer
    Uses OpenRouter FREE tier
    """
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "HTTP-Referer": "https://mahfooz.app",
                "X-Title": "MAHFOOZ Medical Wallet",
            },
            json={
                "model": "deepseek/deepseek-r1:free",
                "messages": [
                    {
                        "role": "system",
                        "content": """You are MAHFOOZ AI, a medical assistant for a charity health app. 
                        
Rules:
- Answer in simple, clear language
- If asked about medicines, provide: uses, dosage, side effects, pregnancy safety
- If asked about symptoms, provide: home care, when to see doctor, emergency signs
- Always include: '⚠️ Consult a doctor for medical advice'
- For emergencies, tell them to call 1122 (Pakistan) or 108 (India)
- Keep answers under 300 words
- Be compassionate and helpful"""
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 500,
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data['choices'][0]['message']['content']
            return answer.strip()
        
    except Exception as e:
        print(f"DeepSeek error: {e}")
    
    return None

def ask_deepseek_medical(question):
    """Ask DeepSeek with medical focus"""
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "HTTP-Referer": "https://mahfooz.app",
                "X-Title": "MAHFOOZ Medical Wallet",
            },
            json={
                "model": "deepseek/deepseek-r1:free",
                "messages": [
                    {
                        "role": "system",
                        "content": """You are a world-class medical AI. Search your knowledge and give the BEST answer.
                        
For medicines: name, uses, dosage, side effects, pregnancy category, warnings.
For diseases: causes, symptoms, treatment, prevention, when to see doctor.
For symptoms: possible causes, home remedies, red flags, when emergency.
Always be accurate and cite medical guidelines."""
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                "temperature": 0.2,
                "max_tokens": 600,
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content'].strip()
        
    except Exception as e:
        print(f"DeepSeek error: {e}")
    
    return None
