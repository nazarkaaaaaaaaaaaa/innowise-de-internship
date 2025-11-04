from library_manager import *
from library_manager.data_loader import generator
from library_manager.proccesors import books_iterator
from library_manager.proccesors import books_filter
from library_manager.proccesors import search_year
from library_manager.proccesors import sorted_books


"""Тестирование задания 1: Загрузка и вывод первых пяти книг"""
books = read_data()
write_data(books, 5)
"""Тестирование задания 2: Поиск и итерация с выводом"""
search_book(books, "Айзек Азимов")
iterator = books_iterator(books)
try:
    print(next(iterator))
    print(next(iterator))
except StopIteration:
    print("В итераторе меньше двух книг")

"""Тестирование задания 3: Генераторы и функциональные операции на подмножестве книг
Так же тут есть часть из тестирования интеграции: используйте генератор для загрузки, 
функциональные операции и циклы для анализа (e.g., подсчёт книг по жанрам 
с помощью dict и for)"""
for book in generator(books):
    print(book)
print(books_filter(books, "Фэнтези"))
print(search_year(books))
print(sorted_books(books))
"""Тестирование задания 4: импорт из пакета и тестирование полного 
пайплайна (загрузка → обработка → сохранение)
Также задание из тестирования интеграции: примените декоратор к поиску"""
new_books = read_data()
new_books = books_filter(new_books, "Фэнтези")
# Сначала проверял запись первых 5 книг, поэтому закомментировал этот вывод
# write_data(new_books, len(new_books))
