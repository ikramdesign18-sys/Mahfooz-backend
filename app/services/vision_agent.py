# app/services/vision_agent.py
# Enhanced Vision Agent for Handwritten Prescriptions
# Uses EasyOCR + Tesseract for better handwriting recognition

import cv2
import numpy as np
from PIL import Image
import pytesseract
import easyocr
import re
import os

# Initialize EasyOCR reader (English)
reader = easyocr.Reader(['en'], gpu=False)

# Common medical abbreviations
MEDICAL_ABBREVIATIONS = {
    "bid": "Twice daily",
    "b.i.d": "Twice daily",
    "tid": "Three times daily",
    "t.i.d": "Three times daily",
    "qid": "Four times daily",
    "q.i.d": "Four times daily",
    "od": "Once daily",
    "o.d": "Once daily",
    "hs": "At bedtime",
    "h.s": "At bedtime",
    "pc": "After meals",
    "p.c": "After meals",
    "ac": "Before meals",
    "a.c": "Before meals",
    "prn": "As needed",
    "p.r.n": "As needed",
    "stat": "Immediately",
    "po": "By mouth",
    "p.o": "By mouth",
    "iv": "Intravenous",
    "i.v": "Intravenous",
    "im": "Intramuscular",
    "i.m": "Intramuscular",
    "sc": "Subcutaneous",
    "s.c": "Subcutaneous",
    "tab": "Tablet",
    "cap": "Capsule",
    "syr": "Syrup",
    "inj": "Injection",
    "mg": "milligrams",
    "ml": "milliliters",
    "mcg": "micrograms",
    "qty": "Quantity",
    "dx": "Diagnosis",
    "rx": "Prescription",
    "tx": "Treatment",
    "fx": "Fracture",
    "hx": "History",
    "sx": "Symptoms",
    "cx": "Complaint",
    "ddx": "Differential Diagnosis",
    "npo": "Nothing by mouth",
    "n.p.o": "Nothing by mouth",
}

# Common medicine names for spell correction
COMMON_MEDICINES = [
    "paracetamol", "ibuprofen", "aspirin", "amoxicillin", "metformin",
    "omeprazole", "lisinopril", "atorvastatin", "levothyroxine", "metronidazole",
    "cetirizine", "loratadine", "salbutamol", "insulin", "warfarin",
    "diclofenac", "tramadol", "gabapentin", "pregabalin", "sertraline",
    "fluoxetine", "amlodipine", "losartan", "pantoprazole", "azithromycin"
]

