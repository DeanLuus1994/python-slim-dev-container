"""Configuration loading and validation utilities."""

import os
import yaml
from typing import Dict, Any, List, Optional
from pathlib import Path
from ...log.logger import get_logger
from ..utils.validation import validate_path, validate_dict_key
from ..utils.helpers import interpolate_env_vars

logger = get_logger()

def load_config(config_name: str) -> Dict[str, Any]:
    """Load configuration from the config.yaml file.
    
    Args:
        config_name: Section of the config to load
        
    Returns:
        Dictionary with the configuration, or empty dict if not found
    """
    try:
        project_root = Path(os.environ.get("PROJECT_ROOT", "/")).resolve()
        config_file = project_root / '.devcontainer' / 'container' / 'config.yaml'
        
        if not config_file.exists():
            logger.warning(f"Config file {config_file} not found")
            return {}
            
        with open(config_file, 'r') as f:
            config_str = interpolate_env_vars(f.read())
            
        config = yaml.safe_load(config_str) or {}
        section = validate_dict_key(config, config_name, {})
        
        if config and not section and config_name:
            logger.warning(f"Section '{config_name}' not found in config.yaml")
            
        return section
    except Exception as e:
        logger.error(f"Error loading config {config_name}: {e}")
        return {}

def validate_required_env(config: Dict[str, Any], section: str) -> List[str]:
    """Check if required environment variables are present.
    
    Args:
        config: Configuration dictionary
        section: Section to check for required_env
        
    Returns:
        List of missing environment variables
    """
    if not isinstance(config, dict) or not isinstance(section, str):
        return []
        
    missing = []
    section_data = validate_dict_key(config, section, {})
    required_env = validate_dict_key(section_data, "required_env", [])
    
    if required_env:
        for var in required_env:
            if var not in os.environ or not os.environ[var]:
                missing.append(var)
                
    return missing

def get_config_path(config: Dict[str, Any], path_key: str, 
                   default: str = "") -> Optional[Path]:
    """Get a path from the configuration and ensure it exists.
    
    Args:
        config: Configuration dictionary
        path_key: Key to look up in the paths section
        default: Default path if not found in config
        
    Returns:
        Path object or None if path couldn't be created
    """
    if "paths" not in config:
        return None
        
    path_str = validate_dict_key(config["paths"], path_key, default)
    if not path_str:
        return None
        
    try:
        return validate_path(path_str, create_dir=True)
    except Exception as e:
        logger.error(f"Error creating path for {path_key}: {e}")
        return None