import pytest
import csv
from collections import defaultdict
from unittest.mock import patch, Mock
from task2.solution import fetch_animals_from_category, save_to_csv


# Мок для API-ответа
def mock_api_response(page=1):
    if page == 1:
        return {
            "query": {
                "categorymembers": [
                    {"title": "Аист"},
                    {"title": "Бегемот"},
                    {"title": "Категория:Подкатегория"}  # должна пропуститься
                ]
            },
            "continue": {"cmcontinue": "page_2_token"}
        }
    else:
        return {
            "query": {
                "categorymembers": [
                    {"title": "Волк"},
                    {"title": "Еж"},
                ]
            }
        }


@pytest.fixture
def mock_session_get():
    with patch("requests.Session.get") as mock_get:
        mock_get.side_effect = [
            Mock(status_code=200, json=lambda: mock_api_response(1)),
            Mock(status_code=200, json=lambda: mock_api_response(2))
        ]
        yield mock_get


def test_fetch_animals_from_category(mock_session_get):
    counts = fetch_animals_from_category()
    assert counts["А"] == 1
    assert counts["Б"] == 1
    assert counts["В"] == 1
    assert counts["Е"] == 1
    # Подкатегория не учитывается
    assert "К" not in counts or counts["К"] == 0


def test_save_to_csv(tmp_path):
    counts = defaultdict(int, {
        "А": 2,
        "Б": 1,
        "C": 3,
        "Ё": 1
    })
    filename = tmp_path / "out.csv"
    save_to_csv(counts, filename)

    with open(filename, encoding="utf-8") as f:
        rows = list(csv.reader(f))

    # Проверяем, что все буквы сохранены с правильными значениями
    saved = {row[0]: int(row[1]) for row in rows}
    for letter, count in counts.items():
        assert saved[letter] == count
