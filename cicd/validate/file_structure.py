#!/usr/bin/env python3
"""
Validate project file structure.
"""

import os
import sys

def check_exists(path: str) -> bool:
    if not os.path.exists(path):
        print(f"Error: '{path}' missing.")
        return False
    return True

def main() -> None:
    reqs = [
        ".devcontainer/Dockerfile",
        ".devcontainer/docker-compose.yml",
        ".env", "pyproject.toml", ".flake8",
        os.path.join(".github", "dependabot.yml"),
    ]
    all_ok = True
    for p in reqs:
        if not check_exists(p):
            all_ok = False
    if all_ok:
        print("File structure OK.")
        sys.exit(0)
    sys.exit(1)

if __name__ == "__main__":
    main()