import re
from typing import List, Optional, Dict
from xml.etree import ElementTree as ET
from .models import PaperRecord, AuthorAffiliation

# Keywords that typically indicate academic affiliations
ACADEMIC_KEYWORDS = {
    "university", "college", "institute", "school", 
    "academy", "labs", "laboratory", "hospital",
    "medical center", "clinic", "foundation"
}

# Common pharmaceutical/biotech company names (can be expanded)
PHARMA_COMPANIES = {
    "pfizer", "novartis", "roche", "sanofi", "merck", 
    "johnson & johnson", "astrazeneca", "gilead", 
    "glaxosmithkline", "abbvie", "bristol-myers squibb",
    "biogen", "amgen", "eli lilly", "moderna", "bioNTech"
}

def parse_pubmed_xml(xml_content: str) -> Optional[PaperRecord]:
    """Parse PubMed XML response into a structured paper record."""
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None
    
    # Extract basic paper information
    article = root.find(".//PubmedArticle//Article")
    if article is None:
        return None
    
    pubmed_id = root.findtext(".//PubmedArticle//PMID")
    title = article.findtext(".//ArticleTitle")
    pub_date = article.findtext(".//Journal//PubDate//Year")
    
    if not all([pubmed_id, title, pub_date]):
        return None
    
    # Extract author information
    authors = []
    corresponding_email = None
    
    for author in article.findall(".//AuthorList//Author"):
        last_name = author.findtext("LastName")
        fore_name = author.findtext("ForeName")
        if not last_name:
            continue
            
        author_name = f"{fore_name} {last_name}" if fore_name else last_name
        affiliations = []
        
        # Extract affiliations
        for aff in author.findall(".//Affiliation"):
            aff_text = aff.text
            if aff_text:
                affiliations.append(aff_text)
                
        # Determine if non-academic and company affiliation
        is_non_academic = False
        company_affiliation = None
        
        for aff in affiliations:
            aff_lower = aff.lower()
            
            # Check if affiliation contains any academic keywords
            is_academic = any(keyword in aff_lower for keyword in ACADEMIC_KEYWORDS)
            
            if not is_academic:
                is_non_academic = True
                # Check for pharmaceutical/biotech company names
                for company in PHARMA_COMPANIES:
                    if company in aff_lower:
                        company_affiliation = company.capitalize()
                        break
        
        # Check for corresponding author email
        email = author.findtext(".//Affiliation[@email]")
        if email and "@" in email:
            corresponding_email = email
            
        authors.append({
            "name": author_name,
            "affiliation": "; ".join(affiliations),
            "is_non_academic": is_non_academic,
            "company": company_affiliation
        })
    
    return {
        "pubmed_id": pubmed_id,
        "title": title,
        "publication_date": pub_date,
        "authors": authors,
        "corresponding_author_email": corresponding_email
    }

def filter_non_academic_authors(paper: PaperRecord) -> PaperRecord:
    """Filter authors to only those with non-academic affiliations."""
    filtered_authors = [
        author for author in paper["authors"] 
        if author["is_non_academic"]
    ]
    return {**paper, "authors": filtered_authors}

def has_pharma_affiliation(paper: PaperRecord) -> bool:
    """Check if any author has a pharmaceutical/biotech affiliation."""
    return any(
        author["company"] is not None
        for author in paper["authors"]
    )