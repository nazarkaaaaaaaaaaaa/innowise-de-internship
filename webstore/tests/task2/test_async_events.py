import unittest
from unittest.mock import patch
import asyncio
from webstore.task2.async_events import create, worker


class TestSimpleAsyncUnits(unittest.IsolatedAsyncioTestCase):
    async def test_1_create_generates_correct_count(self):
        """
        Tests that the 'create' coroutine generates the specified number of
        events and that the first generated event has the correct structure (user_id=1).
        """
        queue = asyncio.Queue()
        expected_count = 15
        await create(queue, expected_count)
        self.assertEqual(queue.qsize(), expected_count,
                         f"Excepted {expected_count} elements, get {queue.qsize()}")
        item = await queue.get()
        self.assertEqual(item.get("user_id"), 1)

    async def test_2_worker_processes_single_event_type(self):
        """
        Tests that the 'worker' coroutine correctly processes a single type of event
        and increments the corresponding counter, while leaving others unchanged.
        Uses mocking to simulate the event retrieval and trigger task cancellation.
        """
        queue = asyncio.Queue()
        counter = {"view": 0, "add_to_cart": 0, "purchase": 0}
        lock = asyncio.Lock()
        test_event = {"event_type": "purchase"}
        with patch.object(queue, 'get', side_effect=[test_event, asyncio.CancelledError]):
            worker_task = asyncio.create_task(worker(queue, counter, lock))
            await asyncio.sleep(0.001)
            worker_task.cancel()
            await asyncio.gather(worker_task, return_exceptions=True)
        self.assertEqual(1, counter.get("purchase"), "Conter 'purchase' should be 1.")
        self.assertEqual(0, counter.get("view"), "Other counters chould be 0.")

    async def test_3_worker_processes_mixed_events(self):
        """
        Tests that the 'worker' coroutine correctly handles and aggregates multiple,
        mixed event types (e.g., 'view', 'add_to_cart') and updates the shared
        'counter' dictionary atomically using the asyncio.Lock.
        """
        queue = asyncio.Queue()
        counter = {"view": 0, "add_to_cart": 0, "purchase": 0}
        lock = asyncio.Lock()
        events_list = [
            {"event_type": "view"},
            {"event_type": "view"},
            {"event_type": "add_to_cart"},
        ]
        # Simulate feeding the queue with events, followed by termination signal
        side_effects = events_list + [asyncio.CancelledError]
        with patch.object(queue, 'get', side_effect=side_effects), \
                patch.object(queue, 'task_done', return_value=None):
            worker_task = asyncio.create_task(worker(queue, counter, lock))
            try:
                # Use wait_for to ensure the worker starts and processes the mocked items
                await asyncio.wait_for(worker_task, timeout=1.0)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass
            finally:
                if not worker_task.done():
                    worker_task.cancel()
                    await asyncio.gather(worker_task, return_exceptions=True)
        self.assertEqual(2, counter["view"])
        self.assertEqual(1, counter["add_to_cart"])
        self.assertEqual(0, counter["purchase"])

if __name__ == '__main__':
    unittest.main()
