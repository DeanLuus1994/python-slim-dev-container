#!/usr/bin/env python3
"""
Verify that all requirements are pinned.
"""

import os
import sys

def main() -> None:
    req_file = os.path.join(".devcontainer", "requirements.txt")
    if not os.path.exists(req_file):
        print("Error: requirements.txt missing.")
        sys.exit(1)
    all_pinned = True
    with open(req_file, "r", encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            if "==" not in ln:
                print("Error: Unpinned req:", ln)
                all_pinned = False
    if all_pinned:
        print("All requirements are pinned.")
        sys.exit(0)
    sys.exit(1)

if __name__ == "__main__":
    main()