"""Memory detection and management utilities."""

import os
import platform
import subprocess
from typing import Dict
from ...log.logger import get_logger
from .commands import run_command

logger = get_logger()

def get_memory_info() -> Dict[str, int]:
    """Get information about system memory.
    
    Returns:
        Dictionary with total_mb and available_mb memory values
    """
    info = {"total_mb": 4096, "available_mb": 2048}
    system = platform.system().lower()
    
    try:
        if system == 'linux':
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    if "MemTotal" in line:
                        info["total_mb"] = int(int(line.split()[1]) / 1024)
                    elif "MemAvailable" in line:
                        info["available_mb"] = int(int(line.split()[1]) / 1024)
        
        elif system == 'windows':
            import ctypes
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            
            memory_status = MEMORYSTATUSEX()
            memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status))
            
            info["total_mb"] = int(memory_status.ullTotalPhys / (1024 * 1024))
            info["available_mb"] = int(memory_status.ullAvailPhys / (1024 * 1024))
        
        elif system == 'darwin':
            result = run_command(['sysctl', '-n', 'hw.memsize'])
            if result:
                info["total_mb"] = int(int(result) / (1024 * 1024))
                
            result = run_command(['vm_stat'])
            if result:
                page_size_result = run_command(['sysctl', '-n', 'hw.pagesize'])
                if page_size_result:
                    page_size = int(page_size_result)
                    free_pages = 0
                    for line in result.split('\n'):
                        if 'Pages free:' in line:
                            free_pages += int(line.split(':')[1].strip().replace('.', ''))
                        elif 'Pages inactive:' in line:
                            free_pages += int(line.split(':')[1].strip().replace('.', ''))
                    
                    info["available_mb"] = int((free_pages * page_size) / (1024 * 1024))
    
    except Exception as e:
        logger.warning(f"Error detecting memory info: {e}")
    
    return info