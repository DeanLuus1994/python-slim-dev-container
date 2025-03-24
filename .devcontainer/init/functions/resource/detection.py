"""Resource detection functionality."""

import os
import platform
from typing import Dict, Any
from ...log.logger import get_logger
from ...core.system.memory import get_memory_info
from ...core.system.cpu import get_cpu_count
from .gpu import detect_gpu

logger = get_logger()

def detect_resources(build_config: Dict[str, Any]) -> Dict[str, Any]:
    """Detect system resources and prepare configuration.
    
    Args:
        build_config: Build configuration dictionary
        
    Returns:
        Dictionary containing detected resources
    """
    resources = {
        "cores": 1,
        "threads": 1,
        "ram_mb": 4096,
        "available_ram_mb": 2048,
        "gpu_detected": False,
        "gpu_memory_mb": 0,
        "gpu_vendor": None,
        "architecture": platform.machine().lower()
    }
    
    try:
        resources["cores"] = get_cpu_count()
        resources["threads"] = resources["cores"]
    except:
        logger.warning("Failed to detect CPU count")
        
    mem_info = get_memory_info()
    resources["ram_mb"] = mem_info["total_mb"]
    resources["available_ram_mb"] = mem_info["available_mb"]
    
    detect_gpu(resources, build_config)
    
    config_resources = build_config.get("resources", {})
    for key, cfg_key in {
        "cores": "default_cores", 
        "threads": "default_threads",
        "ram_mb": "ram_disk_size"
    }.items():
        if cfg_key in config_resources and config_resources[cfg_key] > 0:
            resources[key] = config_resources[cfg_key]
            
    build_jobs = config_resources.get("build_jobs", 0)
    resources["build_jobs"] = build_jobs if build_jobs > 0 else resources["threads"]
    
    log_resources(resources)
    return resources

def log_resources(resources: Dict[str, Any]) -> None:
    """Log detected system resources.
    
    Args:
        resources: Dictionary containing resource information
    """
    logger.info(
        f"Resources: {resources['cores']} cores, "
        f"{resources['threads']} threads, {resources['ram_mb']}MB RAM"
    )
    
    if resources["gpu_detected"]:
        logger.info(
            f"GPU detected: {resources['gpu_vendor']} "
            f"with {resources['gpu_memory_mb']}MB VRAM"
        )
    else:
        logger.info("No GPU detected, using CPU-only optimizations")