"""Path utilities for working with project and system directories."""

import os
from pathlib import Path
from ...log.logger import get_logger

logger = get_logger()

def get_project_root() -> Path:
    """Get the root directory of the project.
    
    Tries to determine the project root from environment variables,
    falls back to the parent of the current directory.
    
    Returns:
        Path object representing the project root directory
    """
    try:
        if "WORKSPACE_FOLDER" in os.environ and "PROJECT_NAME" in os.environ:
            workspace = os.environ["WORKSPACE_FOLDER"]
            project = os.environ["PROJECT_NAME"]
            root = Path(f"/{workspace}/{project}")
            if root.exists():
                return root
    except Exception as e:
        logger.error(f"Error determining project root: {e}")
    
    # Fallback: navigate up from the current file
    return Path(__file__).resolve().parent.parent.parent.parent.parent