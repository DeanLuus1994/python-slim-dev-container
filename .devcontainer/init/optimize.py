"""Optimization script for the Python slim devcontainer initialization.

This script precompiles all modules to bytecode and eagerly imports them
for better IDE performance and reduced latency.

Usage:
    python -m .devcontainer.init.optimize [options]

Options:
    --quiet     Minimize output
    --force     Force recompilation even if bytecode is up to date
    --verbose   Show detailed information about each module
    --benchmark Run performance benchmarks after optimization
"""

import os
import sys
import time
import importlib
import pkgutil
import compileall
from pathlib import Path
from typing import Set, Dict, Any, List, Optional, Tuple, Callable

def measure_time(func: Callable) -> Callable:
    """Decorator to measure execution time of a function.
    
    Args:
        func: Function to be measured
        
    Returns:
        Wrapped function that reports execution time
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"{func.__name__} completed in {duration:.2f} seconds")
        return result
    return wrapper

def find_python_modules(start_dir: Path) -> List[Path]:
    """Find all Python modules and packages recursively.
    
    Args:
        start_dir: Directory to start searching from
        
    Returns:
        List of paths to Python modules and packages
    """
    python_files = []
    
    for root, dirs, files in os.walk(start_dir):
        # Skip __pycache__ directories
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')
        
        # Skip hidden directories (starting with .)
        dirs[:] = [d for d in dirs if not d.startswith('.')]
            
        for file in files:
            if file.endswith('.py'):
                python_files.append(Path(root) / file)
                
        # Add directories with __init__.py as package directories
        if '__init__.py' in files:
            python_files.append(Path(root))
            
    return python_files

@measure_time
def compile_bytecode(directory: Path, force: bool = True, quiet: bool = False) -> bool:
    """Compile all Python modules in directory to optimized bytecode.
    
    Args:
        directory: Directory containing Python modules
        force: Force recompilation even if bytecode is up to date
        quiet: Minimize output
        
    Returns:
        True if compilation was successful
    """
    print(f"Compiling modules in {directory} to optimized bytecode...")
    
    # Ensure path exists
    if not directory.exists() or not directory.is_dir():
        print(f"Error: Directory {directory} does not exist")
        return False
        
    # Get count of Python files before compilation
    python_files = list(directory.glob('**/*.py'))
    file_count = len(python_files)
    print(f"Found {file_count} Python files to compile")
    
    # Run compilation with optimizations
    success = compileall.compile_dir(
        str(directory),
        force=force,
        quiet=2 if quiet else 0,
        legacy=False,
        optimize=2,  # Use highest optimization level
        workers=(os.cpu_count() or 1)  # use CPU cores or fallback to 1
    )
    
    # Verify results
    if success:
        # Count the number of .pyc files created
        pyc_dirs = list(directory.glob('**/__pycache__'))
        pyc_count = sum(1 for _ in directory.glob('**/__pycache__/*.pyc'))
        
        print(f"Successfully compiled {pyc_count} bytecode files")
        return True
    else:
        print("Bytecode compilation encountered errors")
        return False

@measure_time
def preload_modules(modules_to_load: List[str], verbose: bool = False) -> Tuple[int, int]:
    """Eagerly import modules to ensure they're loaded into memory.
    
    Args:
        modules_to_load: List of modules to import
        verbose: Whether to print details for each module
        
    Returns:
        Tuple of (successful imports, failed imports)
    """
    print(f"Preloading {len(modules_to_load)} modules...")
    
    loaded = 0
    failed = 0
    loaded_modules = {}
    
    for module_name in modules_to_load:
        try:
            if verbose:
                print(f"  Loading {module_name}...")
                
            # Skip if already loaded
            if module_name in sys.modules:
                if verbose:
                    print(f"  ✓ {module_name} already loaded")
                loaded += 1
                continue
                
            # Import the module
            module = importlib.import_module(module_name)
            loaded_modules[module_name] = module
            loaded += 1
            
            if verbose:
                print(f"  ✓ Successfully loaded {module_name}")
                
            # Try to import submodules if it's a package
            if hasattr(module, '__path__'):
                for _, name, ispkg in pkgutil.iter_modules(module.__path__, module.__name__ + '.'):
                    try:
                        if name not in sys.modules:
                            sub_module = importlib.import_module(name)
                            loaded_modules[name] = sub_module
                            loaded += 1
                            if verbose:
                                print(f"  ✓ Loaded submodule {name}")
                    except ImportError as e:
                        failed += 1
                        if verbose:
                            print(f"  ✗ Failed to load submodule {name}: {e}")
        except ImportError as e:
            failed += 1
            if verbose:
                print(f"  ✗ Failed to load {module_name}: {e}")
                
    return loaded, failed

@measure_time
def run_benchmark() -> Dict[str, float]:
    """Run import speed benchmarks for key modules.
    
    Returns:
        Dictionary of module names and import times in seconds
    """
    print("Running import speed benchmarks...")
    
    # List of modules to benchmark
    modules = [
        '.devcontainer.init',
        '.devcontainer.init.core',
        '.devcontainer.init.functions',
        '.devcontainer.init.log',
        '.devcontainer.init.orchestration'
    ]
    
    results = {}
    
    # Clear modules from sys.modules to ensure fresh imports
    for module in modules:
        if module in sys.modules:
            del sys.modules[module]
            # Also remove submodules
            for name in list(sys.modules.keys()):
                if name.startswith(module + '.'):
                    del sys.modules[name]
    
    # Benchmark each module import
    for module in modules:
        start_time = time.time()
        try:
            importlib.import_module(module)
            end_time = time.time()
            duration = end_time - start_time
            results[module] = duration
            print(f"  {module}: {duration:.4f} seconds")
        except ImportError as e:
            print(f"  ✗ Error importing {module}: {e}")
            results[module] = -1
    
    return results

def optimize_all() -> int:
    """Run full optimization process.
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    # Parse command line arguments
    force = '--force' in sys.argv
    quiet = '--quiet' in sys.argv
    verbose = '--verbose' in sys.argv
    benchmark = '--benchmark' in sys.argv
    
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        return 0
    
    print("\n" + "="*80)
    print(" PYTHON-SLIM OPTIMIZATION UTILITY ".center(80, "="))
    print("="*80 + "\n")
    
    try:
        # Get the root directory of the project
        script_path = Path(__file__)
        init_dir = script_path.parent
        
        # Ensure we're in the right directory
        if not (init_dir / 'core').exists() or not (init_dir / 'functions').exists():
            print(f"Error: Not running from the correct directory.")
            print(f"Expected to find core and functions subdirectories in {init_dir}")
            return 1
        
        # Step 1: Compile all bytecode
        bytecode_success = compile_bytecode(init_dir, force=force, quiet=quiet)
        if not bytecode_success and not force:
            print("Warning: Bytecode compilation had issues. Continuing anyway...")
        
        # Step 2: Preload core modules
        core_modules = [
            '.devcontainer.init',
            '.devcontainer.init.core',
            '.devcontainer.init.core.config',
            '.devcontainer.init.core.system',
            '.devcontainer.init.core.utils',
            '.devcontainer.init.functions',
            '.devcontainer.init.functions.resource',
            '.devcontainer.init.functions.optimization',
            '.devcontainer.init.functions.vcs',
            '.devcontainer.init.functions.ui',
            '.devcontainer.init.functions.concurrency',
            '.devcontainer.init.log',
            '.devcontainer.init.orchestration'
        ]
        
        loaded, failed = preload_modules(core_modules, verbose=verbose)
        
        print(f"\nOptimization Summary:")
        print(f"  - Successfully loaded: {loaded} modules")
        if failed > 0:
            print(f"  - Failed to load: {failed} modules")
        
        # Step 3: Run benchmarks if requested
        if benchmark:
            print("\nBenchmarking import performance...")
            benchmark_results = run_benchmark()
            print("\nImport Speed Benchmarks:")
            for module, duration in benchmark_results.items():
                if duration > 0:
                    print(f"  {module}: {duration:.4f} seconds")
        
        print("\n" + "="*80)
        print(" OPTIMIZATION COMPLETE ".center(80, "="))
        print("="*80 + "\n")
        
        return 0
    except Exception as e:
        print(f"Error during optimization: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(optimize_all())