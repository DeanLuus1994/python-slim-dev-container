"""Optimization utilities for improving code performance.

This subpackage provides functionality for optimizing Python code,
configuring compilers, and improving runtime performance.
"""

from .compiler import setup_ccache, apply_compiler_flags
from .binary import compile_python_bytecode, strip_binaries

__all__ = [
    'setup_ccache', 'apply_compiler_flags',
    'compile_python_bytecode', 'strip_binaries'
]