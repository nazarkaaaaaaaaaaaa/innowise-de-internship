import time
import gc
import logging

def read_data(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                yield line
    except FileNotFoundError:
        print(f"File {filepath} not found")

def find_products_and_status_200(filepath) -> int:
    counter = 0
    for line in read_data(filepath):
        parts = line.split()
        if parts[7] == "200" and parts[6].startswith("/product/"):
            counter += 1
    return counter

logging.basicConfig(
    filename="task1_sequential.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

if __name__ == "__main__":
    start = time.perf_counter()
    count = find_products_and_status_200("access_logs.txt")
    end = time.perf_counter()
    print(f"Time result: {end-start} seconds")
    print(f"Found {count} logs")
    freed = gc.collect()
    print(f"Freed {freed} objects")
    logging.info(f"Time result: {end-start} seconds")
    logging.info(f"Found {count} logs")
    logging.info(f"Freed {freed} objects")