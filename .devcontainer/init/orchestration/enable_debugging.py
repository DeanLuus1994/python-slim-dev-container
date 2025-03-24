import debugpy
import time
import sys
import os

def main():
    """Enable remote debugging for processes in the container."""
    print("Enabling remote debugging on port 5678...")
    debugpy.listen(("0.0.0.0", 5678))
    print("Debug server is running on port 5678")
    print("Waiting for debugger to attach...")
    
    if "--wait-for-client" in sys.argv:
        debugpy.wait_for_client()
        print("Debugger attached!")
    
    print(f"Current environment: {os.environ.get('WORKSPACE_FOLDER', 'workspace')}/{os.environ.get('PROJECT_NAME', 'python-slim')}")
    
    # Keep debug server running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Debug server stopped")

if __name__ == "__main__":
    main()