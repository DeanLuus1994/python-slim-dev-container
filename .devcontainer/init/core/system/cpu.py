"""CPU detection and information utilities."""

import platform
import subprocess
import multiprocessing
from typing import Set, Dict, Any, List, Optional
from ...log.logger import get_logger

logger = get_logger()

def run_cpu_command(args: List[str]) -> Optional[str]:
    """Execute a command for CPU detection and return its output.
    
    Args:
        args: Command and arguments to execute
        
    Returns:
        Command output as string, or None if command failed
    """
    if not args:
        return None
    cmd_str = " ".join(args)
    try:
        result = subprocess.run(
            args, check=True, stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        logger.debug(f"Error executing CPU detection command {cmd_str}: {str(e)}")
        return None

def detect_cpu_features() -> Set[str]:
    """Detect CPU features like architecture and instruction set extensions.
    
    Returns:
        Set of CPU feature strings (e.g., 'x86_64', 'avx2', 'fma', 'arm64')
    """
    features = set()
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if machine in ('x86_64', 'amd64', 'x64'):
        features.add('x86_64')
        if system == 'linux':
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    cpuinfo = f.read().lower()
                    if 'avx2' in cpuinfo:
                        features.add('avx2')
                    if 'fma' in cpuinfo:
                        features.add('fma')
            except Exception as e:
                logger.debug(f"Error detecting CPU features: {e}")
        elif system == 'windows':
            try:
                import ctypes
                for feature, bit in [(10, 'sse3'), (14, 'avx'), 
                                    (17, 'avx2'), (12, 'fma')]:
                    if ctypes.windll.kernel32.IsProcessorFeaturePresent(feature):
                        features.add(bit)
            except Exception as e:
                logger.debug(f"Error detecting Windows CPU features: {e}")
        elif system == 'darwin':
            try:
                result = run_cpu_command(['sysctl', '-n', 'machdep.cpu.features'])
                if result:
                    cpu_features = result.lower()
                    if 'avx2' in cpu_features:
                        features.add('avx2')
                    if 'fma' in cpu_features:
                        features.add('fma')
            except Exception as e:
                logger.debug(f"Error detecting Mac CPU features: {e}")
    elif 'arm' in machine or 'aarch64' in machine:
        features.add('arm')
        if '64' in machine:
            features.add('arm64')
    
    logger.debug(f"Detected CPU features: {features}")
    return features

def get_cpu_count() -> int:
    """Get the number of CPU cores.
    
    Returns:
        Number of CPU cores, or 1 if detection fails
    """
    try:
        return multiprocessing.cpu_count()
    except:
        logger.debug("Failed to detect CPU count, using default of 1")
        return 1

def get_cpu_info() -> Dict[str, Any]:
    """Get comprehensive CPU information.
    
    Returns:
        Dictionary with CPU details including count, features, 
        architecture, and model
    """
    info = {
        "count": get_cpu_count(),
        "features": detect_cpu_features(),
        "architecture": platform.machine().lower(),
        "processor": platform.processor()
    }
    
    system = platform.system().lower()
    if system == 'linux':
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
                for line in cpuinfo.split('\n'):
                    if 'model name' in line:
                        info["model"] = line.split(':')[1].strip()
                        break
        except:
            pass
    elif system == 'darwin':
        try:
            result = run_cpu_command(['sysctl', '-n', 'machdep.cpu.brand_string'])
            if result:
                info["model"] = result
        except:
            pass
    elif system == 'windows':
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                               r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as key:
                info["model"] = winreg.QueryValueEx(key, "ProcessorNameString")[0]
        except:
            pass
    
    return info