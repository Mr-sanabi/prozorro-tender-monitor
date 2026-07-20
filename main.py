import argparse
import csv
import json
import logging
from pathlib import Path

from cleaner import clean_tender, deduplicate, filter_tenders
from notifier import send_email
from scraper import scrape_tenders

FIELDS = ["ID", "Название", "Заказчик", "Сума", "Валюта", "Дедлайн", "Статус", "Ссылка", "Дата изменения"]


def parse_args():
    parser = argparse.ArgumentParser(description="Monitor Prozorro tenders and notify about matching new entries.")
    parser.add_argument("--config", default="config.json", help="Path to the JSON configuration file")
    return parser.parse_args()


def load_json(path, default):
    try:
        with Path(path).open("r", encoding="utf-8") as file:
            value = json.load(file)
        return value if isinstance(value, type(default)) else default
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    temporary.replace(path)


def save_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def run(config):
    state_path = Path(config["scraping"]["state_file"])
    try:
        offset = state_path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        offset = config["scraping"]["start_offset"]

    history_path = config["output"]["json"]
    old_rows = load_json(history_path, [])
    rows, next_offset = scrape_tenders(config, offset)
    clean_rows = [clean_tender(tender) for tender in rows]
    final_rows, new_rows, duplicates = deduplicate(clean_rows, old_rows)
    matching = filter_tenders(new_rows, config["filters"]["keywords"])

    save_csv(config["output"]["csv"], matching)
    atomic_json(history_path, final_rows)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(next_offset, encoding="utf-8")

    if matching:
        send_email(matching, config)
    logging.info("Найдено %s, новых %s, дубликатов %s", len(clean_rows), len(new_rows), duplicates)
    return matching


def main():
    args = parse_args()
    config = load_json(args.config, {})
    if not config:
        raise SystemExit(f"Invalid or missing config: {args.config}")
    log_path = Path(config.get("output", {}).get("log", "logs/scraper.log"))
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(log_path, encoding="utf-8"), logging.StreamHandler()])
    run(config)


if __name__ == "__main__":
    main()
