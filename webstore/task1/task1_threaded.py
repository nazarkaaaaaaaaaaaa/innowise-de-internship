import gc
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Generator

def read_data(filepath: str) -> Generator[list[str]]:
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            block = []
            for line in file:
                block.append(line)
                if len(block) >= 5000:
                    yield block
                    block = []
            if block:
                yield block
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filepath} not found for processing.")

def find_products_and_status_200(block) -> int:
    counter: int = 0
    for line in block:
        parts: list[str] = line.split()
        if (parts[7] == "200") and parts[6].startswith("/product/"):
            counter += 1
    return counter

def run_threads():
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = (
            executor.submit(find_products_and_status_200, block)
            for block in read_data("access_logs.txt")
        )
        return sum(f.result() for f in as_completed(futures))

logging.basicConfig(
    filename="task1_threaded.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

if __name__ == "__main__":
    start = time.perf_counter()
    result = run_threads()
    end = time.perf_counter()
    print(f"{end - start}")
    print(f"Found {result} logs")
    freed = gc.collect()
    print(f"Freed {freed} objects")
    logging.info(f"Time result: {end - start} seconds")
    logging.info(f"Found {result} logs")
    logging.info(f"Freed {freed} objects")