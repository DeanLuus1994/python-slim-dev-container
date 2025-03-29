"""Command-line interface for the debugging framework."""

import os
import sys
import argparse
from typing import Dict, Any, Optional, List
from pathlib import Path

from .core import DebugCore
from .config import DebugConfig
from .log import get_debug_logger

logger = get_debug_logger()

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the debug CLI.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Python-Slim Debugging Framework",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Main command
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Enable debugging
    enable_parser = subparsers.add_parser("enable", help="Enable debugging")
    enable_parser.add_argument(
        "--profile", choices=["time", "memory", "cpu", "scalene", "none"],
        default="none", help="Profiling mode"
    )
    enable_parser.add_argument(
        "--level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO", help="Debug log level"
    )
    enable_parser.add_argument(
        "--output", type=str, help="Debug log output path"
    )
    
    # Enable debug server
    server_parser = subparsers.add_parser("server", help="Start debug server")
    server_parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Interface to listen on"
    )
    server_parser.add_argument(
        "--port", type=int, default=5678, help="Port to listen on"
    )
    server_parser.add_argument(
        "--wait", action="store_true", help="Wait for client to connect"
    )
    
    # Profile command
    profile_parser = subparsers.add_parser("profile", help="Profile Python code")
    profile_parser.add_argument(
        "script", type=str, help="Python script to profile"
    )
    profile_parser.add_argument(
        "--mode", choices=["time", "memory", "cpu", "scalene"],
        default="time", help="Profiling mode"
    )
    profile_parser.add_argument(
        "--output", type=str, help="Profile output path"
    )
    
    # Show configuration
    subparsers.add_parser("config", help="Show current debug configuration")
    
    return parser.parse_args()

def handle_enable(args: argparse.Namespace) -> int:
    """Handle the 'enable' command.
    
    Args:
        args: Command-line arguments
        
    Returns:
        int: Exit code
    """
    # Set environment variables for future processes
    os.environ["DEBUG_MODE"] = "1"
    os.environ["DEBUG_PROFILE"] = args.profile
    os.environ["DEBUG_LEVEL"] = args.level
    
    if args.output:
        os.environ["DEBUG_OUTPUT"] = args.output
    
    # Initialize debugging
    debugger = DebugCore()
    success = debugger.setup(
        profile_mode=args.profile,
        debug_level=args.level,
        debug_output=args.output
    )
    
    if success:
        logger.info("Debugging enabled successfully")
        return 0
    else:
        logger.error("Failed to enable debugging")
        return 1

def handle_server(args: argparse.Namespace) -> int:
    """Handle the 'server' command.
    
    Args:
        args: Command-line arguments
        
    Returns:
        int: Exit code
    """
    # Set environment variables
    os.environ["DEBUGPY_ENABLE"] = "1"
    os.environ["DEBUGPY_HOST"] = args.host
    os.environ["DEBUGPY_PORT"] = str(args.port)
    os.environ["DEBUGPY_WAIT"] = "1" if args.wait else "0"
    
    # Initialize debugging
    debugger = DebugCore()
    success = debugger.enable_debug_server(
        host=args.host,
        port=args.port,
        wait_for_client=args.wait
    )
    
    if success:
        logger.info(f"Debug server listening on {args.host}:{args.port}")
        if args.wait:
            logger.info("Waiting for client to connect...")
        
        # Keep the server running
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Debug server stopped")
            return 0
    else:
        logger.error("Failed to start debug server")
        return 1

def handle_profile(args: argparse.Namespace) -> int:
    """Handle the 'profile' command.
    
    Args:
        args: Command-line arguments
        
    Returns:
        int: Exit code
    """
    script_path = Path(args.script)
    if not script_path.exists():
        logger.error(f"Script not found: {args.script}")
        return 1
    
    # Set environment variables
    os.environ["DEBUG_MODE"] = "1"
    os.environ["DEBUG_PROFILE"] = args.mode
    
    # Create output path if not specified
    output_path = args.output
    if not output_path:
        timestamp = int(__import__("time").time())
        profiles_dir = Path(os.environ.get("PROFILES_DIR", "/tmp/profiles"))
        profiles_dir.mkdir(parents=True, exist_ok=True)
        
        extension = {
            "time": "html",
            "memory": "dat",
            "cpu": "svg",
            "scalene": "html"
        }.get(args.mode, "txt")
        
        output_path = str(profiles_dir / f"{script_path.stem}_{args.mode}_{timestamp}.{extension}")
    
    # Initialize debugger and run script with profiling
    debugger = DebugCore()
    with debugger.profile_context(args.mode, output_path):
        logger.info(f"Profiling {args.script} with {args.mode} profiler")
        
        # Execute the script
        script_globals = {
            "__file__": str(script_path),
            "__name__": "__main__"
        }
        
        with open(script_path, "r") as f:
            script_code = compile(f.read(), args.script, "exec")
            exec(script_code, script_globals)
    
    logger.info(f"Profile saved to: {output_path}")
    return 0

def handle_config(_: argparse.Namespace) -> int:
    """Handle the 'config' command.
    
    Args:
        _: Command-line arguments (unused)
        
    Returns:
        int: Exit code
    """
    config = DebugConfig()
    
    print("\nCurrent Debug Configuration:")
    print("-" * 30)
    
    # General settings
    print(f"Debug Mode      : {config.debug_mode}")
    print(f"Profile Mode    : {config.profile_mode}")
    print(f"Debug Level     : {config.debug_level}")
    print(f"Debug Output    : {config.debug_output or 'Console only'}")
    
    # Debugpy settings
    print("\nDebugpy Settings:")
    print(f"Enabled         : {config.debugpy_enable}")
    print(f"Wait for Client : {config.debugpy_wait}")
    print(f"Host            : {config.debugpy_host}")
    print(f"Port            : {config.debugpy_port}")
    
    # Profile settings
    print("\nProfile Settings:")
    print(f"Profiles Dir    : {config.profiles_dir}")
    
    # Environment variables
    print("\nEnvironment Variables:")
    for var in ["DEBUG_MODE", "DEBUG_PROFILE", "DEBUG_LEVEL", "DEBUG_OUTPUT",
               "DEBUGPY_ENABLE", "DEBUGPY_WAIT", "DEBUGPY_HOST", "DEBUGPY_PORT",
               "PROFILES_DIR"]:
        print(f"{var.ljust(16)}: {os.environ.get(var, 'Not set')}")
        
    return 0

def main() -> int:
    """Main entry point for the debug CLI.
    
    Returns:
        int: Exit code
    """
    args = parse_args()
    
    if args.command == "enable":
        return handle_enable(args)
    elif args.command == "server":
        return handle_server(args)
    elif args.command == "profile":
        return handle_profile(args)
    elif args.command == "config":
        return handle_config(args)
    else:
        # Show help if no command specified
        print("Please specify a command. Use --help for more information.")
        return 1

if __name__ == "__main__":
    sys.exit(main())