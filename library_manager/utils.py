import time
from functools import wraps
from typing import Any


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start: float = time.time()
        result: Any = func(*args, **kwargs)
        end: float = time.time()
        print(f"Функция '{func.__name__}' выполнена за {end - start:.6f} секунд")
        return result
    return wrapper
