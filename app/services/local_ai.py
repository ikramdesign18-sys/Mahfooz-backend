# app/services/local_ai.py
# LOCAL AI MODEL - understands ANY question, no internet needed
# Uses GPT4All - completely FREE

import os

# Download model once
MODEL_PATH = os.path.expanduser("~/.cache/gpt4all/")
MODEL_NAME = "orca-mini-3b-gguf2-q4_0.gguf"

def ask_local_ai(question):
    """Ask local AI model - understands anything"""
    try:
        from gpt4all import GPT4All
        
        model_path = os.path.join(MODEL_PATH, MODEL_NAME)
        
        # Download model if not exists
        if not os.path.exists(model_path):
            print("Downloading AI model (first time only, ~2GB)...")
        
        model = GPT4All(model_name=MODEL_NAME, model_path=MODEL_PATH, allow_download=True)
        
        prompt = f"""You are a helpful medical assistant for a charity health app called MAHFOOZ.
Answer this question simply and clearly. Include dosage, warnings, and pregnancy safety if relevant.
Always say to consult a doctor for serious issues.

Question: {question}

Answer:"""
        
        response = model.generate(prompt, max_tokens=200, temp=0.3)
        return response.strip() + "\n\n⚠️ Consult a doctor for medical advice."
    
    except Exception as e:
        print(f"Local AI error: {e}")
        return None
