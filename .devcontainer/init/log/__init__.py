"""Logging utilities for the DevContainer initialization process.

This package provides logging functionality with colorized output
and standardized log formatting.
"""

import os
import sys
import logging
import importlib
import compileall
from pathlib import Path

# Eagerly import all modules
from .logger import get_logger
from .formatter import ColorFormatter

__all__ = [
    'get_logger',
    'ColorFormatter'
]

# Compile to bytecode at import time for better performance
compileall.compile_dir(
    str(Path(__file__).parent),
    force=True,
    quiet=1,
    optimize=2
)

# Define module-level logger
logger = get_logger(__name__)