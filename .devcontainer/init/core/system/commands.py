"""Command execution utilities."""

import os
import subprocess
import threading
from typing import Optional, List, Dict
from ...log.logger import get_logger

logger = get_logger()
_cmd_cache_lock = threading.Lock()
_cmd_cache: Dict[str, bool] = {}

def has_command(cmd: str) -> bool:
    """Check if a command is available in the system PATH.
    
    Args:
        cmd: The command name to check
        
    Returns:
        True if the command exists and is executable, False otherwise
    """
    with _cmd_cache_lock:
        if cmd in _cmd_cache:
            return _cmd_cache[cmd]
        
        result = any(
            os.access(os.path.join(path, cmd), os.X_OK)
            for path in os.environ["PATH"].split(os.pathsep)
            if os.path.exists(os.path.join(path, cmd))
        )
        
        _cmd_cache[cmd] = result
        return result

def run_command(args: List[str], check: bool = True, 
                capture: bool = True) -> Optional[str]:
    """Run a system command and optionally capture its output.
    
    Args:
        args: List of command arguments
        check: Whether to raise an exception on command failure
        capture: Whether to capture and return command output
        
    Returns:
        Command output as string if capture=True, None otherwise
        
    Raises:
        subprocess.CalledProcessError: If check=True and the command fails
    """
    if not args:
        logger.error("Empty command provided")
        return None
        
    cmd_str = " ".join(args)
    try:
        if capture:
            result = subprocess.run(
                args, check=check, stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, text=True
            )
            return result.stdout.strip()
        else:
            subprocess.run(args, check=check)
            return None
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {cmd_str}")
        logger.error(f"Error: {e.stderr.strip() if e.stderr else str(e)}")
        if check:
            raise
        return None
    except Exception as e:
        logger.error(f"Error executing {cmd_str}: {str(e)}")
        if check:
            raise
        return None