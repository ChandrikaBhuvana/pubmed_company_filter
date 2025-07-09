import requests  # For sending HTTP requests
from typing import List  # Type hinting for list of PMIDs

# === Function: Search PubMed for PMIDs ===
def search_papers(query: str, max_results: int = 100, debug: bool = False) -> List[str]:
    """
    Use the PubMed E-utilities API (esearch) to search for article PMIDs.

    Args:
        query (str): The search query string for PubMed.
        max_results (int): Maximum number of PMIDs to retrieve.
        debug (bool): Enable verbose logging for debugging.

    Returns:
        List[str]: List of PubMed IDs (PMIDs) matching the query.
    """
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",  # Target the PubMed database
        "term": query,  # The user-provided search query
        "retmax": max_results,  # Limit the number of results
        "retmode": "json"  # Ask for JSON response format
    }

    if debug:
        print(f"[DEBUG] Sending esearch request to {url} with params: {params}")  # NEW: Show request URL and parameters

    try:
        response = requests.get(url, params=params)  # Perform the GET request
        response.raise_for_status()  # Raise error if response has HTTP error status

        data = response.json()  # Parse JSON response

        if debug:
            print(f"[DEBUG] esearch response: {data}")  # NEW: Show full JSON response from PubMed

        pmids = data.get("esearchresult", {}).get("idlist", [])  # Extract PMIDs from response

        if debug:
            print(f"[DEBUG] Retrieved {len(pmids)} PMIDs")  # NEW: Show count of PMIDs retrieved

        return pmids  # Return list of PMIDs

    except Exception as e:
        if debug:
            print(f"[DEBUG] Exception during esearch: {e}")  # NEW: Log exception details
        return []  # Return empty list if error occurs

# === Function: Fetch PubMed Metadata for Given PMIDs ===
def fetch_metadata(pmids: List[str], debug: bool = False) -> str:
    """
    Use the PubMed E-utilities API (efetch) to retrieve metadata for a list of PMIDs.
    Returns raw XML string.

    Args:
        pmids (List[str]): List of PubMed IDs to fetch metadata for.
        debug (bool): Enable verbose logging for debugging.

    Returns:
        str: Raw XML metadata string.
    """
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",  # Specify PubMed database
        "id": ",".join(pmids),  # Convert list of PMIDs to comma-separated string
        "retmode": "xml"  # Request XML response format
    }

    if debug:
        print(f"[DEBUG] Sending efetch request to {url} with {len(pmids)} PMIDs")  # NEW: Show request URL and count of PMIDs

    try:
        response = requests.get(url, params=params)  # Perform the GET request
        response.raise_for_status()  # Raise error if response has HTTP error status

        xml_data = response.text  # Extract XML string from response

        if debug:
            print(f"[DEBUG] Fetched {len(xml_data)} characters of XML data")  # NEW: Show size of XML response

        return xml_data  # Return raw XML string

    except Exception as e:
        if debug:
            print(f"[DEBUG] Exception during efetch: {e}")  # NEW: Log exception details
        return ""  # Return empty string on failure
