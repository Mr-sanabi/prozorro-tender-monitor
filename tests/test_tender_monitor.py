from cleaner import clean_value, deduplicate, filter_tenders
from main import atomic_json, load_json, save_csv


def test_clean_value_collapses_whitespace_and_date():
    assert clean_value("  2026-07-20T10:30:00\n") == "2026-07-20"


def test_filter_tenders_handles_missing_title():
    assert filter_tenders([{"Название": None}], ["python"]) == []


def test_deduplicate_keeps_only_new_urls():
    old = [{"Ссылка": "https://example/1"}]
    final, new, duplicates = deduplicate([{"Ссылка": "https://example/1"}, {"Ссылка": "https://example/2"}], old)
    assert len(final) == 2
    assert new == [{"Ссылка": "https://example/2"}]
    assert duplicates == 1


def test_atomic_json_round_trip(tmp_path):
    path = tmp_path / "nested" / "tenders.json"
    atomic_json(path, [{"ID": "1"}])
    assert load_json(path, []) == [{"ID": "1"}]
    assert not path.with_suffix(".json.tmp").exists()


def test_save_csv_is_atomic(tmp_path):
    path = tmp_path / "nested" / "tenders.csv"
    save_csv(path, [])
    assert path.exists()
    assert not path.with_suffix(".csv.tmp").exists()
