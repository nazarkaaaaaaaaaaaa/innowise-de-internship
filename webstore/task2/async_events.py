import asyncio
import json
import random
import time
import logging
import gc

logging.basicConfig(
    filename="async_events.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

async def create(queue, count):
    for i in range(count):
        await queue.put({
            "user_id": i+1,
            "event_type": random.choice(("view", "add_to_cart", "purchase")),
            "timestamp": time.time()
        })

async def worker(queue, counter, lock):
    while True:
        try:
            item = await queue.get()
            async with lock:
                counter[item["event_type"]] += 1
            queue.task_done()
        except asyncio.CancelledError:
            break

async def timer(counter, lock):
    while True:
        await asyncio.sleep(10)
        async with lock:
            snapshot = counter.copy()
            with open("info.json", "w", encoding="utf-8") as f:
                json.dump(snapshot, f, indent=2)
            logging.info(f"Final count {counter}")
            for key in counter:
                counter[key] = 0

async def main():
    queue = asyncio.Queue()
    counter = {"view": 0, "add_to_cart": 0, "purchase": 0}
    lock = asyncio.Lock()
    workers = []
    for _ in range(5):
        workers.append(asyncio.create_task(worker(queue, counter, lock)))
    timer_task = asyncio.create_task(timer(counter, lock))
    await create(queue, random.randint(150_000, 200_000))
    await queue.join()
    await asyncio.sleep(10.5)
    for w in workers:
        w.cancel()
    timer_task.cancel()
    await asyncio.gather(*workers, timer_task, return_exceptions=True)
    collected = gc.collect()
    tracked = len(gc.get_objects())
    logging.info(f"Garbage collection complete: objects deleted = {collected}, tracked objects remaining = {tracked}")
    print(f"Garbage collection complete: objects deleted = {collected}, tracked objects remaining = {tracked}")

if __name__ == '__main__':
    asyncio.run(main())
