"""Configuration management for the initialization process.

This subpackage provides utilities for loading configuration from files,
handling environment variables, and managing build settings.
"""

from .loader import load_config, validate_required_env, get_config_path
from .env import (
    load_env_file, setup_env_file, update_env_initialized_flag, 
    set_env_from_config
)

__all__ = [
    # Config loading
    'load_config', 'validate_required_env', 'get_config_path',
    
    # Environment management
    'load_env_file', 'setup_env_file', 'update_env_initialized_flag',
    'set_env_from_config'
]