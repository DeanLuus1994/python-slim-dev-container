#!/usr/bin/env python3
"""
Verify critical environment variables in .env.
"""

import os
import sys

def main() -> None:
    env_file = os.path.join(".devcontainer", ".env")
    if not os.path.exists(env_file):
        print("Error: .env missing.")
        sys.exit(1)
    req_keys = [
        "CPUS", "MEMORY", "STORAGE", "DEV_CONTAINER_NAME",
        "DEV_MODE", "USE_ROOT_USER", "ZSH_AUTOSUGGESTIONS_REPO",
        "USERNAME",
    ]
    env_vars = {}
    with open(env_file, "r", encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            parts = ln.split("=", 1)
            if len(parts) == 2:
                env_vars[parts[0].strip()] = parts[1].strip()
    ok = True
    for key in req_keys:
        if key not in env_vars or not env_vars[key]:
            print(f"Error: {key} not set.")
            ok = False
        else:
            print(f"[OK] {key}")
    if ok:
        print("All env vars set.")
        sys.exit(0)
    sys.exit(1)

if __name__ == "__main__":
    main()