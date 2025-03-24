"""Version control utilities for Git and GitHub.

This subpackage provides functionality for managing Git repositories,
handling GitHub operations, and automating version control tasks.
"""

from .git import setup_git_config, clone_or_update_repo, setup_lfs
from .repository import process_solution_repo, process_local_repos

__all__ = [
    'setup_git_config', 'clone_or_update_repo', 'setup_lfs',
    'process_solution_repo', 'process_local_repos'
]