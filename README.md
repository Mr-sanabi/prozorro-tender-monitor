# Prozorro Tender Monitor

A Python 3.11+ script that collects public tenders, filters them by keywords, and saves JSON history and CSV exports.

## Run

Copy `config.example.json` to `config.json` and set paths, filters, and optional SMTP settings. Keep credentials local.

```bash
python -m pip install -r requirements.txt
python main.py --config config.json
```

Runs incrementally using a saved API offset. The offset advances after outputs are saved; failed requests leave it unchanged. Email notifications are optional.

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```
