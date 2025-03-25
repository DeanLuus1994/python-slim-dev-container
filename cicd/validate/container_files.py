#!/usr/bin/env python3
"""
Validate container files in .devcontainer.
"""

import os
import sys

def check_file(path: str) -> bool:
    if not (os.path.exists(path) and os.path.isfile(path)):
        print(f"Error: '{path}' missing/invalid.")
        return False
    return True

def main() -> None:
    files = [
        os.path.join(".devcontainer", "Dockerfile"),
        os.path.join(".devcontainer", "docker-compose.yml"),
    ]
    ok = True
    for f in files:
        if not check_file(f):
            ok = False
    if ok:
        print("Container files OK.")
        sys.exit(0)
    sys.exit(1)

if __name__ == "__main__":
    main()