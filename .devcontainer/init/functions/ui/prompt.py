"""User prompt and interaction utilities."""

import os
import sys
from pathlib import Path
from typing import Optional
from ...log.logger import get_logger

logger = get_logger()

def color_text(text: str, color_code: str) -> str:
    """Apply color to text for terminal output.
    
    Args:
        text: Text to colorize
        color_code: ANSI color code
        
    Returns:
        Colorized text string
    """
    return f"{color_code}{text}\033[0m"

def green(text: str) -> str:
    """Format text in green color.
    
    Args:
        text: Text to colorize
        
    Returns:
        Green-colored text
    """
    return color_text(text, "\033[32m")

def yellow(text: str) -> str:
    """Format text in yellow color.
    
    Args:
        text: Text to colorize
        
    Returns:
        Yellow-colored text
    """
    return color_text(text, "\033[33m")

def blue(text: str) -> str:
    """Format text in blue color.
    
    Args:
        text: Text to colorize
        
    Returns:
        Blue-colored text
    """
    return color_text(text, "\033[36m")

def display_env_prompt(env_path: Path) -> bool:
    """Display environment variables and prompt for action.
    
    Args:
        env_path: Path to the environment file
        
    Returns:
        True if user wishes to continue, False otherwise
    """
    if not env_path.exists():
        logger.warning(f"Environment file not found: {env_path}")
        return False
    
    print("\n" + "="*80)
    print(f"{green('PYTHON-SLIM CONTAINER INITIALIZATION')}")
    print("="*80)
    print(f"\nFound environment file at: {blue(str(env_path))}")
    print("\nPlease review the environment settings below:\n")
    
    with open(env_path, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            try:
                key, value = line.split('=', 1)
                # Mask security tokens
                if any(secret in key.upper() for secret in ['TOKEN', 'PAT', 'SECRET', 'KEY']):
                    value = value[:4] + '*' * (len(value) - 4) if len(value) > 4 else '****'
                print(f"  {yellow(key)}={value}")
            except ValueError:
                print(f"  {line}")
        
    print("\nWould you like to:")
    print("  1. Continue with these settings")
    print("  2. Edit the environment file before continuing")
    print("  3. Abort initialization")
    
    choice = None
    while choice not in ['1', '2', '3']:
        choice = input(f"\n{green('Enter your choice (1-3)')} [1]: ") or '1'
    
    if choice == '2':
        edit_env_file(env_path)
        return True
    elif choice == '3':
        print(f"\n{yellow('Initialization aborted by user')}")
        sys.exit(0)
    
    return True

def edit_env_file(env_path: Path) -> None:
    """Open the environment file in an editor.
    
    Args:
        env_path: Path to the environment file
    """
    print(f"\nOpening {blue(str(env_path))} for editing...")
    
    # Try to find a suitable editor
    editor = os.environ.get('EDITOR', '')
    if not editor:
        for ed in ['nano', 'vim', 'vi', 'notepad', 'code']:
            if os.system(f"which {ed} >/dev/null 2>&1") == 0:
                editor = ed
                break
    
    if editor:
        os.system(f"{editor} {env_path}")
    else:
        print(f"\n{yellow('No editor found. Please edit the file manually at:')}")
        print(f"{blue(str(env_path))}")
        input(f"\n{green('Press Enter when finished editing...')}")