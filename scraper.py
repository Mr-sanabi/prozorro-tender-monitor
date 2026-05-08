import time
import requests
import logging

def scrape_tenders(config: dict, offset: str) -> tuple[list[dict], str]:
    logging.info("Начало скрапинга")
    rows = []
    pages_to_scrape = config["scraping"]["pages_to_scrape"]
    items_per_page = config["scraping"]["items_per_page"]
    delay = config["scraping"]["delay"]
    for i in range(pages_to_scrape):

        logging.info(f"Обработка страницы {i + 1}")
        
        index = requests.get(f"https://api.prozorro.gov.ua/api/2.5/tenders?offset={offset}").json()
        time.sleep(delay)

        for item in index["data"][:items_per_page]:
            tender_id = item["id"]
            detail = requests.get(f"https://api.prozorro.gov.ua/api/2.5/tenders/{tender_id}").json()
            time.sleep(delay)
            t = detail["data"]
            rows.append({
                "ID": t.get("id") or "unknown",
                "Название": t.get("title") or "unknown",
                "Заказчик": t.get("procuringEntity", {}).get("name") or "unknown",
                "Сума": t.get("value", {}).get("amount") or "unknown",
                "Валюта": t.get("value", {}).get("currency") or "unknown",
                "Дедлайн": t.get("tenderPeriod", {}).get("endDate") or "unknown",
                "Статус": t.get("status") or "unknown",
                "Ссылка": f"https://prozorro.gov.ua/tender/{t.get('id')}" or "unknown",
                "Дата изменения": t.get("dateModified") or "unknown",

            })
            offset = index["next_page"]["offset"]
        logging.info(f"Собрано тендеров: {len(rows)}")
    return rows, offset