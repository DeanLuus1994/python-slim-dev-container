"""Core functionality for the Python slim devcontainer initialization.

This package provides essential system operations, configuration management,
CPU detection, environment handling, and validation utilities.
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

# Import from system subpackage
from .system.cpu import detect_cpu_features, get_cpu_count, get_cpu_info
from .system.memory import get_memory_info
from .system.commands import run_command, has_command
from .system.paths import get_project_root

# Import from config subpackage
from .config.loader import load_config, validate_required_env, get_config_path
from .config.env import (
    load_env_file, setup_env_file, update_env_initialized_flag,
    set_env_from_config
)

# Import from utils subpackage
from .utils.helpers import (
    interpolate_env_vars, format_bytes, dict_deep_merge,
    get_nested_dict_value, load_yaml_config, safe_rmtree
)
from .utils.validation import (
    validate_path, validate_executable, validate_dict_key,
    validate_env_var, ensure_list, safe_call
)

# Import exceptions
from .exceptions import (
    CoreError, ConfigurationError, ValidationError, 
    EnvironmentError, SystemError, ResourceError
)

# Define public API
__all__ = [
    # Metadata
    '__version__', '__author__', '__license__', '__description__', '__url__',
    
    # System & CPU functionality
    'detect_cpu_features', 'get_cpu_count', 'get_cpu_info',
    'get_memory_info', 'run_command', 'has_command',
    'get_project_root',
    
    # Configuration & Environment
    'load_config', 'validate_required_env', 'get_config_path',
    'load_env_file', 'setup_env_file', 'update_env_initialized_flag',
    'set_env_from_config',
    
    # Utility functions
    'interpolate_env_vars', 'format_bytes', 'dict_deep_merge',
    'get_nested_dict_value', 'load_yaml_config', 'safe_rmtree',
    
    # Validation functions
    'validate_path', 'validate_executable', 'validate_dict_key',
    'validate_env_var', 'ensure_list', 'safe_call',
    
    # Exceptions
    'CoreError', 'ConfigurationError', 'ValidationError', 
    'EnvironmentError', 'SystemError', 'ResourceError'
]