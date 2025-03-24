"""Binary optimization utilities."""

import os
import platform
import subprocess
from pathlib import Path
from typing import Set, List, Optional
from ...log.logger import get_logger
from ...core.system.commands import has_command, run_command
from ..exceptions import OptimizationError

logger = get_logger()

def compile_python_bytecode(python_exec: str) -> bool:
    """Compile Python modules to bytecode for faster startup.
    
    Args:
        python_exec: Path to Python executable
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if not os.path.isfile(python_exec):
            logger.error(f"Python executable not found at {python_exec}")
            return False
            
        python_lib = os.path.dirname(os.__file__)
        logger.info(f"Compiling Python bytecode in {python_lib}")
        
        # First, compile with optimization level 1 (for __pycache__/*.opt-1.pyc)
        result1 = run_command(
            [python_exec, "-O", "-m", "compileall", "-f", "-q", python_lib],
            check=False
        )
        
        # Then compile with optimization level 2 (for __pycache__/*.opt-2.pyc)
        result2 = run_command(
            [python_exec, "-OO", "-m", "compileall", "-f", "-q", python_lib],
            check=False
        )
        
        success = result1 is not None or result2 is not None
        logger.info(f"Python bytecode compilation {'succeeded' if success else 'failed'}")
        return success
    except Exception as e:
        logger.error(f"Error compiling Python bytecode: {e}")
        return False

def strip_binaries(python_lib: Optional[str] = None) -> bool:
    """Strip debug symbols from libraries to reduce size.
    
    Args:
        python_lib: Path to Python lib directory, defaults to os.__file__ directory
        
    Returns:
        True if successful, False otherwise
    """
    if not has_command("strip"):
        logger.warning("strip command not found, skipping binary optimization")
        return False
        
    try:
        if python_lib is None:
            python_lib = os.path.dirname(os.__file__)
            
        if not os.path.isdir(python_lib):
            logger.error(f"Python library directory not found at {python_lib}")
            return False
            
        logger.info(f"Stripping binaries in {python_lib}")
        
        # Determine file extensions based on platform
        shared_exts = {".so"}
        if platform.system().lower() == "darwin":
            shared_exts.add(".dylib")
        elif platform.system().lower() == "windows":
            shared_exts.add(".dll")
            shared_exts.add(".pyd")
            
        stripped_files = 0
        for root, _, files in os.walk(python_lib):
            for file in files:
                file_path = os.path.join(root, file)
                if any(file.endswith(ext) for ext in shared_exts):
                    try:
                        run_command(["strip", "-s", file_path], check=False)
                        stripped_files += 1
                    except Exception as e:
                        logger.debug(f"Failed to strip {file_path}: {e}")
                        
        logger.info(f"Stripped {stripped_files} binaries in {python_lib}")
        return True
    except Exception as e:
        logger.error(f"Error stripping binaries: {e}")
        return False