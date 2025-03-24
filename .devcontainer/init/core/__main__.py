"""Main entrypoint for the core module.

This allows running the module directly with: python -m .devcontainer.init.core
It provides code quality assessment and debugging tools.
"""

import os
import sys
import importlib
import inspect
import pkgutil
import compileall
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Tuple

def check_type_annotations() -> Tuple[int, List[str]]:
    """Check for proper type annotations in all module functions."""
    import inspect
    from . import __all__ as exposed_items
    
    module_names = [
        name for _, name, _ in pkgutil.iter_modules([str(Path(__file__).parent)])
        if not name.startswith('__')
    ]
    
    missing = []
    total_functions = 0
    
    for module_name in module_names:
        module = importlib.import_module(f".{module_name}", package=__package__)
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and not name.startswith('_'):
                total_functions += 1
                signature = inspect.signature(obj)
                
                # Check return annotation
                if signature.return_annotation == inspect.Signature.empty:
                    missing.append(f"{module_name}.{name} missing return type")
                
                # Check parameter annotations
                for param_name, param in signature.parameters.items():
                    if param.annotation == inspect.Signature.empty:
                        missing.append(
                            f"{module_name}.{name} parameter '{param_name}' missing type"
                        )
    
    return total_functions, missing

def check_docstrings() -> Tuple[int, List[str]]:
    """Check for docstrings in all module functions."""
    module_names = [
        name for _, name, _ in pkgutil.iter_modules([str(Path(__file__).parent)])
        if not name.startswith('__')
    ]
    
    missing = []
    total_functions = 0
    
    for module_name in module_names:
        module = importlib.import_module(f".{module_name}", package=__package__)
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and not name.startswith('_'):
                total_functions += 1
                if not obj.__doc__:
                    missing.append(f"{module_name}.{name} missing docstring")
    
    return total_functions, missing

def check_imports() -> List[str]:
    """Check for unused or missing imports."""
    try:
        import pyflakes.api
        import pyflakes.reporter
        
        module_names = [
            name for _, name, _ in pkgutil.iter_modules([str(Path(__file__).parent)])
            if not name.startswith('__')
        ]
        
        issues = []
        for module_name in module_names:
            module_path = Path(__file__).parent / f"{module_name}.py"
            if module_path.exists():
                reporter = pyflakes.reporter.Reporter(issues.append, issues.append)
                pyflakes.api.checkPath(str(module_path), reporter)
        
        return issues
    except ImportError:
        return ["pyflakes not installed, skipping import checks"]

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

def run_quality_checks() -> None:
    """Run all quality checks and report findings."""
    print(f"\n{'-'*70}")
    print(f"CODE QUALITY ASSESSMENT FOR {__package__}")
    print(f"{'-'*70}\n")
    
    print("Checking type annotations...")
    total_funcs, missing_types = check_type_annotations()
    if missing_types:
        print(f"⚠ Missing type annotations ({len(missing_types)}/{total_funcs} functions):")
        for item in missing_types:
            print(f"  - {item}")
    else:
        print(f"✓ All {total_funcs} functions have complete type annotations\n")
    
    print("\nChecking docstrings...")
    total_funcs, missing_docs = check_docstrings()
    if missing_docs:
        print(f"⚠ Missing docstrings ({len(missing_docs)}/{total_funcs} functions):")
        for item in missing_docs:
            print(f"  - {item}")
    else:
        print(f"✓ All {total_funcs} functions have docstrings\n")
    
    try:
        from importlib.metadata import version
        print("\nPackage Dependencies:")
        for pkg in ["pyyaml", "typing_extensions"]:
            try:
                print(f"  - {pkg}: {version(pkg)}")
            except:
                print(f"  - {pkg}: not installed")
    except:
        pass
    
    print(f"\n{'-'*70}")
    print("RECOMMENDATIONS FOR IMPROVEMENT:")
    print(f"{'-'*70}")
    print("1. Install development tools: pip install pylint mypy black isort")
    print("2. Run type checker: mypy .devcontainer/init/core")
    print("3. Run linter: pylint .devcontainer/init/core")
    print("4. Format code: black .devcontainer/init/core")
    print("5. Sort imports: isort .devcontainer/init/core")
    print(f"{'-'*70}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "compile":
        # Just compile to bytecode and exit
        success = precompile_bytecode()
        sys.exit(0 if success else 1)
    else:
        # Compile bytecode first for better performance
        precompile_bytecode()
        # Then run quality checks
        run_quality_checks()