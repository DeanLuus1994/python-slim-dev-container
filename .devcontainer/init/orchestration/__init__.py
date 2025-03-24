"""Orchestration utilities for coordinating initialization processes.

This package provides high-level components that orchestrate the various
initialization tasks like Python optimization and GitHub provisioning.
"""

import os
import sys
import importlib
import compileall
from pathlib import Path

# Eagerly import all modules
from .python_optimizer import PythonOptimizer
from .github_provisioner import main as github_provision
from .repository_manager import (
    check_repository_status, manage_repository, manage_repositories
)

__all__ = [
    'PythonOptimizer',
    'github_provision',
    'check_repository_status',
    'manage_repository',
    'manage_repositories'
]

# Compile to bytecode at import time for better performance
compileall.compile_dir(
    str(Path(__file__).parent),
    force=True,
    quiet=1,
    optimize=2
)