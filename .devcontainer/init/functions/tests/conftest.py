"""Pytest configuration and fixtures for functions module tests."""
import pytest
from pathlib import Path
from typing import Dict, Any

@pytest.fixture
def sample_build_config() -> Dict[str, Any]:
    """Return a sample build configuration for testing."""
    return {
        "resources": {
            "default_cores": 2,
            "default_threads": 4,
            "build_jobs": 2
        },
        "paths": {
            "build_cache": "/tmp/build_cache",
            "gpu_cache": "/tmp/gpu_cache"
        },
        "cuda": {
            "cache_maxsize": "1073741824"
        }
    }

@pytest.fixture
def sample_python_config() -> Dict[str, Any]:
    """Return a sample Python configuration for testing."""
    return {
        "version": "3.9",
        "compiler": {
            "cc": "ccache gcc",
            "cxx": "ccache g++",
            "makeflags": "-j4"
        },
        "environment": {
            "hashseed": "1",
            "dont_write_bytecode": "1"
        }
    }