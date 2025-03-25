#!/usr/bin/env python3
"""
Validate essential config files.
"""

import os
import sys

def check_exists(path: str) -> bool:
    if not os.path.exists(path):
        print(f"Error: '{path}' missing.")
        return False
    return True

def main() -> None:
    paths = [
        "pyproject.toml",
        ".flake8",
        ".env",
        os.path.join(".github", "dependabot.yml"),
    ]
    ok = True
    for p in paths:
        if not check_exists(p):
            ok = False
    if ok:
        print("Config files OK.")
        sys.exit(0)
    sys.exit(1)

if __name__ == "__main__":
    main()