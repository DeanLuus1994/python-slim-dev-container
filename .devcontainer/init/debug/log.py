"""Debug logging facilities."""

import os
import sys
import logging
import time
import threading
from pathlib import Path
from typing import Dict, Any, Optional, Union

# Colored formatter class - similar to the one in your codebase
class ColoredFormatter(logging.Formatter):
    """Logging formatter that adds colors to log levels."""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m',     # Reset
    }
    
    def format(self, record):
        """Format the log record with colors."""
        log_message = super().format(record)
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        return f"{color}{log_message}{self.COLORS['RESET']}"


# Global debug logger instance
_debug_logger = None

def setup_debug_logger(level: str = 'INFO', 
                      output_path: Optional[str] = None) -> logging.Logger:
    """Set up the debug logger with the specified configuration.
    
    Args:
        level: Log level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        output_path: Path to log file (None for console only)
        
    Returns:
        logging.Logger: Configured logger
    """
    global _debug_logger
    
    # Create logger if it doesn't exist
    if _debug_logger is None:
        _debug_logger = logging.getLogger('python_slim_debug')
    
    # Clear any existing handlers
    for handler in _debug_logger.handlers[:]:
        _debug_logger.removeHandler(handler)
    
    # Set log level
    log_level = getattr(logging, level.upper(), logging.INFO)
    _debug_logger.setLevel(log_level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Create colored formatter
    formatter = ColoredFormatter(
        fmt='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    _debug_logger.addHandler(console_handler)
    
    # Create file handler if output path is specified
    if output_path:
        try:
            # Create directory if it doesn't exist
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Create file handler
            file_handler = logging.FileHandler(output_path)
            file_handler.setLevel(log_level)
            
            # Use a more detailed formatter for file logs
            file_formatter = logging.Formatter(
                fmt='%(asctime)s [%(levelname)s] [%(name)s:%(lineno)d] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            _debug_logger.addHandler(file_handler)
            
            _debug_logger.info(f"Debug logs will be saved to: {output_path}")
        except Exception as e:
            _debug_logger.error(f"Could not set up log file at {output_path}: {e}")
    
    return _debug_logger

def get_debug_logger() -> logging.Logger:
    """Get the debug logger, creating it if necessary.
    
    Returns:
        logging.Logger: Debug logger
    """
    global _debug_logger
    
    if _debug_logger is None:
        return setup_debug_logger()
    
    return _debug_logger