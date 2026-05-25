# app/services/openfda_service.py
# FREE Official FDA Drug Database Integration
# Provides verified medicine information

import requests
import json

OPENFDA_BASE = "https://api.fda.gov/drug"

def search_drug(drug_name, limit=3):
    """
    Search for official drug information from FDA
    Returns verified drug data
    """
    try:
        # Search by brand name or generic name
        url = f"{OPENFDA_BASE}/label.json"
        params = {
            "search": f'openfda.brand_name:"{drug_name}" OR openfda.generic_name:"{drug_name}"',
            "limit": limit
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = []
            
            for result in data.get("results", []):
                openfda = result.get("openfda", {})
                results.append({
                    "brand_name": openfda.get("brand_name", [drug_name])[0],
                    "generic_name": openfda.get("generic_name", ["Unknown"])[0],
                    "manufacturer": openfda.get("manufacturer_name", ["Unknown"])[0],
                    "purpose": result.get("purpose", [""])[0][:300],
                    "warnings": result.get("warnings", [""])[0][:300] if result.get("warnings") else "",
                    "dosage": result.get("dosage_and_administration", [""])[0][:300] if result.get("dosage_and_administration") else "",
                    "side_effects": result.get("adverse_reactions", [""])[0][:300] if result.get("adverse_reactions") else "",
                    "source": "FDA Official Database"
                })
            
            return results if results else None
        
        return None
    except Exception as e:
        print(f"FDA API Error: {e}")
        return None

def search_drug_interactions(drug1, drug2):
    """
    Check official drug interactions
    """
    try:
        # Search for drug interaction data
        url = f"{OPENFDA_BASE}/label.json"
        params = {
            "search": f'openfda.brand_name:"{drug1}" AND drug_interactions:"{drug2}"',
            "limit": 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("results"):
                interactions = data["results"][0].get("drug_interactions", [""])[0]
                return {
                    "found": True,
                    "details": interactions[:500],
                    "source": "FDA Official Database"
                }
        
        return {"found": False, "message": "No official interaction data found"}
    except Exception as e:
        print(f"FDA Interaction Error: {e}")
        return None

def get_drug_warnings(drug_name):
    """
    Get official FDA warnings for a drug
    """
    try:
        url = f"{OPENFDA_BASE}/label.json"
        params = {
            "search": f'openfda.brand_name:"{drug_name}"',
            "limit": 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("results"):
                result = data["results"][0]
                return {
                    "boxed_warning": result.get("boxed_warning", [""])[0][:500] if result.get("boxed_warning") else "",
                    "warnings": result.get("warnings", [""])[0][:500] if result.get("warnings") else "",
                    "contraindications": result.get("contraindications", [""])[0][:300] if result.get("contraindications") else "",
                    "source": "FDA Official Warnings"
                }
        
        return None
    except Exception as e:
        print(f"FDA Warning Error: {e}")
        return None