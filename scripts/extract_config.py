#!/usr/bin/env python3
"""Extract container configuration from pyproject.toml."""

import tomli
import sys
from pathlib import Path


def main():
    """Extract configuration and output as environment variables."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    
    with open(pyproject_path, "rb") as f:
        pyproject = tomli.load(f)
    
    # Changed from container to slimdev to match actual config section
    container_config = pyproject.get("tool", {}).get("slimdev", {})
    
    if not container_config:
        print("Error: No tool.slimdev section found in pyproject.toml", file=sys.stderr)
        sys.exit(1)
    
    # Output as environment variables
    for key, value in container_config.items():
        key = key.upper()
        if isinstance(value, bool):
            value = str(value).lower()
        print(f"{key}={value}")


if __name__ == "__main__":
    main()