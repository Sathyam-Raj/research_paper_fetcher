import click
import csv
import sys
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
from .api import search_papers, fetch_paper_details
from .processor import parse_pubmed_xml, filter_non_academic_authors, has_pharma_affiliation
from .models import PaperRecord

def generate_default_filename():
    """Generate a default filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"papers_results_{timestamp}.csv"

@click.command()
@click.argument("query")
@click.option("-d", "--debug", is_flag=True, help="Print debug information during execution.")
@click.option("-f", "--file", type=click.Path(), help="Custom filename to save results as CSV.")
@click.option("-p", "--print", "print_to_console", is_flag=True, help="Print results to console instead of saving to file.")
def main(query: str, debug: bool, file: Optional[str], print_to_console: bool):
    """Fetch research papers from PubMed and save results to CSV by default."""
    output_file = file if file else generate_default_filename()
    
    if debug:
        print(f"Debug mode: ON")
        print(f"Query: {query}")
        if not print_to_console:
            print(f"Output will be saved to: {output_file}")
    
    try:
        # Step 1: Search for papers
        if debug:
            print("Searching PubMed...")
        pubmed_ids = search_papers(query)
        
        if not pubmed_ids:
            print("No papers found matching your query.")
            sys.exit(0)
            
        if debug:
            print(f"Found {len(pubmed_ids)} papers.")
        
        # Step 2: Fetch and process each paper
        results = []
        for pubmed_id in pubmed_ids:
            if debug:
                print(f"Processing paper {pubmed_id}...")
            
            paper_xml = fetch_paper_details(pubmed_id)
            if not paper_xml:
                continue
                
            paper = parse_pubmed_xml(paper_xml)
            if not paper:
                continue
                
            # Filter for papers with pharma/biotech affiliations
            if has_pharma_affiliation(paper):
                filtered_paper = filter_non_academic_authors(paper)
                if filtered_paper["authors"]:  # Only include if non-academic authors found
                    results.append(filtered_paper)
        
        if not results:
            print("No papers found with pharmaceutical/biotech affiliations.")
            sys.exit(0)
            
        # Step 3: Prepare output
        output = prepare_csv_output(results)
        
        # Step 4: Output results
        if print_to_console:
            print_csv(output)
        else:
            save_to_csv(output, output_file)
            print(f"Results saved to: {Path(output_file).resolve()}")
            
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def prepare_csv_output(papers: List[PaperRecord]) -> List[Dict]:
    """Prepare paper records for CSV output."""
    csv_data = []
    for paper in papers:
        non_academic_authors = [
            author["name"] for author in paper["authors"]
        ]
        companies = [
            author["company"] for author in paper["authors"]
            if author["company"]
        ]
        
        csv_data.append({
            "PubmedID": paper["pubmed_id"],
            "Title": paper["title"],
            "Publication Date": paper["publication_date"],
            "Non-academic Author(s)": "; ".join(non_academic_authors),
            "Company Affiliation(s)": "; ".join(companies),
            "Corresponding Author Email": paper["corresponding_author_email"] or ""
        })
    return csv_data

def save_to_csv(data: List[Dict], filename: str):
    """Save data to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def print_csv(data: List[Dict]):
    """Print data in CSV format to console."""
    import io
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    print(output.getvalue())