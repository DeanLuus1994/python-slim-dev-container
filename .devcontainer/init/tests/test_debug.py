"""Unit tests for the debug module."""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path to import debug module
sys.path.insert(0, str(Path(__file__).parent.parent))

from debug.core import DebugCore
from debug.config import DebugConfig
from debug.profilers import (
    TimeProfiler, MemoryProfiler, CPUProfiler, ScaleneProfiler, NullProfiler
)

class TestDebugConfig(unittest.TestCase):
    """Test the debug configuration system."""
    
    def setUp(self):
        """Set up test environment."""
        # Save original environment variables
        self.original_env = {}
        for var in ["DEBUG_MODE", "DEBUG_PROFILE", "DEBUG_LEVEL", "DEBUG_OUTPUT",
                   "DEBUGPY_ENABLE", "DEBUGPY_WAIT", "DEBUGPY_HOST", "DEBUGPY_PORT",
                   "PROFILES_DIR"]:
            self.original_env[var] = os.environ.get(var)
            if var in os.environ:
                del os.environ[var]
    
    def tearDown(self):
        """Restore test environment."""
        # Restore original environment variables
        for var, value in self.original_env.items():
            if value is not None:
                os.environ[var] = value
            elif var in os.environ:
                del os.environ[var]
    
    def test_default_config(self):
        """Test default configuration values."""
        config = DebugConfig()
        
        self.assertFalse(config.debug_mode)
        self.assertEqual(config.profile_mode, "none")
        self.assertEqual(config.debug_level, "INFO")
        self.assertIsNone(config.debug_output)
        
        self.assertFalse(config.debugpy_enable)
        self.assertFalse(config.debugpy_wait)
        self.assertEqual(config.debugpy_host, "0.0.0.0")
        self.assertEqual(config.debugpy_port, 5678)
        
        self.assertEqual(config.profiles_dir, "/tmp/profiles")
    
    def test_env_override(self):
        """Test environment variable overrides."""
        # Set environment variables
        os.environ["DEBUG_MODE"] = "1"
        os.environ["DEBUG_PROFILE"] = "memory"
        os.environ["DEBUG_LEVEL"] = "DEBUG"
        os.environ["DEBUG_OUTPUT"] = "/tmp/test.log"
        os.environ["DEBUGPY_ENABLE"] = "1"
        os.environ["DEBUGPY_WAIT"] = "1"
        os.environ["DEBUGPY_PORT"] = "1234"
        os.environ["PROFILES_DIR"] = "/tmp/test_profiles"
        
        # Create config with environment variables
        config = DebugConfig()
        
        # Check if environment variables are applied
        self.assertTrue(config.debug_mode)
        self.assertEqual(config.profile_mode, "memory")
        self.assertEqual(config.debug_level, "DEBUG")
        self.assertEqual(config.debug_output, "/tmp/test.log")
        self.assertTrue(config.debugpy_enable)
        self.assertTrue(config.debugpy_wait)
        self.assertEqual(config.debugpy_port, 1234)
        self.assertEqual(config.profiles_dir, "/tmp/test_profiles")
    
    def test_yaml_config(self):
        """Test YAML configuration file loading."""
        # Create temporary YAML config file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("""
debug:
  debug_mode: true
  profile_mode: cpu
  debug_level: WARNING
  debug_output: /tmp/yaml_test.log
  debugpy_enable: true
  debugpy_port: 9876
  profiles_dir: /tmp/yaml_profiles
            """)
            config_path = f.name
        
        try:
            # Create config with YAML file
            config = DebugConfig(config_path)
            
            # Check if YAML settings are applied
            self.assertTrue(config.debug_mode)
            self.assertEqual(config.profile_mode, "cpu")
            self.assertEqual(config.debug_level, "WARNING")
            self.assertEqual(config.debug_output, "/tmp/yaml_test.log")
            self.assertTrue(config.debugpy_enable)
            self.assertEqual(config.debugpy_port, 9876)
            self.assertEqual(config.profiles_dir, "/tmp/yaml_profiles")
        finally:
            # Clean up
            Path(config_path).unlink()

class TestDebugCore(unittest.TestCase):
    """Test the debug core functionality."""
    
    @patch('debug.core.setup_debug_logger')
    def test_setup(self, mock_setup_logger):
        """Test debug setup."""
        debugger = DebugCore()
        
        # Mock the config
        debugger.config.debug_mode = True
        debugger.config.profile_mode = "none"
        debugger.config.debug_level = "INFO"
        debugger.config.debug_output = None
        
        # Call setup
        result = debugger.setup()
        
        # Verify setup
        self.assertTrue(result)
        self.assertTrue(debugger.initialized)
        mock_setup_logger.assert_called_once()
    
    @patch('debug.core.get_debug_logger')
    def test_start_profiler(self, mock_get_logger):
        """Test profiler activation."""
        # Mock logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        # Create debugger
        debugger = DebugCore()
        
        # Test starting each profiler type
        for profiler_type in ["time", "memory", "cpu", "scalene"]:
            with patch.object(debugger._profiler_registry[profiler_type], 'start') as mock_start:
                result = debugger.start_profiler(profiler_type)
                
                self.assertTrue(result)
                mock_start.assert_called_once()
                self.assertEqual(debugger.active_profiler.name, profiler_type)
    
    @patch('debug.core.get_debug_logger')
    def test_profile_context(self, mock_get_logger):
        """Test profile context manager."""
        # Mock logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        # Create debugger
        debugger = DebugCore()
        
        # Test time profiler context
        with patch.object(TimeProfiler, 'start') as mock_start:
            with patch.object(TimeProfiler, 'stop') as mock_stop:
                with debugger.profile_context('time') as profiler:
                    self.assertIsInstance(profiler, TimeProfiler)
                    mock_start.assert_called_once()
                
                mock_stop.assert_called_once()

class TestProfilers(unittest.TestCase):
    """Test the profiler implementations."""
    
    def test_null_profiler(self):
        """Test null profiler functionality."""
        profiler = NullProfiler()
        
        self.assertEqual(profiler.name, "null")
        self.assertEqual(profiler.file_extension, "txt")
        
        # Should not raise exceptions
        profiler.start()
        self.assertTrue(profiler.is_running)
        
        profiler.stop()
        self.assertFalse(profiler.is_running)
    
    @patch('debug.profilers.subprocess.Popen')
    def test_cpu_profiler(self, mock_popen):
        """Test CPU profiler functionality."""
        # Mock process
        mock_process = MagicMock()
        mock_popen.return_value = mock_process
        
        # Create profiler with specific output path
        profiler = CPUProfiler()
        profiler.output_path = "/tmp/test_cpu_profile.svg"
        
        # Start profiler
        profiler.start()
        self.assertTrue(profiler.is_running)
        mock_popen.assert_called_once()
        
        # Stop profiler
        profiler.stop()
        self.assertFalse(profiler.is_running)
        mock_process.terminate.assert_called_once()

if __name__ == "__main__":
    unittest.main()