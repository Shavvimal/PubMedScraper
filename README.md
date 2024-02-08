# PubMed Scraper

Welcome to the PubMed Scraper repo! This tool is designed for efficient extraction of the [PubMed Open Access Subset](https://www.ncbi.nlm.nih.gov/pmc/tools/openftlist/), a resource comprising millions of freely available journal articles and preprints.

These documents are distributed under licenses permitting reuse, making them an ideal dataset for academic research, data analysis, and machine learning projects. Utilizing the PMC [FTP Service](https://www.ncbi.nlm.nih.gov/pmc/tools/ftp/), this repo provides a solution for bulk downloading, parsing the nested XML files in the `tar.gz`'s, and storing the PMC OA subset data in a structured PostgreSQL database, ready for analysis.

## Getting Started 🚀

Ensure you have:

- Python 3.11 or later 🐍
- Access to a PostgreSQL database 🗄️
- Required Python packages: `beautifulsoup4`, `psycopg2-binary`, `python-dotenv`, `pydantic`

### Installation

1. Clone the repository to your local machine.
2. Install the required Python packages by running `pip install -r requirements.txt`
3. Set up your environment variables for database access
   - `DB_USER`
   - `DB_PASS`
   - `DB_HOST`
   - `DB_PORT`
   - `DB_NAME`
4. The database should be set up with the following table:

```sql
CREATE TABLE pub_med_papers (
    pmid TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    abstract TEXT,
    full_text TEXT,
    authors TEXT
);
```

### Running the Scraper

To launch the scraper, make sure your database is up and running, then execute the main script from the command line:

```bash
python app/main.py
```

## Result

The scraper will download the PMC OA subset, parse the XML files, and store the data in the PostgreSQL database:

![PunMed Data in PGAdmin](/img/image.png)

## Features ✨

- **Bulk Download:** Automates the retrieval of bulk datasets from the PMC FTP service.
- **XML Parsing:** Efficiently extracts key information from complex XML structures into an organized format.
- **Database Storage:** Neatly stores extracted data in a PostgreSQL database, facilitating easy retrieval and analysis.
- **Deep Extraction of Nested Files:** Extracts and parses nested XML files from compressed `.tar.gz` archives
- **Postprocessing with Worker Queues:** Employs worker queue system for efficient postprocessing of downloaded content.
- **Efficient Database Connection Pooling:** Implements a connection pool to efficiently manage database interactions, reducing overhead
