"""Constants used throughout the core module."""

import os
from typing import Dict, Any, List

# Path constants
CONFIG_DIR = "config"
DEFAULT_ENV_FILE = ".env"
EXAMPLE_ENV_FILE = "example.env"

# System constants
DEFAULT_CPU_COUNT = 2
DEFAULT_MEMORY_MB = 4096
DEFAULT_TIMEOUT = 60  # Seconds
DEFAULT_ENCODING = "utf-8"

# Environment variable constants
ENV_PROJECT_ROOT = "PROJECT_ROOT"
ENV_PYTHON_EXEC = "PYTHON_EXEC"
ENV_INITIALIZED = "PYTHON_SLIM_INITIALIZED"
ENV_NOPROMPT = "PYTHON_SLIM_NOPROMPT"

# Git constants
GIT_DEFAULT_BRANCH = "main"
GIT_DEFAULT_REMOTE = "origin"

# Config keys
CONFIG_TYPES = ["build", "python", "github"]

# Result status
STATUS_SUCCESS = 0
STATUS_ERROR = 1
STATUS_WARNING = 2

# Default configuration values
DEFAULT_CONFIG: Dict[str, Any] = {
    "build": {
        "resources": {
            "default_cores": 0,  # 0 means auto-detect
            "default_threads": 0,
            "build_jobs": 0
        },
        "paths": {
            "build_cache": "/tmp/build_cache",
            "gpu_cache": "/tmp/gpu_cache"
        }
    },
    "python": {
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
}

# File extension mapping
FILE_EXTENSIONS: Dict[str, List[str]] = {
    "python": [".py", ".pyi", ".pyx", ".pyd"],
    "c": [".c", ".h"],
    "cpp": [".cpp", ".hpp", ".cc", ".cxx"],
    "text": [".txt", ".md", ".rst", ".ini", ".cfg"],
    "yaml": [".yml", ".yaml"],
    "json": [".json"],
    "binary": [".so", ".dll", ".dylib", ".pyc", ".pyo"]
}