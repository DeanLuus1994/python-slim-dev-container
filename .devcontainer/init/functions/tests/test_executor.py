import time
import pytest
from ..concurrency.executor import get_executor, parallel_map, shutdown_executors

def test_get_executor_thread():
    # Get a thread pool executor and verify basic properties.
    executor = get_executor("test_executor", executor_type="thread", workers=2)
    assert executor is not None
    # Submit a trivial function
    future = executor.submit(lambda x: x + 1, 1)
    result = future.result(timeout=1)
    assert result == 2
    shutdown_executors()

def test_parallel_map():
    # Define a simple function to square numbers with a small delay.
    def square(x: int) -> int:
        time.sleep(0.05)
        return x * x

    items = list(range(5))
    results = parallel_map(square, items, executor_name="parallel_test", executor_type="thread", workers=3)
    expected = [x * x for x in items]
    assert results == expected

def test_executor_reuse():
    # Ensure multiple calls with the same name return the same executor.
    executor1 = get_executor("reuse_executor", executor_type="thread", workers=2)
    executor2 = get_executor("reuse_executor", executor_type="thread", workers=4)
    assert executor1 is executor2
    shutdown_executors()