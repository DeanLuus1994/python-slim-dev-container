"""Constants used throughout the functions module."""

# Resource detection constants
DEFAULT_GPU_MEMORY_MB = 0
MEMORY_RESERVATION_PERCENT = 5  # Reserve 5% of RAM for system

# Optimization constants
DEFAULT_CCACHE_SIZE = "5G"
DEFAULT_STRIP_FLAG = "-s"
COMPILER_FLAGS = {
    "x86_64": ["-march=native", "-mtune=native"],
    "amd64": ["-march=native", "-mtune=native"],
    "arm64": ["-march=native"],
    "aarch64": ["-march=native"]
}
CPU_FEATURE_FLAGS = {
    "avx": "-mavx",
    "avx2": "-mavx2",
    "fma": "-mfma",
    "sse4_1": "-msse4.1",
    "sse4_2": "-msse4.2"
}

# Repository constants
DEFAULT_BRANCH = "main"
DEFAULT_GIT_JOBS = 4
DEFAULT_REMOTE = "origin"
GIT_CONFIG = {
    "credential.helper": "store",
    "core.autocrlf": "input",
    "init.defaultBranch": "main",
    "pull.rebase": "false",
    "fetch.parallel": "0"
}

# Parallelism constants
DEFAULT_PROCESS_MULTIPLIER = 1
DEFAULT_THREAD_MULTIPLIER = 2
DEFAULT_TIMEOUT = 120  # seconds

# UI constants
COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[36m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m"
}

# File patterns
BINARY_EXTENSIONS = [".so", ".dll", ".dylib", ".pyd"]
PYTHON_EXTENSIONS = [".py", ".pyi", ".pyx", ".pyd"]

# Environment variables
ENV_VARS = {
    "PYTHON_EXEC": "sys.executable",
    "PROJECT_ROOT": "project_root",
    "GITHUB_PAT": "",
    "GITHUB_USERNAME": "",
    "GITHUB_EMAIL": "",
    "PYTHONHASHSEED": "1",
    "PYTHONDONTWRITEBYTECODE": "1",
    "PYTHONUNBUFFERED": "1"
}