# Prozorro Tender Monitor

## What it does

Prozorro Tender Monitor is a Python tool that monitors tenders from the Prozorro API, filters them by configured keywords, removes duplicates, saves results to CSV/JSON, and sends new matching tenders to an email address.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Copy `config.example.json` to `config.json` and fill in your own values.

Required fields:

- `scraping.pages_to_scrape` — number of API pages to scan per run.
- `scraping.items_per_page` — number of tenders to process from each page.
- `scraping.delay` — delay between API requests.
- `scraping.start_offset` — initial offset for the first run.
- `scraping.state_file` — file where the last offset is stored.
- `filters.keywords` — keywords used to filter tender titles.
- `output.csv` — CSV output file.
- `output.json` — JSON database file.
- `email.from` — Gmail address used to send emails.
- `email.to` — recipient email address.
- `email.password` — Gmail App Password.
- `email.limit` — maximum number of tenders included in one email.

Do not commit real passwords or private email credentials to GitHub.

## Run

```bash
python main.py
```
    