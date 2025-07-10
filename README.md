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

- **Python 3.11**  
- [**Poetry**](https://python-poetry.org/) – for dependency and project management  
- [**Typer**](https://typer.tiangolo.com/) – for building the CLI interface  
- `requests` – to make HTTP calls to PubMed APIs  
- `pandas` – to format and save results in CSV  
- `lxml` – for parsing PubMed XML metadata  

---

## 🚀 Setup Instructions

### 1. Clone the Repository

git clone https://github.com/your-username/pubmed_company_filter.git  
cd pubmed_company_filter

### 2. Install Dependencies Using Poetry

poetry install

### 3. Run the CLI Tool

poetry run python cli.py --query "your search query" --max-results 10 --output data/results.csv

---

## ⚙️ CLI Options

### Required

- `--query <search string>`  
  Your PubMed query (e.g., "artificial intelligence in medicine")

### Optional

- `--max-results <int>`  
  Number of results to fetch (default: 10)

- `--output <file.csv>`  
  Save output to the specified CSV file

- `--debug`  
  Show internal logs (useful for transparency and debugging)

- `--help`  
  Show usage instructions

---

### ✅ Example

poetry run python cli.py --query "cancer AND 2024[PDAT]" --max-results 15 --output data/cancer.csv --debug

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

The tool parses each author's affiliations from the PubMed XML metadata and uses regex pattern matching to detect company associations.

### Keywords Checked

Inc, LLC, Ltd, Corporation, Company, Pharma, Technologies, Solutions, Industries, and known company names like Pfizer, Roche, Genentech, Amgen, etc.

If at least one author's affiliation matches a company-related term, the paper is included.

When using `--debug`, the tool will print each author's affiliation and tag it as COMPANY or non-company.

---

## 📂 Output Format (CSV)

Example row:

pmid,title,publication_date,non_academic_authors,company_affiliations,emails  
40624840,"Impact of antibody Fc engineering...",2025-Dec,"['Eric Stefanich', 'Xiaoting Wang']","['Genentech Inc', 'Amgen Inc']",[]

---

## 🤖 LLM Usage

This project was built with the help of ChatGPT (OpenAI) to:

- Design filtering logic and regex patterns  
- Debug API integration  
- Structure the CLI using Typer  
- Write beginner-friendly documentation and clean output formats  

---

## 🧪 Sample Run (Debug Mode)

poetry run python cli.py --query "drug development Pfizer Roche" --max-results 5 --output data/drug_dev_companies.csv --debug

Output:

[DEBUG] Retrieved 5 PMIDs  
[DEBUG] Processing article with PMID: 40624840  
[DEBUG] Author: Frank R Brennan, Affiliation: UCB Pharma --> COMPANY  
...  
Filtered down to 1 company-affiliated articles.  
Saved 1 records to data/drug_dev_companies.csv

---

## 📞 Contact

Created by: Bhuvana Chandrika Mukkolla  


---

## 📎 License

This project is licensed for academic demonstration use only.

---
