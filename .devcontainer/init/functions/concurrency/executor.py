"""Executor utilities for parallel processing."""

import os
import threading
import concurrent.futures
from typing import List, Callable, TypeVar, Dict, Any, Iterable, Optional, Tuple, Union
from ...log.logger import get_logger
from ..exceptions import ConcurrencyError

logger = get_logger()
T = TypeVar('T')
R = TypeVar('R')

# Global registry of executors
_executor_lock = threading.Lock()
_executors: Dict[str, concurrent.futures.Executor] = {}

def get_optimal_workers(task_type: str = "io") -> int:
    """Determine optimal number of worker threads/processes.
    
    Args:
        task_type: Type of task ("io" or "cpu")
        
    Returns:
        Optimal number of workers
    """
    try:
        cpu_count = os.cpu_count() or 4
        if task_type.lower() == "cpu":
            # For CPU-bound tasks, leave one core free for system
            return max(1, cpu_count - 1)
        elif task_type.lower() == "io":
            # For I/O-bound tasks, use more workers
            return cpu_count * 2
        else:
            # Default to number of cores
            return cpu_count
    except Exception as e:
        logger.warning(f"Error determining optimal workers: {e}")
        return 4  # Reasonable fallback

def get_executor(name: str, executor_type: str = "thread", 
                workers: int = 0) -> concurrent.futures.Executor:
    """Get or create a thread or process executor.
    
    Args:
        name: Unique name for the executor
        executor_type: Type of executor ("thread" or "process")
        workers: Number of workers, or 0 for auto-detect
        
    Returns:
        Executor instance
        
    Raises:
        ConcurrencyError: If an invalid executor_type is specified
    """
    with _executor_lock:
        # Return existing executor if available and not shutdown
        if name in _executors:
            try:
                # Check if executor is still usable
                executor = _executors[name]
                # Safely check shutdown state
                if not hasattr(executor, '_shutdown') or not getattr(executor, '_shutdown', False):
                    return executor
            except Exception:
                # If there's any issue checking the executor, create a new one
                pass
        
        # Clean up existing executor if it exists
        if name in _executors:
            try:
                _executors[name].shutdown(wait=False)
            except Exception:
                pass
            
        # Create appropriate executor type
        if executor_type.lower() == "process":
            worker_count = workers if workers > 0 else get_optimal_workers("cpu")
            logger.debug(f"Creating process pool '{name}' with {worker_count} workers")
            _executors[name] = concurrent.futures.ProcessPoolExecutor(
                max_workers=worker_count
            )
        elif executor_type.lower() == "thread":
            worker_count = workers if workers > 0 else get_optimal_workers("io")
            logger.debug(f"Creating thread pool '{name}' with {worker_count} workers")
            _executors[name] = concurrent.futures.ThreadPoolExecutor(
                max_workers=worker_count,
                thread_name_prefix=name
            )
        else:
            raise ConcurrencyError(f"Invalid executor type: {executor_type}")
            
        return _executors[name]

def parallel_map(func: Callable[[T], R], items: Iterable[T], 
                executor_name: str = "default",
                executor_type: str = "thread",
                workers: int = 0,
                timeout: Optional[float] = None,
                chunk_size: int = 1) -> List[R]:
    """Execute a function on multiple items in parallel.
    
    Args:
        func: Function to execute
        items: Items to process
        executor_name: Name of executor to use
        executor_type: Type of executor ("thread" or "process")
        workers: Number of workers, or 0 for auto-detect
        timeout: Maximum execution time in seconds
        chunk_size: Number of items to process per task (for process pools)
        
    Returns:
        List of results
        
    Raises:
        ConcurrencyError: If execution fails
        TimeoutError: If execution times out
    """
    # Convert items to list to ensure we can iterate multiple times
    items_list = list(items)
    if not items_list:
        return []
        
    # Get or create appropriate executor
    executor = get_executor(executor_name, executor_type, workers)
    results = []
    errors = []
    
    try:
        # Submit all tasks and collect futures
        futures = {executor.submit(func, item): item for item in items_list}
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(futures, timeout=timeout):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                item = futures[future]
                errors.append((item, e))
                logger.error(f"Error processing {item}: {e}")
    except concurrent.futures.TimeoutError:
        pending_count = sum(1 for f in futures if not f.done())
        logger.error(f"Parallel execution timed out after {timeout} seconds "
                     f"with {pending_count} pending tasks")
        raise ConcurrencyError(f"Execution timed out after {timeout} seconds")
    finally:
        # Don't shutdown executor here as it might be reused
        pass
        
    if errors:
        logger.warning(f"{len(errors)} tasks failed during parallel execution")
        
    return results

def execute_with_timeout(func: Callable[..., R], 
                        args: Tuple = (), 
                        kwargs: Optional[Dict[str, Any]] = None,
                        timeout: float = 60.0) -> R:
    """Execute a function with a timeout.
    
    Args:
        func: Function to execute
        args: Positional arguments for the function
        kwargs: Keyword arguments for the function
        timeout: Timeout in seconds
        
    Returns:
        Result of the function
        
    Raises:
        TimeoutError: If execution times out
    """
    if kwargs is None:
        kwargs = {}
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func, *args, **kwargs)
        try:
            return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            future.cancel()
            raise TimeoutError(f"Function {func.__name__} timed out after {timeout} seconds")

def shutdown_executors() -> None:
    """Shut down all executor instances gracefully."""
    with _executor_lock:
        logger.debug(f"Shutting down {len(_executors)} executors")
        for name, executor in list(_executors.items()):
            try:
                logger.debug(f"Shutting down executor '{name}'")
                executor.shutdown(wait=False)
            except Exception as e:
                logger.warning(f"Error shutting down executor '{name}': {e}")
        _executors.clear()