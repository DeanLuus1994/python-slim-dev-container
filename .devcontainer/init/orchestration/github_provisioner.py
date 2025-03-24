"""GitHub repository provisioning functionality."""

import os
import sys
import atexit
from pathlib import Path
from typing import List, Tuple
from ..log.logger import get_logger
from ..core.system.commands import has_command
from ..core.utils.validation import validate_executable
from ..functions.vcs.git import setup_git_config
from ..functions.vcs.repository import process_solution_repo, process_local_repos
from ..functions.concurrency.executor import shutdown_executors

logger = get_logger()
atexit.register(shutdown_executors)

def verify_git_installed() -> Tuple[bool, List[str]]:
    """Verify that required Git tools are installed.
    
    Returns:
        Tuple of (all_tools_installed, list_of_missing_tools)
    """
    missing = []
    if not validate_executable("git"):
        missing.append("git")
    if not validate_executable("git-lfs"):
        logger.warning("git-lfs not found, large files may not be handled properly")
    return len(missing) == 0, missing

def main() -> int:
    """Main entry point for GitHub repository provisioning.
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    logger.info("Starting GitHub repository provisioning")
    git_ok, missing = verify_git_installed()
    if not git_ok:
        logger.error(f"Required tools not installed: {', '.join(missing)}")
        return 1
    try:
        setup_git_config()
        solution_result = process_solution_repo()
        if solution_result:
            logger.info(f"Solution repository processed: {solution_result}")
        repos_processed = process_local_repos()
        if repos_processed:
            logger.info(f"Processed {len(repos_processed)} local repositories")
        logger.info("GitHub repository provisioning completed")
        return 0
    except Exception as e:
        logger.error(f"Error in GitHub provisioning: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())