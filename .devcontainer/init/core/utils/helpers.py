"""Helper functions for common operations."""

import os
import re
import math
import logging
import yaml
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

def interpolate_env_vars(text: str) -> str:
    """Replace environment variable placeholders in a string.
    
    Args:
        text: String with ${VAR} placeholders
        
    Returns:
        String with placeholders replaced by environment variable values
    """
    pattern = r'\$\{([^}^{]+)\}'
    
    def replace_var(match):
        env_var = match.group(1)
        val = os.environ.get(env_var)
        if val is None:
            parts = env_var.split(':-')
            if len(parts) == 2:
                env_name, default = parts
                val = os.environ.get(env_name, default)
            else:
                val = match.group(0)
        return val
        
    return re.sub(pattern, replace_var, text)

def format_bytes(size_bytes: int) -> str:
    """Format bytes as a human-readable string.
    
    Args:
        size_bytes: Number of bytes
        
    Returns:
        Human-readable string (e.g., "1.5 MB")
    """
    if size_bytes == 0:
        return "0B"
        
    size_name = ("B", "KB", "MB", "GB", "TB", "PB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_name[i]}"

def load_yaml_config(config_path: Path) -> Dict[str, Any]:
    """Load a YAML configuration file.
    
    Args:
        config_path: Path to the YAML file
        
    Returns:
        Dictionary with the configuration, or empty dict if not found
    """
    if not config_path.exists():
        return {}
        
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        logging.getLogger("devcontainer_init").error(
            f"Error loading YAML config {config_path}: {e}"
        )
        return {}

def get_nested_dict_value(d: Dict[str, Any], keys: List[str], 
                         default: Any = None) -> Any:
    """Get a value from a nested dictionary using a list of keys.
    
    Args:
        d: Dictionary to look in
        keys: List of keys to traverse
        default: Value to return if key not found
        
    Returns:
        Value from the dictionary or default
    """
    if not isinstance(d, dict) or not keys:
        return default
        
    current = d
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
        
    return current

def safe_rmtree(path: Path) -> bool:
    """Safely remove a directory tree.
    
    Args:
        path: Path to remove
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
        return True
    except Exception as e:
        logging.getLogger("devcontainer_init").error(
            f"Error removing directory {path}: {e}"
        )
        return False

def dict_deep_merge(base: Dict[str, Any], 
                   override: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two dictionaries with nested dictionary support.
    
    Args:
        base: Base dictionary
        override: Dictionary with values to override
        
    Returns:
        New merged dictionary
    """
    result = base.copy()
    
    for key, value in override.items():
        if (key in result and isinstance(result[key], dict) 
                and isinstance(value, dict)):
            result[key] = dict_deep_merge(result[key], value)
        else:
            result[key] = value
            
    return result