"""Function utilities for the Python slim devcontainer.

This package provides higher-level utilities built on top of the core module,
including resource detection, code optimization, version control integration,
and user interface components.
"""

import os
import sys
import importlib
import compileall
from pathlib import Path

# Compile package to bytecode at import time for better performance
_package_dir = Path(__file__).parent
compileall.compile_dir(
    str(_package_dir),
    force=True,
    quiet=1,
    optimize=2
)

# Package metadata
from .__about__ import (
    __version__, __author__, __license__,
    __description__, __url__
)

# Import from resource subpackage
from .resource.detection import detect_resources, log_resources
from .resource.gpu import detect_gpu, setup_gpu_env

# Import from optimization subpackage
from .optimization.compiler import setup_ccache, apply_compiler_flags
from .optimization.binary import compile_python_bytecode, strip_binaries

# Import from vcs subpackage
from .vcs.git import setup_git_config, clone_or_update_repo, setup_lfs
from .vcs.repository import process_solution_repo, process_local_repos

# Import from ui subpackage
from .ui.prompt import (
    display_env_prompt, edit_env_file, color_text, green, yellow, blue
)

# Import from concurrency subpackage
from .concurrency.executor import (
    get_optimal_workers, get_executor, parallel_map, shutdown_executors
)

# Import exceptions
from .exceptions import (
    FunctionError, ResourceError, OptimizationError,
    RepositoryError, ConcurrencyError, UserInteractionError
)

__all__ = [
    # Metadata
    '__version__', '__author__', '__license__', '__description__', '__url__',
    
    # Resource detection
    'detect_resources', 'log_resources', 'detect_gpu', 'setup_gpu_env',
    
    # Optimization
    'setup_ccache', 'apply_compiler_flags', 'compile_python_bytecode', 'strip_binaries',
    
    # Version control
    'setup_git_config', 'clone_or_update_repo', 'setup_lfs',
    'process_solution_repo', 'process_local_repos',
    
    # User interface
    'display_env_prompt', 'edit_env_file', 'color_text', 'green', 'yellow', 'blue',
    
    # Concurrency
    'get_optimal_workers', 'get_executor', 'parallel_map', 'shutdown_executors',
    
    # Exceptions
    'FunctionError', 'ResourceError', 'OptimizationError',
    'RepositoryError', 'ConcurrencyError', 'UserInteractionError'
]