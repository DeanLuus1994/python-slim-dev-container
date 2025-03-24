"""GPU detection and setup utilities."""

import os
import platform
from typing import Dict, Any
from ...log.logger import get_logger
from ...core.system.commands import has_command, run_command

logger = get_logger()

def detect_gpu(resources: Dict[str, Any], 
               build_config: Dict[str, Any]) -> None:
    """Detect GPU hardware and update resources dictionary.
    
    Args:
        resources: Resources dictionary to update
        build_config: Build configuration dictionary
    """
    if has_command("nvidia-smi"):
        try:
            result = run_command(["nvidia-smi", "-L"])
            if result:
                resources["gpu_detected"] = True
                resources["gpu_vendor"] = "nvidia"
                result = run_command([
                    "nvidia-smi", "--query-gpu=memory.total", 
                    "--format=csv,noheader"
                ])
                if result:
                    resources["gpu_memory_mb"] = int(result.split()[0])
                setup_gpu_env(build_config)
        except:
            pass
    elif has_command("rocm-smi"):
        try:
            result = run_command(["rocm-smi", "--showmeminfo", "vram"])
            if result:
                resources["gpu_detected"] = True
                resources["gpu_vendor"] = "amd"
                for line in result.split("\n"):
                    if "GPU memory" in line:
                        try:
                            memory_mb = int(line.split(":")[1].strip().split()[0])
                            resources["gpu_memory_mb"] = memory_mb
                        except:
                            pass
        except:
            pass
    elif platform.system().lower() == "darwin" and has_command("system_profiler"):
        try:
            result = run_command(["system_profiler", "SPDisplaysDataType"])
            if result and ("Metal" in result or "Supported" in result):
                resources["gpu_detected"] = True
                resources["gpu_vendor"] = "apple"
                for line in result.split("\n"):
                    if "VRAM" in line:
                        try:
                            memory_mb = int(line.split(":")[1].strip().split()[0])
                            resources["gpu_memory_mb"] = memory_mb
                        except:
                            pass
        except:
            pass

def setup_gpu_env(build_config: Dict[str, Any]) -> None:
    """Configure environment variables for GPU support.
    
    Args:
        build_config: Build configuration dictionary
    """
    if "CUDA_HOME" in os.environ:
        cuda_home = os.environ["CUDA_HOME"]
        os.environ["PATH"] = f"{cuda_home}/bin:{os.environ['PATH']}"
        ld_path = os.environ.get("LD_LIBRARY_PATH", "")
        os.environ["LD_LIBRARY_PATH"] = f"{cuda_home}/lib64:{ld_path}"
        
    gpu_cache = build_config.get("paths", {}).get("gpu_cache")
    if gpu_cache:
        os.makedirs(gpu_cache, exist_ok=True)
        os.environ["CUDA_CACHE_PATH"] = gpu_cache
        os.environ["CUDA_CACHE_MAXSIZE"] = str(
            build_config.get("cuda", {}).get("cache_maxsize", "2147483648")
        )