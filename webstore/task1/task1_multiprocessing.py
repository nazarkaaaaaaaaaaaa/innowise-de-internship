import gc
import logging
import time
from concurrent.futures import ProcessPoolExecutor

def read_data(filepath: str) -> list[str]:
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
        print(f"File {filepath} not found")

def find_products_and_status_200(block) -> int:
    counter = 0
    for line in block:
        parts = line.split()
        if parts[7] == "200" and parts[6].startswith("/product/"):
            counter += 1
    return counter

def run_processes():
    with ProcessPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(find_products_and_status_200, read_data("access_logs.txt")))
        return sum(results)

logging.basicConfig(
    filename="task1_multiprocessing.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

if __name__ == "__main__":
    start = time.perf_counter()
    result = run_processes()
    end = time.perf_counter()
    print(f"{end - start}")
    print(f"Found {result} logs")
    freed = gc.collect()
    print(f"Freed {freed} objects")
    logging.info(f"Time result: {end - start} seconds")
    logging.info(f"Found {result} logs")
    logging.info(f"Freed {freed} objects")
