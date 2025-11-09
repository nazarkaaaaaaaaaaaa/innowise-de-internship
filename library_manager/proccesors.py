from typing import Any, Iterator
from library_manager.utils import measure_time


@measure_time
def search_book(books: list[dict[str, Any]], author: str) -> list[dict[str, Any]]:
    """Функция поиска книги по автору"""
    searched_books: list = []
    for index, book in enumerate(books):
        if book["author"].lower() == author.lower():
            searched_books.append(dict({"index": index + 1,"title": book["title"]}))
    return searched_books

def books_iterator(books: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:
    return iter(books)

def books_filter(books: list[dict[str, Any]], genre: str) -> list[dict[str, Any]]:
    return list(filter(lambda book: book["genre"] == genre, books))

def search_year(books: list[dict[str, Any]]) -> list[int]:
    return list(map(lambda book: int(book["year"]), books))

def sorted_books(books: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return list(sorted(books, key=lambda book: book["year"]))
