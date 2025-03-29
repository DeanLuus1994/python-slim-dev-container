"""Profiling strategy implementations."""

import os
import sys
import time
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable

class Profiler(ABC):
    """Base profiler abstract class.
    
    Defines the interface for all profiling strategies.
    """
    
    def __init__(self):
        """Initialize the profiler."""
        self.output_path = None
        self.start_time = None
        self.is_running = False
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the profiler name."""
        pass
    
    @property
    @abstractmethod
    def file_extension(self) -> str:
        """Get the default file extension for output files."""
        pass
    
    @abstractmethod
    def start(self) -> None:
        """Start profiling."""
        self.start_time = time.time()
        self.is_running = True
    
    @abstractmethod
    def stop(self) -> None:
        """Stop profiling."""
        self.is_running = False
    
    def __enter__(self):
        """Support for context manager usage."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support for context manager usage."""
        self.stop()


class NullProfiler(Profiler):
    """Null profiler that does nothing.
    
    Useful as a no-op option when profiling is disabled.
    """
    
    @property
    def name(self) -> str:
        return "null"
    
    @property
    def file_extension(self) -> str:
        return "txt"
    
    def start(self) -> None:
        """Start the null profiler (does nothing)."""
        super().start()
    
    def stop(self) -> None:
        """Stop the null profiler (does nothing)."""
        super().stop()


class TimeProfiler(Profiler):
    """Time-based profiler using pyinstrument.
    
    Provides detailed timing analysis of function calls.
    """
    
    def __init__(self):
        """Initialize the time profiler."""
        super().__init__()
        self.profiler = None
    
    @property
    def name(self) -> str:
        return "time"
    
    @property
    def file_extension(self) -> str:
        return "html"
    
    def start(self) -> None:
        """Start time profiling."""
        try:
            from pyinstrument import Profiler
            self.profiler = Profiler()
            self.profiler.start()
            super().start()
        except ImportError:
            print("Warning: pyinstrument not installed, time profiling disabled")
    
    def stop(self) -> None:
        """Stop time profiling and save results."""
        if not self.is_running or not self.profiler:
            return
            
        self.profiler.stop()
        
        if self.output_path:
            # Create directory if it doesn't exist
            Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Save HTML report
            with open(self.output_path, 'w') as f:
                f.write(self.profiler.output_html())
        else:
            # Print to console
            print(self.profiler.output_text(unicode=True, color=True))
        
        super().stop()


class MemoryProfiler(Profiler):
    """Memory profiling using memory_profiler.
    
    Tracks memory usage over time.
    """
    
    def __init__(self):
        """Initialize the memory profiler."""
        super().__init__()
        self.process = None
    
    @property
    def name(self) -> str:
        return "memory"
    
    @property
    def file_extension(self) -> str:
        return "dat"
    
    def start(self) -> None:
        """Start memory profiling."""
        # Get the main script being executed
        main_script = sys.argv[0]
        
        # Determine the output path
        output_path = self.output_path or f"/tmp/profiles/memory_{int(time.time())}.dat"
        
        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Start mprof as a separate process
        cmd = [
            sys.executable, "-m", "memory_profiler", 
            "--multiprocess", 
            "-o", output_path, 
            main_script
        ] + sys.argv[1:]
        
        try:
            self.process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            super().start()
        except Exception as e:
            print(f"Warning: Could not start memory profiler: {e}")
    
    def stop(self) -> None:
        """Stop memory profiling."""
        if not self.is_running or not self.process:
            return
            
        try:
            self.process.terminate()
            self.process.wait(timeout=5)
            
            # If process didn't terminate, force kill
            if self.process.poll() is None:
                self.process.kill()
                
            print(f"Memory profile saved to: {self.output_path}")
        except Exception as e:
            print(f"Warning: Error stopping memory profiler: {e}")
        
        super().stop()


class CPUProfiler(Profiler):
    """CPU profiling using py-spy.
    
    Creates a visual CPU flame graph.
    """
    
    def __init__(self):
        """Initialize the CPU profiler."""
        super().__init__()
        self.process = None
    
    @property
    def name(self) -> str:
        return "cpu"
    
    @property
    def file_extension(self) -> str:
        return "svg"
    
    def start(self) -> None:
        """Start CPU profiling."""
        # Determine the output path
        output_path = self.output_path or f"/tmp/profiles/cpu_{int(time.time())}.svg"
        
        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Start py-spy as a separate process
        cmd = [
            "py-spy", "record",
            "--output", output_path,
            "--format", "flamegraph",
            "--rate", "100",
            "--nonblocking",
            "--pid", str(os.getpid())
        ]
        
        try:
            self.process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            self.output_path = output_path
            super().start()
        except Exception as e:
            print(f"Warning: Could not start CPU profiler: {e}")
    
    def stop(self) -> None:
        """Stop CPU profiling."""
        if not self.is_running or not self.process:
            return
            
        try:
            self.process.terminate()
            self.process.wait(timeout=5)
            
            # If process didn't terminate, force kill
            if self.process.poll() is None:
                self.process.kill()
                
            print(f"CPU profile saved to: {self.output_path}")
        except Exception as e:
            print(f"Warning: Error stopping CPU profiler: {e}")
        
        super().stop()


class ScaleneProfiler(Profiler):
    """Scalene profiler for CPU, memory, and GPU profiling.
    
    Provides comprehensive profiling information.
    """
    
    def __init__(self):
        """Initialize the Scalene profiler."""
        super().__init__()
        self.process = None
    
    @property
    def name(self) -> str:
        return "scalene"
    
    @property
    def file_extension(self) -> str:
        return "html"
    
    def start(self) -> None:
        """Start Scalene profiling."""
        # Get the main script being executed
        main_script = sys.argv[0]
        
        # Determine the output path
        output_path = self.output_path or f"/tmp/profiles/scalene_{int(time.time())}.html"
        
        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Start scalene as a separate process
        cmd = [
            sys.executable, "-m", "scalene",
            "--outfile", output_path,
            "--html",
            "--cpu",
            "--memory",
            main_script
        ] + sys.argv[1:]
        
        try:
            self.process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            self.output_path = output_path
            super().start()
        except Exception as e:
            print(f"Warning: Could not start Scalene profiler: {e}")
    
    def stop(self) -> None:
        """Stop Scalene profiling."""
        if not self.is_running or not self.process:
            return
            
        try:
            self.process.terminate()
            self.process.wait(timeout=5)
            
            # If process didn't terminate, force kill
            if self.process.poll() is None:
                self.process.kill()
                
            print(f"Scalene profile saved to: {self.output_path}")
        except Exception as e:
            print(f"Warning: Error stopping Scalene profiler: {e}")
        
        super().stop()