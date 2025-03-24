"""Compiler optimization utilities."""

import os
from typing import Dict, Any, Set
from ...log.logger import get_logger
from ...core.system.commands import has_command, run_command

logger = get_logger()

def setup_ccache(build_config: Dict[str, Any], 
                python_config: Dict[str, Any]) -> bool:
    """Configure ccache for compiler acceleration.
    
    Args:
        build_config: Build configuration dictionary
        python_config: Python configuration dictionary
        
    Returns:
        True if successful, False otherwise
    """
    if not has_command("ccache"):
        logger.warning("ccache not found, skipping configuration")
        return False
        
    try:
        ccache_dir = build_config.get("paths", {}).get("build_cache")
        if ccache_dir:
            os.makedirs(ccache_dir, exist_ok=True)
            os.environ["CCACHE_DIR"] = ccache_dir
            
        compiler_config = python_config.get("compiler", {})
        if compiler_config:
            for key, env_key in [
                ("cc", "CC"), ("cxx", "CXX"), ("makeflags", "MAKEFLAGS")
            ]:
                if key in compiler_config:
                    os.environ[env_key] = compiler_config[key]
                    
        max_size = build_config.get("ccache", {}).get("max_size", "5G")
        run_command(["ccache", "-M", max_size], check=False)
        run_command(["ccache", "-z"], check=False)
        logger.info(f"ccache configured with max size {max_size}")
        return True
    except Exception as e:
        logger.error(f"Error setting up ccache: {e}")
        return False

def apply_compiler_flags(build_config: Dict[str, Any], 
                        cpu_features: Set[str]) -> bool:
    """Apply CPU-specific compiler optimization flags.
    
    Args:
        build_config: Build configuration dictionary
        cpu_features: Set of detected CPU features
        
    Returns:
        True if successful, False otherwise
    """
    try:
        flags = []
        if "x86_64" in cpu_features:
            flags.extend(["-march=native", "-mtune=native"])
            if "avx2" in cpu_features:
                flags.append("-mavx2")
            if "fma" in cpu_features:
                flags.append("-mfma")
        elif "arm64" in cpu_features:
            flags.append("-march=native")
            
        if flags:
            for env_var in ["CFLAGS", "CXXFLAGS"]:
                current = os.environ.get(env_var, "")
                if current:
                    os.environ[env_var] = f"{current} {' '.join(flags)}"
                else:
                    os.environ[env_var] = " ".join(flags)
            logger.info(f"Applied compiler flags: {' '.join(flags)}")
            
        return True
    except Exception as e:
        logger.error(f"Error applying compiler flags: {e}")
        return False