"""
Centralized debugging and profiling framework for Python-Slim.

This module provides a comprehensive debugging system that can be
easily injected into any component of the application with minimal
code changes.

Usage:
    # Simple activation
    from .devcontainer.init.debug import debugger
    debugger.setup_if_enabled()

    # With specific profiling
    from .devcontainer.init.debug import debugger
    debugger.setup(profile_mode='memory')

    # As a context manager for specific blocks
    from .devcontainer.init.debug import profile
    with profile('time'):
        expensive_operation()

Environment Variables:
    DEBUG_MODE=1                # Enable debugging
    DEBUG_PROFILE=time|memory|cpu|scalene  # Set profiling mode
    DEBUG_LEVEL=DEBUG|INFO|WARNING|ERROR   # Set log level
    DEBUG_OUTPUT=/path/to/file.log         # Redirect debug output
    DEBUGPY_ENABLE=1            # Enable debugpy server
    DEBUGPY_WAIT=1              # Wait for debugger to attach
"""

import os
import sys
import logging
from typing import Optional, Dict, Any, Callable, Union, Type, List
from pathlib import Path

from .core import DebugCore
from .profilers import (
    TimeProfiler, MemoryProfiler, CPUProfiler, ScaleneProfiler, 
    NullProfiler, Profiler
)
from .log import setup_debug_logger, get_debug_logger

__version__ = "1.0.0"
__all__ = ['debugger', 'profile', 'debug_log', 'enable_debug_server', 'configure']

# Singleton debugger instance
debugger = DebugCore()

# Global logger
debug_log = get_debug_logger()

# Convenience function for profiling context
def profile(mode: str = 'time', output_path: Optional[str] = None):
    """Context manager for profiling specific code blocks.
    
    Args:
        mode: Profiling mode ('time', 'memory', 'cpu', 'scalene')
        output_path: Where to save profiling results (default: auto-generated)
    
    Example:
        with profile('memory'):
            expensive_operation()
    """
    return debugger.profile_context(mode, output_path)

# Convenience function for enabling debug server
def enable_debug_server(host: str = '0.0.0.0', port: int = 5678, 
                       wait_for_client: bool = False):
    """Enable the debug server for IDE integration.
    
    Args:
        host: Interface to listen on (default: all interfaces)
        port: Port to listen on (default: 5678)
        wait_for_client: Whether to pause execution until a client connects
    """
    return debugger.enable_debug_server(host, port, wait_for_client)

def configure(config_path: Optional[str] = None, 
             debug_mode: Optional[bool] = None,
             profile_mode: Optional[str] = None,
             debug_level: Optional[str] = None,
             debug_output: Optional[str] = None):
    """Configure debugging with specific settings.
    
    Args:
        config_path: Path to custom debug YAML config
        debug_mode: Enable or disable debugging
        profile_mode: Set profiling mode
        debug_level: Set log level
        debug_output: Redirect debug output
        
    Returns:
        bool: True if configuration succeeded
    """
    # Override configuration from environment
    if debug_mode is not None:
        os.environ['DEBUG_MODE'] = '1' if debug_mode else '0'
    
    if profile_mode is not None:
        os.environ['DEBUG_PROFILE'] = profile_mode
    
    if debug_level is not None:
        os.environ['DEBUG_LEVEL'] = debug_level
    
    if debug_output is not None:
        os.environ['DEBUG_OUTPUT'] = debug_output
    
    # Reload configuration
    from .config import DebugConfig
    debugger.config = DebugConfig(config_path)
    
    return True