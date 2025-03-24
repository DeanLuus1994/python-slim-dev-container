"""Tests for the env.py module."""
import os
import pytest
from pathlib import Path
from ..config.env import load_env_file, update_env_initialized_flag

def test_load_env_file(temp_env_file: Path) -> None:
    """Test loading environment variables from a file."""
    env_vars = load_env_file(temp_env_file)
    assert "TEST_VAR1" in env_vars
    assert env_vars["TEST_VAR1"] == "value1"
    assert "TEST_VAR2" in env_vars
    assert env_vars["TEST_VAR2"] == "value2"
    assert "TEST_EMPTY" in env_vars
    assert env_vars["TEST_EMPTY"] == ""

def test_update_env_initialized_flag(temp_env_file: Path) -> None:
    """Test updating the INITIALIZED flag in env file."""
    # Add INITIALIZED flag to temp file
    with open(temp_env_file, 'a') as f:
        f.write("INITIALIZED=false\n")
    
    # Update the flag
    success = update_env_initialized_flag(temp_env_file, True)
    assert success is True
    
    # Check if the flag was updated
    content = temp_env_file.read_text()
    assert "INITIALIZED=true" in content
    assert "INITIALIZED=false" not in content