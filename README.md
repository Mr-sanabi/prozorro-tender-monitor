# Prozorro Tender Monitor

A configuration-driven Python monitor for collecting, filtering, deduplicating, and exporting public Prozorro tenders.

## Features

- paginated API collection with request timeout and status validation;
- normalized tender records and keyword filtering;
- JSON history and CSV exports;
- offset-based incremental runs;
- optional SMTP notification for matching new tenders;
- atomic history writes and delayed state advancement.

## Setup

```bash
python -m pip install -r requirements.txt
cp config.example.json config.json
python main.py --config config.json
```

Review the paths, filters, and email settings in `config.json` before running it. The local config and generated state are ignored by Git.

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Reliability contract

The stored offset is advanced only after the output files are written. A failed API request therefore cannot silently skip unseen tenders on the next run.

## Stack

Python 3.11+, Requests, JSON, CSV, SMTP, pytest.
