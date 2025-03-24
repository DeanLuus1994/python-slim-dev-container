"""Concurrency utilities for parallel processing.

This subpackage provides utilities for executing tasks in parallel,
managing thread and process pools, and coordinating concurrent operations.
"""

from .executor import (
    get_optimal_workers, get_executor, 
    parallel_map, shutdown_executors
)

__all__ = [
    'get_optimal_workers', 'get_executor',
    'parallel_map', 'shutdown_executors'
]