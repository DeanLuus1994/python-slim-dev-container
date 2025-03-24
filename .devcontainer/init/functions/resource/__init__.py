"""Resource detection and management utilities.

This subpackage provides functionality for detecting system resources like
CPU, memory, and GPU, and configuring the environment accordingly.
"""

from .detection import detect_resources, log_resources
from .gpu import detect_gpu, setup_gpu_env

__all__ = [
    'detect_resources', 'log_resources',
    'detect_gpu', 'setup_gpu_env'
]