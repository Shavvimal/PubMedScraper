# Pubmed Scraper

This Repo collects code to scrape the [PubMed](https://www.ncbi.nlm.nih.gov/pmc/tools/openftlist/) Open Access Subset. The PMC Open Access Subset includes millions of journal articles and preprints that are made available under license terms that allow reuse. The PMC [FTP](https://www.ncbi.nlm.nih.gov/pmc/tools/ftp/) Service allows bulk download of the PMC OA subset. This repo will scrape the FTP store, parse the nested XML files, and store the data in a database for further analysis.

## Database

Environment variables are used to connect to the database. The following environment variables are used:

- `DB_USER`
- `DB_PASS`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`

The database should be set up with the following table:

```sql
CREATE TABLE pub_med_papers (
    pmid TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    abstract TEXT,
    full_text TEXT,
    authors TEXT
);
```
