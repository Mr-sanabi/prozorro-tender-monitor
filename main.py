import json 
import csv
from scraper import scrape_tenders
from cleaner import clean_tender, deduplicate, filter_tenders
from notifier import send_email
import logging



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("scraper.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

try:
    with open("tenders.json", "r", encoding="utf-8") as file:
        old_rows = json.load(file)
except FileNotFoundError:
    old_rows = []

try:
    with open(config["scraping"]["state_file"], "r", encoding="utf-8") as file:
        offset = file.read().strip()
except FileNotFoundError:
    offset = config["scraping"]["start_offset"]

logging.info("Запуск скрапера")
rows, offset = scrape_tenders(config, offset)

with open(config["scraping"]["state_file"], "w", encoding="utf-8") as file:
            file.write(offset)

clean_rows = []

for tender in rows:
        clean_rows.append(clean_tender(tender))

final_rows, unique_new_rows, duplicates = deduplicate(clean_rows, old_rows)

result = filter_tenders(unique_new_rows, config["filters"]["keywords"])

if result:
    send_email(result, config)
else:
    if unique_new_rows:
        logging.info("Новые тендеры есть, но ни один не подходит под keywords")
    else:
        logging.info("Нет новых подходящих тендеров, письмо не отправлено")

logging.info(f"Найдено {len(clean_rows)}, новых {len(unique_new_rows)}, дубликатов {duplicates}")
fields = ["ID", "Название", "Заказчик", "Сума", "Валюта", "Дедлайн", "Статус", "Ссылка", "Дата изменения"]
with open(config["output"]["csv"], "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(result)

with open(config["output"]["json"], "w", encoding="utf-8") as file:
    json.dump(final_rows, file, indent=4, ensure_ascii=False)