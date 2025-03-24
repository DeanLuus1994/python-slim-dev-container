"""Pytest configuration and fixtures for core module tests."""
import os
import pytest
from pathlib import Path
from typing import Dict, Any, Generator

@pytest.fixture
def sample_env_content() -> str:
    """Return sample environment file content for testing."""
    return """
# Sample environment file
TEST_VAR1=value1
TEST_VAR2=value2
# Comment line
TEST_EMPTY=
    """

@pytest.fixture
def temp_env_file(tmp_path: Path, sample_env_content: str) -> Path:
    """Create a temporary .env file with sample content."""
    env_file = tmp_path / ".env"
    env_file.write_text(sample_env_content)
    return env_file

@pytest.fixture
def sample_config() -> Dict[str, Any]:
    """Return a sample configuration dictionary for testing."""
    return {
        "build": {
            "resources": {
                "default_cores": 2,
                "default_threads": 4
            },
            "paths": {
                "build_cache": "/tmp/cache"
            }
        },
        "python": {
            "version": "3.9",
            "environment": {
                "hashseed": "1",
                "dont_write_bytecode": "1"
            }
        }
    }