class VisionAgent:
    def __init__(self):
        self.abbreviations = MEDICAL_ABBREVIATIONS
        self.common_medicines = COMMON_MEDICINES
    
    def scan_prescription(self, image_path):
        """
        Enhanced prescription scanning using multiple OCR engines
        """
        results = {
            "raw_text": "",
            "cleaned_text": "",
            "medicines_found": [],
            "abbreviations_found": [],
            "dosage_instructions": [],
            "confidence": 0
        }
        
        try:
            # Step 1: Try EasyOCR first (better for handwriting)
            image = cv2.imread(image_path)
            if image is None:
                return {"error": "Cannot read image"}
            
            # Preprocess image
            processed = self.preprocess_image(image)
            
            # EasyOCR
            easy_results = reader.readtext(processed)
            easy_text = " ".join([r[1] for r in easy_results if r[2] > 0.3])
            
            # Tesseract as backup
            tess_text = pytesseract.image_to_string(processed, config='--psm 6')
            
            # Combine results (use the longer one - usually more complete)
            raw_text = easy_text if len(easy_text) > len(tess_text) else tess_text
            
            results["raw_text"] = raw_text
            
            # Step 2: Try with different OCR settings for handwriting
            try:
                import pytesseract
                # Handwriting mode
                hw_config = r'--oem 1 --psm 6'
                hw_text = pytesseract.image_to_string(processed, config=hw_config)
                if len(hw_text) > len(raw_text):
                    raw_text = hw_text
                    results["raw_text"] = raw_text
            except:
                pass
            
            # Step 2: Clean and expand abbreviations
            cleaned = self.expand_abbreviations(raw_text)
            results["cleaned_text"] = cleaned
            
            # Add line-by-line reading
            lines = [l.strip() for l in cleaned.split('\n') if l.strip()]
            results["lines"] = lines[:20]  # First 20 lines
            results["abbreviations_found"] = self.find_abbreviations(raw_text)
            
            # Step 3: Extract medicines
            results["medicines_found"] = self.extract_medicines(cleaned)
            
            # Step 4: Extract dosage instructions
            results["dosage_instructions"] = self.extract_dosage(cleaned)
            
            # Step 5: Calculate confidence
            if len(raw_text) > 20:
                results["confidence"] = min(0.9, len(raw_text) / 200)
            else:
                results["confidence"] = 0.3
            
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def preprocess_image(self, image):
        """Enhance image for better OCR"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Increase contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # Threshold
        _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
    
    def expand_abbreviations(self, text):
        """Replace medical abbreviations with full words"""
        words = text.split()
        expanded = []
        
        for word in words:
            lower = word.lower().strip('.,;:')
            if lower in self.abbreviations:
                expanded.append(f"{word}({self.abbreviations[lower]})")
            else:
                expanded.append(word)
        
        return " ".join(expanded)
    
    def find_abbreviations(self, text):
        """Find all medical abbreviations in text"""
        found = []
        words = text.lower().split()
        
        for word in words:
            clean = word.strip('.,;:')
            if clean in self.abbreviations:
                found.append({
                    "abbreviation": clean,
                    "meaning": self.abbreviations[clean]
                })
        
        return found
    
    def extract_medicines(self, text):
        """Extract medicine names from prescription"""
        text_lower = text.lower()
        found = []
        
        for medicine in self.common_medicines:
            if medicine in text_lower:
                found.append(medicine)
        
        # Also try to find unknown medicines (Capitalized words after numbers)
        medicine_pattern = r'(?:Tab|Cap|Syr|Inj)\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'
        matches = re.findall(medicine_pattern, text)
        for match in matches:
            if match.lower() not in found:
                found.append(match.lower())
        
        return list(set(found))
    
    def extract_dosage(self, text):
        """Extract dosage instructions"""
        instructions = []
        
        # Pattern: Medicine Name Dose Frequency
        patterns = [
            r'([A-Za-z]+)\s+(\d+)\s*(mg|ml|mcg|g)\s*(bid|tid|qd|od|hs|pc|ac|prn|daily|weekly)',
            r'Take\s+(\d+)\s*(tablet|capsule|pill|dose)',
            r'(\d+)\s*(mg|ml)\s*(every|daily|twice|once)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                instructions.append(" ".join(match))
        
        return instructions
    
    def explain_prescription(self, scan_results):
        """Convert scan results to patient-friendly explanation"""
        explanation = []
        
        if scan_results.get("medicines_found"):
            explanation.append("📋 **Medicines Found:**")
            for med in scan_results["medicines_found"]:
                explanation.append(f"  • {med.title()}")
        
        if scan_results.get("dosage_instructions"):
            explanation.append("\n💊 **Dosage Instructions:**")
            for inst in scan_results["dosage_instructions"]:
                explanation.append(f"  • {inst}")
        
        if scan_results.get("abbreviations_found"):
            explanation.append("\n📖 **Medical Terms Explained:**")
            for abbr in scan_results["abbreviations_found"]:
                explanation.append(f"  • {abbr['abbreviation']} = {abbr['meaning']}")
        
        if not explanation:
            explanation.append("I couldn't clearly read the prescription. Please upload a clearer image.")
        
        explanation.append(f"\n📊 **Scan Confidence:** {scan_results.get('confidence', 0)*100:.0f}%")
        explanation.append("\n⚠️ Always verify with your doctor or pharmacist.")
        
        return "\n".join(explanation)