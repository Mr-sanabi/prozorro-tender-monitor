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
        
        response = requests.get(f"https://api.prozorro.gov.ua/api/2.5/tenders?offset={offset}", timeout=15)
        response.raise_for_status()
        index = response.json()
        time.sleep(delay)

        for item in index["data"][:items_per_page]:
            tender_id = item["id"]
            response = requests.get(f"https://api.prozorro.gov.ua/api/2.5/tenders/{tender_id}", timeout=15)
            response.raise_for_status()
            detail = response.json()
            time.sleep(delay)
            t = detail["data"]
            tender_id = t.get("id")
            rows.append({
                "ID": tender_id or "unknown",
                "Название": t.get("title") or "unknown",
                "Заказчик": t.get("procuringEntity", {}).get("name") or "unknown",
                "Сума": t.get("value", {}).get("amount") or "unknown",
                "Валюта": t.get("value", {}).get("currency") or "unknown",
                "Дедлайн": t.get("tenderPeriod", {}).get("endDate") or "unknown",
                "Статус": t.get("status") or "unknown",
                "Ссылка": f"https://prozorro.gov.ua/tender/{tender_id}" if tender_id else "unknown",
                "Дата изменения": t.get("dateModified") or "unknown",

            })
        offset = index["next_page"]["offset"]
        logging.info(f"Собрано тендеров: {len(rows)}")
    return rows, offset
