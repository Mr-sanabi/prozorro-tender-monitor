def clean_value(value):
    if isinstance(value, str):
        value = value.replace("\n", " ").replace("\t", " ")
        value = "".join(ch for ch in value if ch.isprintable())
        value = " ".join(value.split())

        if value == "":
            return None
        
        if len(value) >= 10 and value[4] == "-" and value[7] == "-":
            return value[:10]
        
        return value
    return value
def clean_tender(tender):
    cleaned = {}

    for key, value in tender.items():
        cleaned[key] = clean_value(value)

    return cleaned

def filter_tenders(tenders, keywords):
    
    if keywords == []:
        return tenders
    
    filtered = []

    for item in tenders:
        title = item["Название"]
        title = title.lower()

        for i in keywords:
            if i.lower() in title:
                filtered.append(item)
                break
    
    return filtered

def deduplicate(tenders, old_rows):
    unique_new_rows = []
    duplicates = 0  
    seen_url = set()
    for item in old_rows:
        url = item["Ссылка"]
        seen_url.add(url)
    for new_rows in tenders:
        url = new_rows["Ссылка"]

        if url not in seen_url:
            seen_url.add(url)
            unique_new_rows.append(new_rows)
        else:
            duplicates+=1
    
    final_rows = old_rows + unique_new_rows

    return final_rows, unique_new_rows, duplicates