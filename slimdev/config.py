"""
Configuration management for slimdev.

Provides a central configuration interface that extracts settings from pyproject.toml.
"""

import sys
import tomli
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Configuration manager for the slim development container."""

    def __init__(self, toml_path: Optional[Path] = None) -> None:
        """
        Initialize the configuration.

        Args:
            toml_path: Path to pyproject.toml. If None, will search in parent directories.
        """
        if toml_path is None:
            toml_path = self._find_pyproject()
        
        self.toml_path = toml_path
        self._config = self._load_config()
    
    def _find_pyproject(self) -> Path:
        """Find pyproject.toml by looking in parent directories."""
        current_dir = Path.cwd()
        
        while current_dir != current_dir.parent:
            pyproject = current_dir / "pyproject.toml"
            if pyproject.exists():
                return pyproject
            current_dir = current_dir.parent
        
        raise FileNotFoundError(
            "Could not find pyproject.toml in any parent directory. "
            "Please ensure you're running this from within a Python project."
        )
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from pyproject.toml."""
        try:
            with open(self.toml_path, "rb") as f:
                pyproject = tomli.load(f)
        except Exception as e:
            raise ValueError(f"Failed to parse pyproject.toml: {str(e)}")
        
        # Get the slimdev config section
        config = pyproject.get("tool", {}).get("slimdev", {})
        
        if not config:
            raise ValueError(
                "Missing [tool.slimdev] section in pyproject.toml. "
                "Please ensure your configuration is correctly set up."
            )
        
        return config
    
    def get_env_vars(self) -> Dict[str, str]:
        """
        Get configuration as environment variables.
        
        Returns:
            Dict mapping environment variable names to values.
        """
        result = {}
        
        for key, value in self._config.items():
            env_key = key.upper()
            
            # Convert booleans to lowercase strings
            if isinstance(value, bool):
                value = str(value).lower()
            else:
                value = str(value)
            
            result[env_key] = value
        
        return result
    
    def generate_env_file(self, path: Path) -> None:
        """
        Generate .env file at the specified path.
        
        Args:
            path: Path where the .env file will be written.
        """
        env_vars = self.get_env_vars()
        
        try:
            with open(path, "w") as f:
                f.write("# Generated from pyproject.toml - DO NOT EDIT\n")
                for key, value in env_vars.items():
                    f.write(f"{key}={value}\n")
            print(f"Environment file generated at: {path}")
        except Exception as e:
            raise IOError(f"Failed to write environment file to {path}: {str(e)}")
    
    def __getitem__(self, key: str) -> Any:
        """Access config values using dictionary syntax."""
        return self._config[key]
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get config value with optional default.
        
        Args:
            key: The configuration key to retrieve
            default: Value to return if key is not found
            
        Returns:
            The configuration value or default
        """
        return self._config.get(key, default)


def generate_env() -> None:
    """
    Generate .env file in the .devcontainer directory.
    
    This function finds the appropriate .devcontainer directory and
    creates an .env file with variables from pyproject.toml.
    """
    config = Config()
    
    # Ensure .devcontainer directory exists
    devcontainer_dir = Path.cwd().parent / ".devcontainer"
    if not devcontainer_dir.exists():
        devcontainer_dir = Path.cwd() / ".devcontainer"
    
    if not devcontainer_dir.exists():
        devcontainer_dir.mkdir(parents=True)
        print(f"Created .devcontainer directory at: {devcontainer_dir}")
    
    env_file = devcontainer_dir / ".env"
    config.generate_env_file(env_file)


if __name__ == "__main__":
    """When executed directly, generate .env file and print variables."""
    try:
        config = Config()
        
        for key, value in config.get_env_vars().items():
            print(f"{key}={value}")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)