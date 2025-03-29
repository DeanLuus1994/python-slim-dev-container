"""Core debugging functionality."""

import os
import sys
import time
import inspect
import signal
import atexit
import threading
import traceback
from pathlib import Path
from typing import Dict, Any, Optional, Union, Type, List, Callable, ContextManager
from contextlib import contextmanager

from .config import DebugConfig
from .profilers import (
    TimeProfiler, MemoryProfiler, CPUProfiler, ScaleneProfiler, 
    NullProfiler, Profiler
)
from .log import setup_debug_logger, get_debug_logger

# Configure logging
logger = get_debug_logger()

class DebugCore:
    """Central debugging coordination class.
    
    This class manages debugging functionality across the application,
    including profiling, logging, and debug server configuration.
    """
    
    def __init__(self):
        """Initialize the debug core."""
        self.config = DebugConfig()
        self.active_profiler = None
        self.debug_server_running = False
        self.initialized = False
        self._profiler_registry = {
            'time': TimeProfiler,
            'memory': MemoryProfiler,
            'cpu': CPUProfiler,
            'scalene': ScaleneProfiler,
            'none': NullProfiler
        }
        
        # Register shutdown handler
        atexit.register(self.shutdown)
    
    def setup_if_enabled(self) -> bool:
        """Setup debugging if enabled in environment or configuration.
        
        Returns:
            bool: True if debugging was set up, False otherwise
        """
        if self.config.debug_mode:
            return self.setup()
        return False
    
    def setup(self, profile_mode: Optional[str] = None, 
             debug_level: Optional[str] = None,
             debug_output: Optional[str] = None,
             enable_debugpy: Optional[bool] = None,
             wait_for_client: Optional[bool] = None) -> bool:
        """Setup debugging with specific configuration.
        
        Args:
            profile_mode: Profiling mode to use (overrides config)
            debug_level: Debug log level (overrides config)
            debug_output: Debug output file (overrides config)
            enable_debugpy: Whether to enable debugpy (overrides config)
            wait_for_client: Wait for debugger to attach (overrides config)
            
        Returns:
            bool: True if setup succeeded, False otherwise
        """
        if self.initialized:
            logger.warning("Debug system already initialized")
            return True
            
        try:
            # Configure logging
            log_level = debug_level or self.config.debug_level
            log_output = debug_output or self.config.debug_output
            setup_debug_logger(log_level, log_output)
            
            # Activate profiler
            profile_mode = profile_mode or self.config.profile_mode
            if profile_mode and profile_mode != 'none':
                self.start_profiler(profile_mode)
            
            # Enable debug server if requested
            if enable_debugpy or (enable_debugpy is None and self.config.debugpy_enable):
                self.enable_debug_server(
                    wait_for_client=wait_for_client or self.config.debugpy_wait
                )
            
            # Set up exception hooks
            self._setup_exception_hooks()
            
            # Enable signal handlers for graceful debugging
            self._setup_signal_handlers()
            
            self.initialized = True
            logger.info(f"Debug system initialized with profile mode: {profile_mode}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize debug system: {e}")
            traceback.print_exc()
            return False
    
    def start_profiler(self, mode: str) -> bool:
        """Start a specific profiler.
        
        Args:
            mode: Profiler type ('time', 'memory', 'cpu', 'scalene')
            
        Returns:
            bool: True if profiler started successfully
        """
        if mode not in self._profiler_registry:
            logger.error(f"Unknown profiler mode: {mode}")
            return False
            
        # Stop any existing profiler
        if self.active_profiler:
            self.active_profiler.stop()
            
        # Create and start the new profiler
        profiler_class = self._profiler_registry[mode]
        self.active_profiler = profiler_class()
        
        try:
            self.active_profiler.start()
            logger.info(f"Started {mode} profiler")
            return True
        except Exception as e:
            logger.error(f"Failed to start {mode} profiler: {e}")
            self.active_profiler = None
            return False
    
    def stop_profiler(self) -> bool:
        """Stop the active profiler.
        
        Returns:
            bool: True if stopped successfully
        """
        if not self.active_profiler:
            return False
            
        try:
            self.active_profiler.stop()
            logger.info(f"Stopped {self.active_profiler.name} profiler")
            self.active_profiler = None
            return True
        except Exception as e:
            logger.error(f"Error stopping profiler: {e}")
            return False
    
    @contextmanager
    def profile_context(self, mode: str = 'time', 
                       output_path: Optional[str] = None):
        """Context manager for profiling a specific block of code.
        
        Args:
            mode: Profiling mode ('time', 'memory', 'cpu', 'scalene')
            output_path: Where to save profiling results
            
        Yields:
            The active profiler
        """
        if mode not in self._profiler_registry:
            logger.error(f"Unknown profiler mode: {mode}")
            yield None
            return
            
        # Create a new profiler for this context
        profiler_class = self._profiler_registry[mode]
        profiler = profiler_class()
        
        # Get caller information for automatic output naming
        if not output_path:
            frame = inspect.currentframe().f_back
            module = inspect.getmodule(frame)
            module_name = module.__name__ if module else "unknown"
            lineno = frame.f_lineno
            timestamp = int(time.time())
            
            # Create profiles directory if it doesn't exist
            profiles_dir = Path('/tmp/profiles')
            profiles_dir.mkdir(exist_ok=True)
            
            output_path = f"/tmp/profiles/{module_name}_{lineno}_{timestamp}.{profiler.file_extension}"
        
        # Configure output path
        profiler.output_path = output_path
        
        try:
            # Start profiler and yield control
            profiler.start()
            logger.debug(f"Started {mode} profiler for context")
            yield profiler
        finally:
            # Always stop the profiler
            try:
                profiler.stop()
                logger.debug(f"Stopped {mode} profiler, output at: {output_path}")
            except Exception as e:
                logger.error(f"Error stopping context profiler: {e}")
    
    def enable_debug_server(self, host: str = '0.0.0.0', port: int = 5678,
                           wait_for_client: bool = False) -> bool:
        """Enable the debug server for IDE integration.
        
        Args:
            host: Interface to listen on
            port: Port to listen on
            wait_for_client: Whether to pause execution until a client connects
            
        Returns:
            bool: True if debug server started successfully
        """
        if self.debug_server_running:
            logger.warning("Debug server already running")
            return True
            
        try:
            import debugpy
            debugpy.listen((host, port))
            
            logger.info(f"Debug server listening on {host}:{port}")
            
            if wait_for_client:
                logger.info("Waiting for debugger to attach...")
                debugpy.wait_for_client()
                logger.info("Debugger attached!")
                
            self.debug_server_running = True
            return True
        except ImportError:
            logger.error("debugpy not installed, cannot start debug server")
            return False
        except Exception as e:
            logger.error(f"Failed to start debug server: {e}")
            return False
    
    def shutdown(self):
        """Clean up debugging resources."""
        if self.active_profiler:
            try:
                self.active_profiler.stop()
                logger.info(f"Stopped {self.active_profiler.name} profiler during shutdown")
            except Exception as e:
                logger.error(f"Error stopping profiler during shutdown: {e}")
                
        logger.info("Debug system shutdown")
    
    def _setup_exception_hooks(self):
        """Set up exception hooks for better debugging."""
        original_excepthook = sys.excepthook
        
        def debug_exception_hook(exc_type, exc_value, exc_traceback):
            """Enhanced exception hook for debugging."""
            # Log the exception
            logger.error(
                "Uncaught exception",
                exc_info=(exc_type, exc_value, exc_traceback)
            )
            
            # Generate detailed traceback with locals
            tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            logger.debug("".join(tb_lines))
            
            # Call the original exception handler
            original_excepthook(exc_type, exc_value, exc_traceback)
        
        # Set our custom exception hook
        sys.excepthook = debug_exception_hook
        
        # Also handle thread exceptions
        original_thread_excepthook = threading.excepthook
        
        def debug_thread_exception_hook(args):
            """Enhanced thread exception hook."""
            # Log the thread exception
            logger.error(
                f"Uncaught exception in thread: {args.thread.name}",
                exc_info=(args.exc_type, args.exc_value, args.exc_traceback)
            )
            
            # Call the original thread exception handler
            original_thread_excepthook(args)
        
        # Set our custom thread exception hook
        threading.excepthook = debug_thread_exception_hook
    
    def _setup_signal_handlers(self):
        """Set up signal handlers for graceful debugging."""
        # SIGINT handler (Ctrl+C)
        def sigint_handler(sig, frame):
            logger.info("Received SIGINT, starting clean shutdown...")
            self.shutdown()
            # Re-raise the signal to allow normal SIGINT behavior
            signal.default_int_handler(sig, frame)
        
        # SIGTERM handler (termination signal)
        def sigterm_handler(sig, frame):
            logger.info("Received SIGTERM, starting clean shutdown...")
            self.shutdown()
            # Exit cleanly
            sys.exit(0)
        
        # Register signal handlers
        signal.signal(signal.SIGINT, sigint_handler)
        signal.signal(signal.SIGTERM, sigterm_handler)