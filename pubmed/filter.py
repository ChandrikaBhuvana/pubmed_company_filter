# filters.py

import re  # Regular expressions to detect company-related keywords
from typing import List  # NEW: Type hinting for better readability and tooling

# ----------------------------------------------------------------------------------
# Function: is_company_affiliation
# ----------------------------------------------------------------------------------
def is_company_affiliation(affiliation: str) -> bool:
    """
    Checks if the given affiliation string looks like it belongs to a company
    (as opposed to a university, hospital, or research institute).

    Args:
        affiliation (str): The affiliation text from PubMed.

    Returns:
        bool: True if it's likely a company affiliation, False otherwise.
    """

    # --- Convert to lowercase for consistent matching ---
    text = affiliation.lower()

    # --- Company-related keywords to match against ---
    company_keywords = [
        r"\binc\b", r"\bltd\b", r"\bllc\b", r"\bcorp\b", r"\bco\b",
        r"\bcompany\b", r"\btechnologies\b", r"\bsolutions\b", r"\bpharma\b",
        r"\bindustries\b", r"\bbiotech\b", r"\blaboratories\b", r"\bstart[- ]?up\b",
        r"\bsas\b", r"\bgmbh\b", r"\bpvt\b", r"\bprivate limited\b"
    ]

    # --- Academic-related keywords (to skip) ---
    academic_keywords = [
        r"\buniversity\b", r"\binstitute\b", r"\bcollege\b", r"\bhospital\b",
        r"\bdepartment\b", r"\bcentre\b", r"\bcenter\b", r"\bclinic\b",
        r"\bresidency\b", r"\bmedical school\b", r"\bfaculty\b"
    ]

    # --- If academic keywords appear, likely not a company ---
    if any(re.search(pattern, text) for pattern in academic_keywords):
        return False

    # --- If any company keyword is present, flag as company ---
    return any(re.search(pattern, text) for pattern in company_keywords)

# ----------------------------------------------------------------------------------
# Function: has_company_author
# ----------------------------------------------------------------------------------
def has_company_author(affiliations: List[str], debug: bool = False) -> bool:  # NEW: Used List[str] for clarity
    """
    Checks if there's at least one company-affiliated author in the list.

    Args:
        affiliations (list[str]): List of affiliation strings.
        debug (bool): If True, prints each affiliation and decision.

    Returns:
        bool: True if any affiliation looks like it's from a company.
    """
    for aff in affiliations:
        result = is_company_affiliation(aff)
        if debug:
            print(f"[DEBUG] Affiliation: {aff} --> {'COMPANY' if result else 'non-company'}")  # NEW: Log decision per affiliation
        if result:
            return True  # Return True as soon as a company affiliation is found
    return False  # If none of the affiliations matched
