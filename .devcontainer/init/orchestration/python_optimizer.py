"""Python interpreter optimization functionality."""

import os
import sys
import atexit
from typing import Dict, Any, Set, Optional
from ..log.logger import get_logger
from ..core.config.loader import load_config
from ..core.system.memory import get_memory_info
from ..core.system.cpu import detect_cpu_features
from ..core.utils.validation import validate_dict_key
from ..functions.resource.detection import detect_resources
from ..functions.optimization.compiler import setup_ccache, apply_compiler_flags
from ..functions.optimization.binary import compile_python_bytecode, strip_binaries
from ..functions.concurrency.executor import shutdown_executors

logger = get_logger()
atexit.register(shutdown_executors)

class PythonOptimizer:
    """Optimizes Python interpreter based on system capabilities."""
    
    def __init__(self):
        self.build_config = load_config("build") or {}
        self.python_config = load_config("python") or {}
        self.resources = detect_resources(self.build_config)
        self.cpu_features = detect_cpu_features()
    
    def validate_configs(self) -> bool:
        """Validate that necessary configuration is available.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        if not self.build_config:
            logger.warning("Build configuration is empty")
        if not self.python_config:
            logger.warning("Python configuration is empty")
        return bool(self.build_config and self.python_config)
    
    def optimize_python(self) -> bool:
        """Perform Python optimization actions.
        
        Returns:
            True if optimization was successful, False otherwise
        """
        python_exec = os.environ.get("PYTHON_EXEC", sys.executable)
        if not os.path.isfile(python_exec) or not os.access(python_exec, os.X_OK):
            logger.error(f"Python executable not valid at {python_exec}. Falling back to sys.executable.")
            python_exec = sys.executable  # fallback to current interpreter
        try:
            logger.info(f"Optimizing Python at {python_exec}")
            apply_compiler_flags(self.build_config, self.cpu_features)
            compile_python_bytecode(python_exec)
            strip_binaries(python_exec)
            py_env = validate_dict_key(self.python_config, "environment", {})
            os.environ["PYTHONHASHSEED"] = str(validate_dict_key(py_env, "hashseed", "1"))
            os.environ["PYTHONDONTWRITEBYTECODE"] = str(
                validate_dict_key(py_env, "dont_write_bytecode", "1")
            )
            os.environ["PYTHONUNBUFFERED"] = str(
                validate_dict_key(py_env, "unbuffered", "1")
            )
            logger.info("Python optimization completed")
            return True
        except Exception as e:
            logger.error(f"Error during Python optimization: {e}")
            return False
    
    def run(self) -> int:
        """Run the optimization process.
        
        Returns:
            Exit code (0 for success, non-zero for errors)
        """
        try:
            logger.info("Starting Python optimization")
            if not self.validate_configs():
                logger.warning("Using default configurations")
            setup_ccache(self.build_config, self.python_config)
            success = self.optimize_python()
            return 0 if success else 1
        except Exception as e:
            logger.error(f"Optimization failed: {e}")
            return 1

def main() -> int:
    """Main entry point for Python optimization.
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    optimizer = PythonOptimizer()
    return optimizer.run()

if __name__ == "__main__":
    sys.exit(main())