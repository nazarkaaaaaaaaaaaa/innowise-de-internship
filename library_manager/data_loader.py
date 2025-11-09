from typing import Any, Iterator


def read_data(filepath: str) -> list[dict[str, Any]]:
    """Ищет необходимый файл data.txt и считывает данные из него"""
    books_keys: str = "title,author,genre,year,isbn"
    books_values: list = []
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for book in file.readlines():
                books_values.append(dict(zip(books_keys.split(","), book.strip().rsplit(",", maxsplit=4))))
    except FileNotFoundError:
        print(f"Файл {filepath} не найден.")
    return books_values

def write_data(filepath: str, books: list[dict[str, Any]]):
    """Берёт список книг и записывает нужное количесвто"""
    with open(filepath, "w", encoding="utf-8") as file:
        for book in books:
            file.write(f"{book}\n")

def books_generator(filepath:str) -> Iterator[dict[str, Any]]:
    books_keys: str = "title,author,genre,year,isbn"
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for book in file:
                yield dict(zip(books_keys.split(","), book.strip().rsplit(",", maxsplit=4)))
    except FileNotFoundError:
        print(f"Файл {filepath} не найден.")
