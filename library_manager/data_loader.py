from typing import Any, Iterator


def read_data() -> list[dict[str, Any]]:
    """Ищет необходимый файл data.txt и считывает данные из него"""
    books_keys: str = "title,author,genre,year,isbn"
    books_values: list = []
    try:
        file = open("data.txt", "r", encoding="utf-8")
        data_values: list[str] = file.readlines()
        file.close()
        for book in data_values:
            book_values = book.strip().rsplit(",", maxsplit=4)
            book_values[-2] = int(book_values[-2])
            books_values.append(dict(zip(books_keys.split(","), book_values)))
    except FileNotFoundError:
        print("Файл 'data.txt' не найден.")
    return books_values

def write_data(books: list[dict[str, Any]], count_of_books: int):
    """Берёт список книг и записывает нужное количесвто"""
    file = open("data1.txt", "w+", encoding="utf-8")
    books = books[:count_of_books]
    for book in books:
        file.write(f"{book['title']},{book['author']},{book['genre']},"
                   f"{str(book['year'])},{book['isbn']}\n")
    file.close()

def generator(books: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:
    for book in books:
        yield book
