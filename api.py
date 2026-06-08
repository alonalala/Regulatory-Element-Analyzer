import requests
import sys

BASE_URL = "https://rest.ensembl.org"

def fetch_regulatory_features(species, chrom, start, end):
    """Fetches regulatory features for a genomic region."""
    endpoint = f"/overlap/region/{species}/{chrom}:{start}-{end}?feature=regulatory"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.get(BASE_URL + endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error fetching features: {e}")
        sys.exit(1)

def fetch_region_sequence(species, chrom, start, end):
    """Fetches the full DNA sequence for a genomic region."""
    endpoint = f"/sequence/region/{species}/{chrom}:{start}-{end}"
    headers = {"Content-Type": "text/plain"}
    
    try:
        response = requests.get(BASE_URL + endpoint, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"API Error fetching sequence: {e}")
        sys.exit(1)