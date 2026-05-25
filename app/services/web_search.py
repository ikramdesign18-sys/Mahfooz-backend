# app/services/web_search.py
# MULTI-SOURCE MEDICAL SEARCH - Searches multiple sites for best answer

import requests
import re

def search_medical_web(query, max_results=3):
    """Search multiple medical sources for best answer"""
    
    all_results = []
    
    # Source 1: DuckDuckGo medical search
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            for r in ddgs.text(f"{query} medical site:mayoclinic.org OR site:webmd.com OR site:medlineplus.gov OR site:nhs.uk OR site:who.int", max_results=max_results):
                text = clean_text(r['body'])
                if len(text) > 50:
                    all_results.append({"title": r['title'], "body": text[:400], "url": r['href'], "source": "DuckDuckGo"})
    except:
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                for r in ddgs.text(f"{query} medical", max_results=max_results):
                    text = clean_text(r['body'])
                    if len(text) > 50:
                        all_results.append({"title": r['title'], "body": text[:400], "url": r['href'], "source": "DuckDuckGo"})
        except:
            pass
    
    # Source 2: Wikipedia medical
    try:
        import wikipedia
        search_results = wikipedia.search(query, results=2)
        for term in search_results:
            try:
                summary = wikipedia.summary(term, sentences=3)
                if len(summary) > 50:
                    all_results.append({"title": term, "body": summary[:400], "url": f"https://en.wikipedia.org/wiki/{term.replace(' ', '_')}", "source": "Wikipedia"})
            except:
                pass
    except:
        pass
    
    # Source 3: PubMed (free medical research)
    try:
        pubmed_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmax=2&format=json"
        pubmed_response = requests.get(pubmed_url, timeout=10)
        if pubmed_response.status_code == 200:
            ids = pubmed_response.json().get('esearchresult', {}).get('idlist', [])
            for pid in ids[:2]:
                fetch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pid}&format=json"
                fetch_response = requests.get(fetch_url, timeout=10)
                if fetch_response.status_code == 200:
                    data = fetch_response.json().get('result', {}).get(pid, {})
                    title = data.get('title', '')
                    if title:
                        all_results.append({"title": title, "body": f"PubMed ID: {pid}. {title}", "url": f"https://pubmed.ncbi.nlm.nih.gov/{pid}/", "source": "PubMed"})
    except:
        pass
    
    return all_results[:5] if all_results else None

def clean_text(text):
    """Clean search result text"""
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^\w\s.,!?;:()\-\'\"]', '', text)
    return text

def search_medicine_info(medicine_name):
    """Search medicine information from multiple sources"""
    return search_medical_web(f"{medicine_name} drug uses dosage side effects", max_results=3)

def search_symptoms(symptoms_text):
    """Search symptom information"""
    return search_medical_web(f"{symptoms_text} symptoms causes treatment", max_results=3)
