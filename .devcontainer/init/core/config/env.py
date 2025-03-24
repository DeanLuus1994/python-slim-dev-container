"""Environment variable handling utilities."""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from ...log.logger import get_logger
from ..utils.validation import validate_path, validate_dict_key

logger = get_logger()

def load_env_file(env_path: Path) -> Dict[str, str]:
    """Load environment variables from a file.
    
    Args:
        env_path: Path to the .env file
        
    Returns:
        Dictionary of environment variables
    """
    env_vars = {}
    try:
        env_path = validate_path(env_path, must_exist=True)
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                try:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
                except ValueError:
                    continue
    except FileNotFoundError:
        logger.warning(f"Environment file not found: {env_path}")
    except Exception as e:
        logger.error(f"Error loading env file {env_path}: {e}")
    return env_vars

def setup_env_file(project_root: Path) -> Optional[Path]:
    """Set up the environment file, copying from example if needed.
    
    Args:
        project_root: Project root directory
        
    Returns:
        Path to the environment file, or None if setup failed
    """
    try:
        project_root = validate_path(project_root, must_exist=True)
        example_env_path = project_root / '.devcontainer' / 'init' / 'example.env'
        root_env_path = project_root / '.env'
        
        if not root_env_path.exists() and example_env_path.exists():
            logger.info("Creating .env file from example")
            shutil.copy(example_env_path, root_env_path)
            update_env_initialized_flag(root_env_path, True)
            return root_env_path
        elif not example_env_path.exists():
            logger.warning("example.env not found")
            
        return root_env_path if root_env_path.exists() else None
    except Exception as e:
        logger.error(f"Error setting up env file: {e}")
        return None

def update_env_initialized_flag(env_path: Path, initialized: bool = True) -> bool:
    """Update the INITIALIZED flag in the environment file.
    
    Args:
        env_path: Path to the .env file
        initialized: Value to set for the INITIALIZED flag
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if env_path.exists():
            content = []
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith('INITIALIZED='):
                        content.append(f'INITIALIZED={"true" if initialized else "false"}\n')
                    else:
                        content.append(line)
            
            with open(env_path, 'w') as f:
                f.writelines(content)
            return True
        return False
    except Exception as e:
        logger.error(f"Error updating INITIALIZED flag: {e}")
        return False

def set_env_from_config(config: Dict[str, Any], prefix: str = "") -> int:
    """Set environment variables from a configuration dictionary.
    
    Args:
        config: Configuration dictionary
        prefix: Prefix for environment variable names
        
    Returns:
        Number of environment variables set
    """
    if not isinstance(config, dict):
        return 0
        
    count = 0
    try:
        def _flatten_dict(d: Dict[str, Any], parent_key: str = "") -> Dict[str, Any]:
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}_{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(_flatten_dict(v, new_key).items())
                else:
                    items.append((new_key, v))
            return dict(items)
            
        flattened = _flatten_dict(config)
        for key, value in flattened.items():
            env_key = f"{prefix}_{key}".upper() if prefix else key.upper()
            if isinstance(value, (list, tuple)):
                value = ",".join(str(x) for x in value)
            elif not isinstance(value, str):
                value = str(value)
                
            os.environ[env_key] = value
            count += 1
    except Exception as e:
        logger.error(f"Error setting environment variables: {e}")
        
    return count