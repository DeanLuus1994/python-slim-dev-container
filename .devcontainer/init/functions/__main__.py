"""Main entrypoint for the functions module.

This allows running the module directly with: python -m .devcontainer.init.functions
It provides testing and utility functionality for the functions.
"""

import os
import sys
import compileall
from pathlib import Path
from typing import Dict, Any, List
from .resource.detection import detect_resources
from ..core.config.loader import load_config

def precompile_bytecode() -> bool:
    """Compile all Python files in this package to bytecode."""
    print(f"Compiling {__package__} modules to bytecode...")
    success = compileall.compile_dir(
        str(Path(__file__).parent),
        force=True,
        quiet=0,
        legacy=False,
        optimize=2,  # Highest optimization level
        workers=0    # Use all CPU cores
    )
    return bool(success)

def test_resource_detection() -> None:
    """Test resource detection functionality."""
    print("\n=== Testing Resource Detection ===")
    build_config = load_config("build") or {}
    
    resources = detect_resources(build_config)
    
    print(f"\nDetected Resources:")
    print(f"  CPU Cores:      {resources['cores']}")
    print(f"  CPU Threads:    {resources['threads']}")
    print(f"  RAM:            {resources['ram_mb']} MB")
    print(f"  Available RAM:  {resources['available_ram_mb']} MB")
    print(f"  Architecture:   {resources['architecture']}")
    
    if resources['gpu_detected']:
        print(f"  GPU:            {resources['gpu_vendor']}")
        print(f"  GPU Memory:     {resources['gpu_memory_mb']} MB")
    else:
        print("  GPU:            Not detected")

def test_parallel_execution() -> None:
    """Test parallel execution functionality."""
    from .concurrency.executor import get_executor, parallel_map
    
    print("\n=== Testing Parallel Execution ===")
    
    # Create a simple test function
    def square(x: int) -> int:
        import time
        time.sleep(0.1)  # Simulate work
        return x * x
    
    numbers = list(range(10))
    
    print(f"Computing squares of {numbers} in parallel...")
    results = parallel_map(square, numbers)
    
    print(f"Results: {results}")
    print(f"Expected: {[n*n for n in numbers]}")
    print(f"Success: {results == [n*n for n in numbers]}")

def test_optimization() -> None:
    """Test optimization functionality."""
    import tempfile
    from .optimization.binary import compile_python_bytecode
    
    print("\n=== Testing Optimization ===")
    
    # Test bytecode compilation
    print("Testing Python bytecode compilation...")
    python_exec = sys.executable
    success = compile_python_bytecode(python_exec)
    print(f"Bytecode compilation {'succeeded' if success else 'failed'}")

def run_demo() -> None:
    """Run a demonstration of functions module capabilities."""
    print("\n" + "="*70)
    print("FUNCTIONS MODULE CAPABILITIES")
    print("="*70)
    
    # Test resource detection
    test_resource_detection()
    
    print("\n" + "="*70)
    print("AVAILABLE COMMANDS:")
    print("="*70)
    print("1. python -m .devcontainer.init.functions resource - Test resource detection")
    print("2. python -m .devcontainer.init.functions optimize - Test optimization")
    print("3. python -m .devcontainer.init.functions parallel - Test parallel execution")
    print("4. python -m .devcontainer.init.functions compile - Compile all modules to bytecode")

if __name__ == "__main__":
    # Compile bytecode first for better performance
    precompile_bytecode()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "resource":
            test_resource_detection()
        elif command == "optimize":
            test_optimization()
        elif command == "parallel":
            test_parallel_execution()
        elif command == "compile":
            # Just compile to bytecode and exit
            print("Bytecode compilation completed.")
            sys.exit(0)
        else:
            print(f"Unknown command: {command}")
    else:
        run_demo()