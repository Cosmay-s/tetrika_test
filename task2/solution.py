"""Необходимо реализовать скрипт, который будет получать с русскоязычной
   википедии список всех животных
  (https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту)
   и записывать в файл в формате beasts.csv количество животных на каждую
   букву алфавита. Содержимое результирующего файла:"""


import requests
import csv
from collections import defaultdict
import time

API_URL = "https://ru.wikipedia.org/w/api.php"
CATEGORY = "Категория:Животные_по_алфавиту"
OUTPUT_FILE = "beasts_api.csv"


def fetch_animals_from_category() -> defaultdict[str, int]:
    """
    Получает животных из указанной категории Википедии через API.

    Возвращает:
        defaultdict[str, int]: словарь с подсчётом животных.
    """
    counts = defaultdict(int)
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": CATEGORY,
        "cmlimit": "500",
        "format": "json"
    }

    session = requests.Session()
    total = 0
    page_num = 1

    while True:
        print(f"[{page_num}] Получаем данные...")
        response = session.get(API_URL, params=params)
        data = response.json()

        for member in data.get("query", {}).get("categorymembers", []):
            title = member.get("title", "")
            if not title.startswith("Категория:"):
                first_letter = title[0].upper()
                counts[first_letter] += 1
                total += 1

        if "continue" in data:
            params.update(data["continue"])
            page_num += 1
            time.sleep(0.5)
        else:
            print(f"Готово. Загружено {total} животных.")
            break

    return counts


def save_to_csv(counts: dict[str, int], filename: str):
    """
    Сохраняет подсчитанные буквы и их количество в CSV файл.
    Сортировка букв происходит следующим образом:
      1. Сначала все русские буквы в алфавитном порядке, включая букву Ё.
      2. Затем все латинские буквы в алфавитном порядке.
      3. После них — все остальные символы (если есть), отсортированные по Unicode.

    Это нужно, чтобы результат был упорядочен логично и удобно для чтения.

    Аргументы:
        counts: dict[str, int] — словарь с ключами в виде букв (заглавных)
                               и значениями — количеством животных на эту букву.
        filename: str — имя файла для сохранения CSV.
    """
    russian_alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    latin_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def sort_key(char):
        char_upper = char.upper()
        if char_upper in russian_alphabet:
            return (0, russian_alphabet.index(char_upper))

        if char_upper in latin_alphabet:
            return (1, latin_alphabet.index(char_upper))

        return (2, ord(char_upper))

    sorted_keys = sorted(counts.keys(), key=sort_key)

    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for letter in sorted_keys:
            writer.writerow([letter, counts[letter]])


def main():
    counts = fetch_animals_from_category()
    save_to_csv(counts, OUTPUT_FILE)
    print(f"Результаты сохранены в {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
