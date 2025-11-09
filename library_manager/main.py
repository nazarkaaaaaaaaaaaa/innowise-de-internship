from library_manager import read_data, write_data, search_book
from library_manager.data_loader import books_generator
from library_manager.proccesors import books_iterator, books_filter,  search_year, sorted_books


if __name__ == "__main__":
    """Тестирование задания 1: Загрузка и вывод первых пяти книг"""
    books = read_data("data.txt")
    write_data("result.txt", books[:5])
    """Тестирование задания 2: Поиск и итерация с выводом"""
    print(search_book(books, "Айзек Азимов"))
    for book in books_iterator(books):
        print(book)
    """Тестирование задания 3: Генераторы и функциональные операции на подмножестве книг
    Так же тут есть часть из тестирования интеграции: используйте генератор для загрузки, 
    функциональные операции и циклы для анализа (e.g., подсчёт книг по жанрам 
    с помощью dict и for)"""
    for book in books_generator("data.txt"):
        print(book)
    print(books_filter(books, "Фэнтези"))
    print(search_year(books))
    print(sorted_books(books))
    """Тестирование задания 4: импорт из пакета и тестирование полного 
    пайплайна (загрузка → обработка → сохранение)
    Также задание из тестирования интеграции: примените декоратор к поиску"""
