"""Tests for the resource detection functionality."""
import platform
from typing import Dict, Any
import pytest
from unittest.mock import patch, MagicMock
from ..resource.detection import detect_resources

def test_detect_resources_config_override(sample_build_config: Dict[str, Any]) -> None:
    """Test that resource configuration can be overridden by build config."""
    with patch('platform.machine', return_value='x86_64'), \
         patch('..core.system.cpu.get_cpu_count', return_value=8), \
         patch('..core.system.memory.get_memory_info', 
               return_value={"total_mb": 16384, "available_mb": 8192}), \
         patch('..resource.gpu.detect_gpu'):
        
        resources = detect_resources(sample_build_config)
        
        # Check that build config overrides are applied
        assert resources["cores"] == 2  # From sample_build_config
        assert resources["threads"] == 4  # From sample_build_config
        assert resources["build_jobs"] == 2  # From sample_build_config
        
        # Check that detected values are preserved
        assert resources["ram_mb"] == 16384
        assert resources["available_ram_mb"] == 8192
        assert resources["architecture"] == "x86_64"