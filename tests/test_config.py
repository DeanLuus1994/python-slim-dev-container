"""Tests for the configuration module."""

import tempfile
from pathlib import Path
import pytest

from slimdev.config import Config


def test_config_loading():
    """Test loading configuration from pyproject.toml."""
    config = Config()
    
    # Test accessor methods
    assert isinstance(config["python_version"], str)
    assert config.get("postgres_user") == "postgres"
    assert config.get("nonexistent_key", "default") == "default"


def test_env_var_generation():
    """Test generation of environment variables."""
    config = Config()
    env_vars = config.get_env_vars()
    
    assert "PYTHON_VERSION" in env_vars
    assert "DEV_MODE" in env_vars
    # Boolean should be converted to lowercase string
    assert env_vars["DEV_MODE"] == "true"


def test_env_file_generation():
    """Test generating .env file."""
    config = Config()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        env_path = Path(temp_dir) / ".env"
        config.generate_env_file(env_path)
        
        # Check file exists
        assert env_path.exists()
        
        # Read and verify content
        content = env_path.read_text()
        assert "PYTHON_VERSION=" in content
        assert "POSTGRES_USER=postgres" in content