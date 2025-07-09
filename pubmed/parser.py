import xml.etree.ElementTree as ET  # For parsing XML
from typing import List, Dict  # For type annotations

# === Function: Parse raw XML to structured metadata ===
def extract_metadata(xml_string: str, debug: bool = False) -> List[Dict]:
    """
    Parses the PubMed XML response into a list of article dictionaries.
    Each dictionary contains metadata like title, authors, affiliations, etc.

    Args:
        xml_string (str): Raw XML response from PubMed.
        debug (bool): Enable detailed debug output if True.

    Returns:
        List[Dict]: List of parsed article metadata dictionaries.
    """
    articles = []

    try:
        root = ET.fromstring(xml_string)  # Parse the raw XML string

        # Iterate through all PubmedArticle elements in the XML
        for article in root.findall(".//PubmedArticle"):
            pmid = article.findtext(".//PMID")  # Extract PMID
            title = article.findtext(".//ArticleTitle")  # Extract article title

            if debug:
                print(f"[DEBUG] Processing article with PMID: {pmid}")  # NEW: Log current article PMID
                print(f"[DEBUG] Title: {title}")  # NEW: Log article title

            authors = []
            for author in article.findall(".//Author"):
                last = author.findtext("LastName") or ""  # Handle missing last name
                first = author.findtext("ForeName") or ""  # Handle missing first name
                full_name = f"{first} {last}".strip()  # Combine names cleanly

                # Extract all affiliation strings for this author
                aff_list = [aff.text for aff in author.findall("AffiliationInfo/Affiliation") if aff.text]

                if debug:
                    print(f"[DEBUG] Author: {full_name}, Affiliations: {aff_list}")  # NEW: Log author name and affiliations

                authors.append({
                    "name": full_name,
                    "affiliations": aff_list
                })

            # Extract publication date (format: YYYY-MM-DD)
            pub_date_node = article.find(".//PubDate")
            if pub_date_node is not None:
                year = pub_date_node.findtext("Year") or ""
                month = pub_date_node.findtext("Month") or ""
                day = pub_date_node.findtext("Day") or ""
                publication_date = f"{year}-{month}-{day}".strip("-")  # Remove trailing dash if day/month is missing
            else:
                publication_date = "N/A"

            # Look for email addresses inside affiliation text (basic heuristic)
            email_nodes = article.findall(".//AffiliationInfo/Affiliation")
            emails = []
            for aff in email_nodes:
                if aff is not None and aff.text and "@" in aff.text:
                    emails.append(aff.text.strip())  # Collect raw email-containing strings

            # Assemble structured article record
            articles.append({
                "pmid": pmid,
                "title": title,
                "authors": authors,
                "publication_date": publication_date,
                "emails": emails
            })

    except ET.ParseError as e:
        if debug:
            print(f"[DEBUG] XML parsing error: {e}")  # NEW: Log XML parsing failure

    if debug:
        print(f"[DEBUG] Parsed {len(articles)} articles total")  # NEW: Log total articles parsed

    return articles
