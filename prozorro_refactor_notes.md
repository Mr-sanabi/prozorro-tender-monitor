# Prozorro Refactor Notes

## Что уже хорошо
- Проект разбит на модули: scraper.py, cleaner.py, notifier.py, main.py
- Есть config.json
- Есть logging
- Есть deduplication
- Есть фильтрация по keywords
- Есть state через offset
- Есть CSV/JSON export
- Есть email notification
- Добавлены базовые type hints к ключевым функциям

## Что улучшил сегодня
- Добавил type hints в scraper.py
- Добавил type hints в notifier.py
- Добавил type hints в cleaner.py
- Проверил, какие функции что принимают и что возвращают

## Что можно улучшить в будущем
- Вынести формирование текста письма в отдельную функцию `build_email_text(...)`
- Добавить обработку requests-ошибок в scraper.py
- Уточнить тип config через TypedDict, но позже
- Улучшить обработку отсутствующих ключей в `filter_tenders`
- Добавить type hints к `clean_value`, но сейчас это не обязательно
- Добавить отдельные функции load_json / save_json / save_csv, если они ещё в main.py

## Главный вывод
Проект уже имеет нормальную структуру. Сейчас задача не переписать его полностью, а научиться видеть зоны ответственности функций и постепенно улучшать читаемость.