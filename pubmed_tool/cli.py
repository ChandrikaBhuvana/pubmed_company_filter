# === External Modules ===
import typer  # Typer is used to build the command-line interface
from typing import Optional  # Needed for optional output_file
import pandas as pd

# === Internal Imports ===
from pubmed.api import search_papers, fetch_metadata  # Functions for searching and fetching PubMed data
from pubmed.parser import extract_metadata  # Function to parse raw XML into structured metadata
from pubmed.filter import has_company_author, is_company_affiliation  # Functions to detect company authors

# === Typer App Instance ===
app = typer.Typer(help="Fetch and filter PubMed papers with at least one company-affiliated author.")

# === Search Command ===
@app.command()
def search(
    query: str = typer.Option(..., "--query", "-q", help="PubMed search query"),
    max_results: int = typer.Option(100, "--max-results", "-m", help="Maximum number of results to fetch"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Path to save the output CSV (optional)"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode to show internal logs")
):
    """
    Main CLI command to search PubMed, fetch article metadata,
    parse it into structured data, filter company-affiliated ones,
    and save/output the required metadata.
    """

    if debug:
        typer.echo("[DEBUG] Debug mode is enabled")

    typer.echo(f"Searching PubMed for query: {query}")
    typer.echo(f"Max results to fetch: {max_results}")
    if output_file:
        typer.echo(f"Output will be saved to: {output_file}")
    else:
        typer.echo("No --output provided. Results will be printed to console.")

    # --- Step 1: Search for PMIDs ---
    pmids = search_papers(query, max_results, debug=debug)
    if not pmids:
        typer.secho("No PMIDs found or API search failed. Exiting.", fg=typer.colors.RED)
        raise typer.Exit()

    typer.echo(f"Found {len(pmids)} PMIDs.")
    typer.echo(f"First few PMIDs: {pmids[:5]}")

    # --- Step 2: Fetch Metadata ---
    xml_data = fetch_metadata(pmids, debug=debug)
    if not xml_data:
        typer.secho("Failed to fetch metadata. Exiting.", fg=typer.colors.RED)
        raise typer.Exit()

    typer.echo(f"Fetched {len(xml_data)} characters of XML metadata.")

    # --- Step 3: Parse XML into Structured Data ---
    articles = extract_metadata(xml_data, debug=debug)
    if not articles:
        typer.secho("Failed to parse articles from XML. Exiting.", fg=typer.colors.RED)
        raise typer.Exit()

    typer.echo(f"Parsed {len(articles)} articles.")

    # --- Step 4: Filter Articles Based on Company Affiliation ---
    final_output = []
    for article in articles:
        all_affiliations = [aff for author in article["authors"] for aff in author["affiliations"]]

        if not has_company_author(all_affiliations, debug=debug):
            continue  # Skip non-company papers

        non_academic_authors = []
        company_affiliations = set()

        for author in article["authors"]:
            for aff in author["affiliations"]:
                if is_company_affiliation(aff):
                    non_academic_authors.append(author["name"])
                    company_affiliations.add(aff)

        final_output.append({
            "pmid": article["pmid"],
            "title": article["title"],
            "publication_date": article["publication_date"],
            "non_academic_authors": list(set(non_academic_authors)),
            "company_affiliations": list(company_affiliations),
            "emails": article["emails"]
        })

    typer.echo(f"Filtered down to {len(final_output)} company-affiliated articles.")

    if not final_output:
        typer.secho("No company-affiliated articles found. Exiting.", fg=typer.colors.YELLOW)
        raise typer.Exit()

    # --- Step 5: Preview First Filtered Article ---
    typer.echo("First article:")
    first = final_output[0]
    typer.echo(f"  PMID: {first['pmid']}")
    typer.echo(f"  Title: {first['title']}")
    typer.echo(f"  Publication Date: {first['publication_date']}")
    typer.echo(f"  Non-Academic Authors: {first['non_academic_authors']}")
    typer.echo(f"  Company Affiliations: {first['company_affiliations']}")
    typer.echo(f"  Emails: {first['emails']}")

    # --- Step 6: Save or Print Output ---
    df = pd.DataFrame(final_output)

    if output_file:
        df.to_csv(output_file, index=False)
        typer.echo(f"Saved {len(df)} records to {output_file}")
    else:
        typer.echo("Printing result to console:")
        try:
            typer.echo(df.to_markdown(index=False))
        except Exception:
            typer.echo(df.to_string(index=False))  # Fallback if rich-markdown fails

# === Entry Point ===
if __name__ == "__main__":
    app()
