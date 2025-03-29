#!/usr/bin/env python3
"""
Generate configuration for the development container.

This script is a convenience wrapper around slimdev.config functionality.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from slimdev.config import generate_env
    
    generate_env()
except ImportError:
    print("Error: slimdev package not found. Make sure you're running from the project root.", 
          file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error generating configuration: {str(e)}", file=sys.stderr)
    sys.exit(1)