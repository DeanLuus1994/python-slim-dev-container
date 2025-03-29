"""Debug configuration handling."""

import os
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Union, List

class DebugConfig:
    """Debug configuration management.
    
    This class handles loading debug configuration from environment
    variables and configuration files.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize debug configuration.
        
        Args:
            config_path: Path to debug config YAML (optional)
        """
        # Default configuration
        self._config = {
            'debug_mode': False,
            'profile_mode': 'none',
            'debug_level': 'INFO',
            'debug_output': None,
            'debugpy_enable': False,
            'debugpy_wait': False,
            'debugpy_host': '0.0.0.0',
            'debugpy_port': 5678,
            'profiles_dir': '/tmp/profiles',
        }
        
        # Load from YAML if specified
        if config_path:
            self._load_from_yaml(config_path)
        else:
            # Try default locations
            default_paths = [
                '.debug.yaml',
                '.debug.yml',
                '.devcontainer/.debug.yaml',
                '.devcontainer/.debug.yml',
            ]
            
            for path in default_paths:
                if Path(path).exists():
                    self._load_from_yaml(path)
                    break
        
        # Override with environment variables
        self._load_from_env()
    
    def _load_from_yaml(self, config_path: str) -> None:
        """Load configuration from YAML file.
        
        Args:
            config_path: Path to YAML configuration file
        """
        try:
            with open(config_path, 'r') as f:
                yaml_config = yaml.safe_load(f)
                
            if yaml_config and isinstance(yaml_config, dict):
                if 'debug' in yaml_config:
                    # Use debug section if available
                    yaml_config = yaml_config['debug']
                    
                # Update configuration
                self._config.update(yaml_config)
        except Exception as e:
            print(f"Warning: Could not load debug config from {config_path}: {e}")
    
    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        # Debug mode
        if 'DEBUG_MODE' in os.environ:
            self._config['debug_mode'] = self._parse_bool(os.environ['DEBUG_MODE'])
        
        # Profile mode
        if 'DEBUG_PROFILE' in os.environ:
            self._config['profile_mode'] = os.environ['DEBUG_PROFILE']
        
        # Debug level
        if 'DEBUG_LEVEL' in os.environ:
            self._config['debug_level'] = os.environ['DEBUG_LEVEL']
        
        # Debug output
        if 'DEBUG_OUTPUT' in os.environ:
            self._config['debug_output'] = os.environ['DEBUG_OUTPUT']
        
        # Debugpy settings
        if 'DEBUGPY_ENABLE' in os.environ:
            self._config['debugpy_enable'] = self._parse_bool(os.environ['DEBUGPY_ENABLE'])
        
        if 'DEBUGPY_WAIT' in os.environ:
            self._config['debugpy_wait'] = self._parse_bool(os.environ['DEBUGPY_WAIT'])
        
        if 'DEBUGPY_HOST' in os.environ:
            self._config['debugpy_host'] = os.environ['DEBUGPY_HOST']
        
        if 'DEBUGPY_PORT' in os.environ:
            self._config['debugpy_port'] = int(os.environ['DEBUGPY_PORT'])
        
        # Profiles directory
        if 'PROFILES_DIR' in os.environ:
            self._config['profiles_dir'] = os.environ['PROFILES_DIR']
    
    def _parse_bool(self, value: str) -> bool:
        """Parse a string as a boolean value.
        
        Args:
            value: String value to parse
            
        Returns:
            bool: Parsed boolean value
        """
        if value.lower() in ('true', '1', 'yes', 'y', 'on'):
            return True
        return False
    
    def __getattr__(self, name: str) -> Any:
        """Get a configuration value by attribute name.
        
        Args:
            name: Configuration name
            
        Returns:
            Configuration value
            
        Raises:
            AttributeError: If configuration doesn't exist
        """
        if name in self._config:
            return self._config[name]
        raise AttributeError(f"No debug configuration named '{name}'")