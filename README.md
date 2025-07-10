# 📚 PubMed Company Filter CLI Tool

A Python command-line tool to search PubMed for research articles, extract metadata, and filter results to include only those papers that have at least one **company-affiliated** author.

> ✅ Developed as part of the **Aganitha Take-Home Assignment**.

---

## 📌 Project Overview

This tool automates the process of:

- 🔍 Searching for research articles using a PubMed query  
- 📥 Fetching article metadata via PubMed's APIs  
- 🧠 Parsing the XML metadata to extract relevant fields  
- 🏢 Identifying articles with at least one **non-academic** (i.e., company-affiliated) author  
- 💾 Saving the filtered results to a CSV file  

---

## 🧰 Technologies Used

- **Python 3.12**  
- [**Poetry**](https://python-poetry.org/) – for dependency and project management  
- [**Typer**](https://typer.tiangolo.com/) – for building the CLI interface  
- `requests` – to make HTTP calls to PubMed APIs  
- `pandas` – to format and save results in CSV  
- `lxml` – for parsing PubMed XML metadata  
- `rich` – for colorful CLI output

---

## 📁 Project Structure

pubmed_company_filter/
│
├── pubmed_tool/
│     ├── __init__.py
│     └── cli.py             # Typer CLI entry point
│
├── pubmed/
│   ├── __init__.py
│   ├── api.py              # PubMed API logic
│   ├── parser.py           # XML parsing and affiliation extraction
│   └── filters.py          # Company detection logic (regex etc.)
│
├── data/                   # Output CSVs saved here
├── tests/                  # Optional test files (e.g. test_api.py)
├── pyproject.toml          # Poetry project settings
├── README.md
└── .gitignore

---

## 🚀 Setup Instructions

### 1. Clone the Repository

git clone https://github.com/ChandrikaBhuvana/pubmed_company_filter.git  
cd pubmed_company_filter

### 2. Install Dependencies Using Poetry

poetry install

### 3. Run the CLI Tool

poetry run get-papers-list --query "your search query" --max-results 10 --output data/results.csv

---

## ⚙️ CLI Options

### Required

- `--query <search string>`  
  Your PubMed query (e.g., "artificial intelligence in medicine")

### Optional

- `--max-results <int>`  
  Number of results to fetch (default: 10)

- `--output <file.csv>`  
  Save output to the specified CSV file. If not specified, results are printed to the console.

- `--debug`  
  Show internal logs for API calls and filtering logic

- `--help`  
  Show usage instructions

---

## ✅ Example Usage

poetry run get-papers-list --query "cancer AND 2024[PDAT]" --max-results 15 --output data/cancer.csv --debug

---

## 🔍 What the Tool Extracts

Each filtered article in the CSV includes:

- PubMed ID  
- Title  
- Publication Date  
- Non-academic Author(s) (company-affiliated)  
- Company Affiliation(s)  
- Corresponding Author Email (if available)  

---

## 🏭 How Company Affiliations Are Detected

The tool parses each author's affiliations and uses regex-based pattern matching to detect **company associations**.

### Keywords Checked

> Inc, LLC, Ltd, Corporation, Company, Pharma, Technologies, Solutions, Industries  
> + known names like Pfizer, Roche, Genentech, Amgen, etc.

If **at least one** author's affiliation matches a company-related pattern, the article is kept.

When `--debug` is enabled, affiliations are printed with tags like:

[DEBUG] Affiliation: Genentech Inc. --> COMPANY  
[DEBUG] Affiliation: Stanford University --> non-company

---

## 📂 Output Format (CSV)

Example row:

pmid,title,publication_date,non_academic_authors,company_affiliations,emails  
40624840,"Impact of antibody Fc engineering...",2025-12-01,"['Eric Stefanich', 'Xiaoting Wang']","['Genentech Inc', 'Amgen Inc']",[]

---

## 🤖 LLM Usage

This project was built using **ChatGPT** to:

- Design filtering logic and regex patterns  
- Debug and test PubMed API integration  
- Structure the CLI with `typer`  
- Improve documentation, code clarity, and output formatting

---

## 🧪 Sample Run (Debug Mode)

poetry run get-papers-list --query "drug development Pfizer Roche" --max-results 5 --output data/drug_dev_companies.csv --debug

Output (truncated):

[DEBUG] Retrieved 5 PMIDs  
[DEBUG] Author: Frank R Brennan, Affiliation: UCB Pharma --> COMPANY  
...  
Filtered down to 1 company-affiliated articles.  
Saved 1 records to data/drug_dev_companies.csv

---

## 📞 Contact

Created by: **Bhuvana Chandrika Mukkolla**  
📧 mukkollabhuvanachandrika@gmail.com

---

## 📎 License

This project is licensed for academic demonstration use only.
