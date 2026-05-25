# app/services/free_ai.py
# FREE AI models - no API key, no credit card

import requests

def ask_huggingface(question):
    """Use free Hugging Face models"""
    
    models = [
        # Medical model
        "https://api-inference.huggingface.co/models/google/flan-t5-large",
        # Chat model  
        "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
    ]
    
    for model_url in models:
        try:
            prompt = f"Answer this medical question simply and clearly: {question}"
            
            response = requests.post(
                model_url,
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_length": 200,
                        "temperature": 0.3,
                    }
                },
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get('generated_text', '')
                    text = text.replace(prompt, '').strip()
                    if len(text) > 20:
                        return text + "\n\n⚠️ AI-generated. Verify with a doctor."
        except:
            continue
    
    return None

def search_and_answer(question):
    """Search DuckDuckGo + answer with AI"""
    
    # First try AI
    ai_answer = ask_huggingface(question)
    if ai_answer:
        return ai_answer
    
    # Fallback: web search
    try:
        from app.services.web_search import search_medical_web
        results = search_medical_web(question)
        if results:
            return f"🌐 {results[0]['body'][:400]}...\n\n⚠️ From medical sources. Verify with a doctor."
    except:
        pass
    
    return None
