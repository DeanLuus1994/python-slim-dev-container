"""
DevContainer initialization package with modular architecture.

This package provides a comprehensive initialization system for Python
development containers, with features for resource detection, optimization,
and repository management.

Usage: python -m .devcontainer.init [command]

Commands:
  python-optimize   - Optimize Python interpreter
  github-provision  - Clone or update GitHub repositories
  all               - Run all initialization tasks (default)
"""
import os
import sys
import atexit
import platform
import importlib
import compileall
from pathlib import Path
from typing import Dict, Any, Optional

# Import from log module
from .log.logger import get_logger
from .log.formatter import ColorFormatter

# Import from core module
from .core.config.env import setup_env_file, load_env_file, update_env_initialized_flag
from .core.system.paths import get_project_root
from .core.utils.validation import validate_path
from .core.__about__ import __version__ as core_version

# Import from functions module with updated paths
from .functions.concurrency.executor import shutdown_executors
from .functions.ui.prompt import display_env_prompt, green, yellow, blue
from .functions.__about__ import __version__ as functions_version

# Import from orchestration modules
from .orchestration.python_optimizer import PythonOptimizer
from .orchestration.github_provisioner import main as github_provision

logger = get_logger()

# Register shutdown hook to ensure resources are cleaned up
atexit.register(shutdown_executors)

# Compile package to bytecode at import time for better performance
_package_dir = Path(__file__).parent
compileall.compile_dir(
    str(_package_dir),
    force=True,
    quiet=1,
    optimize=2
)

__version__ = '1.0.0'
__author__ = 'DeanLuus1994'
__all__ = [
    'init_environment',
    'main',
    '__version__',
    '__author__'
]

def show_help() -> None:
    """Display the help information for the initialization package."""
    print(__doc__)
    print("\nEnvironment Variables:")
    print("  PYTHON_SLIM_NOPROMPT=1  - Skip interactive prompts")
    print("  PROJECT_ROOT=/path      - Override project root path")
    print("  PYTHON_EXEC=/path       - Override Python executable path")
    print("  GITHUB_PAT=token        - Set GitHub Personal Access Token")
    print("  GITHUB_USERNAME=user    - Set GitHub username")
    print("  GITHUB_LOCAL_REPOS=a,b  - Comma-separated repos to clone")
    
def init_environment() -> int:
    """Initialize the environment by loading configuration from .env file.
    
    Returns:
        Number of environment variables loaded
    """
    try:
        project_root = get_project_root()
        env_path = setup_env_file(project_root)
        if not env_path:
            logger.warning("No .env file found or created")
            return 0
            
        # Display prompt for user to review/edit .env file
        # Skip if running in non-interactive mode or with PYTHON_SLIM_NOPROMPT=1
        if (sys.stdin.isatty() and sys.stdout.isatty() and 
            os.environ.get("PYTHON_SLIM_NOPROMPT") != "1"):
            display_env_prompt(env_path)
            
        # Reload env file in case it was modified
        env_vars = load_env_file(env_path)
        for key, value in env_vars.items():
            os.environ[key] = value
            
        if "PROJECT_ROOT" not in os.environ:
            os.environ["PROJECT_ROOT"] = str(project_root)
            
        logger.info(f"Environment initialized with {len(env_vars)} variables")
        update_env_initialized_flag(env_path, True)
        return len(env_vars)
    except Exception as e:
        logger.error(f"Error initializing environment: {e}")
        return 0

def main() -> int:
    """Main entry point for the initialization package.
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    try:
        # Print basic system info
        logger.info(f"Python {platform.python_version()} on {platform.system()}")
        logger.info(f"Core v{core_version}, Functions v{functions_version}")
        
        # Initialize environment
        vars_loaded = init_environment()
        if vars_loaded == 0:
            logger.warning("No environment variables loaded, using defaults")
            
        command = sys.argv[1] if len(sys.argv) > 1 else 'all'
        
        if command == 'python-optimize':
            optimizer = PythonOptimizer()
            return optimizer.run()
        elif command == 'github-provision':
            return github_provision()
        elif command == 'all':
            logger.info("Running all initialization tasks")
            optimizer = PythonOptimizer()
            python_result = optimizer.run()
            if python_result != 0:
                return python_result
            return github_provision()
        elif command in ['-h', '--help', 'help']:
            show_help()
            return 0
        else:
            logger.error(f"Unknown command: {command}")
            show_help()
            return 1
    except KeyboardInterrupt:
        print("\nOperation aborted by user")
        return 130
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        logger.debug(f"Error details: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())