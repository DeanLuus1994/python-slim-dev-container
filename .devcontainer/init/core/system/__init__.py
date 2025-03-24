"""System-related utilities for hardware detection and system operations.

This subpackage provides functionality for detecting hardware capabilities,
executing system commands, and managing system resources.
"""

from .cpu import detect_cpu_features, get_cpu_count, get_cpu_info
from .memory import get_memory_info
from .commands import run_command, has_command
from .paths import get_project_root

__all__ = [
    # CPU detection
    'detect_cpu_features', 'get_cpu_count', 'get_cpu_info',
    
    # Memory detection
    'get_memory_info',
    
    # Command execution
    'run_command', 'has_command',
    
    # Path operations
    'get_project_root'
]