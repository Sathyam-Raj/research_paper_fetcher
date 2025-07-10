import requests
from typing import List, Dict, Optional
from .models import PaperRecord

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def search_papers(query: str, max_results: int = 100) -> List[str]:
    """Search PubMed for papers matching the query and return PubMed IDs."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,
    }
    
    try:
        response = requests.get(PUBMED_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])
    except requests.exceptions.RequestException as e:
        print(f"Error searching PubMed: {e}")
        return []

def fetch_paper_details(pubmed_id: str) -> Optional[Dict]:
    """Fetch detailed information for a single paper using its PubMed ID."""
    params = {
        "db": "pubmed",
        "id": pubmed_id,
        "retmode": "xml",
    }
    
    try:
        response = requests.get(PUBMED_FETCH_URL, params=params)
        response.raise_for_status()
        return response.text  # We'll parse XML later
    except requests.exceptions.RequestException as e:
        print(f"Error fetching paper details for {pubmed_id}: {e}")
        return None