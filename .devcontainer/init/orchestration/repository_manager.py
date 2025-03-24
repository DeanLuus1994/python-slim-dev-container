"""Repository management functionality."""

import os
import traceback
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from ..log.logger import get_logger
from ..core.system.commands import run_command
from ..functions.vcs.git import clone_or_update_repo
from ..functions.ui.prompt import blue, green, yellow

logger = get_logger()

def check_repository_status(repo_path: Path) -> Tuple[bool, bool, bool]:
    """Check the status of a repository.
    
    Args:
        repo_path: Path to the repository
        
    Returns:
        Tuple of (exists, has_local_changes, has_remote_changes)
    """
    if not repo_path.exists() or not (repo_path / ".git").exists():
        return False, False, False
    
    # Check for local changes
    result = run_command(["git", "-C", str(repo_path), "status", "--porcelain"])
    has_changes = bool(result and result.strip())
    
    # Check for remote changes
    run_command(["git", "-C", str(repo_path), "fetch", "origin"], check=False)
    result = run_command([
        "git", "-C", str(repo_path), "rev-list", "HEAD..@{upstream}", "--count"
    ], check=False)
    
    # Ensure result is a boolean
    has_remote_changes = bool(result and result.strip() and result.strip() != "0")
    
    return True, has_changes, has_remote_changes

def manage_repository(repo_name: str, repo_url: str, repo_path: Path, 
                      force: bool = False, dry_run: bool = False) -> str:
    """Manage a repository - clone, update, or handle conflicts.
    
    Args:
        repo_name: Name of the repository
        repo_url: URL to clone from
        repo_path: Local path for the repository
        force: If True, automatically reset local changes without prompt
        dry_run: If True, simulate the operation without making changes
        
    Returns:
        Repository name if successful
    """
    exists, has_changes, has_remote_changes = check_repository_status(repo_path)
    if not exists:
        logger.info(f"Cloning repository: {repo_name}")
        if dry_run:
            logger.info(f"[DRY RUN] Would clone {repo_name} from {repo_url}")
            return repo_name
        return clone_or_update_repo(str(repo_path), repo_url)
    
    print(f"\nRepository {blue(repo_name)} already exists at {blue(str(repo_path))}")
    
    if has_changes:
        if force or dry_run:
            action = "2"  # Force reset to remote state in force mode or simulate in dry run
            if dry_run:
                logger.info(f"[DRY RUN] Would reset {repo_name} to remote state (discard local changes)")
                return repo_name
            logger.info(f"Force mode enabled: resetting {repo_name} to remote state")
            run_command(["git", "-C", str(repo_path), "fetch", "origin"])
            branch = run_command([
                "git", "-C", str(repo_path), "rev-parse", "--abbrev-ref", "HEAD"
            ])
            run_command([
                "git", "-C", str(repo_path), "reset", "--hard", f"origin/{branch}"
            ])
        else:
            print(f"{yellow('Local changes detected!')} What would you like to do?")
            print("  1. Keep changes and pull updates (may cause conflicts)")
            print("  2. Reset to remote state (will discard all local changes)")
            print("  3. Skip updating this repository")
            choice = None
            while choice not in ['1', '2', '3']:
                choice = input(f"\n{green('Enter your choice (1-3)')} [3]: ") or '3'
            
            if choice == '1':
                logger.info(f"Pulling updates for {repo_name} (keeping local changes)")
                run_command(["git", "-C", str(repo_path), "pull", "--rebase=false"])
            elif choice == '2':
                logger.info(f"Resetting {repo_name} to remote state")
                run_command(["git", "-C", str(repo_path), "fetch", "origin"])
                branch = run_command([
                    "git", "-C", str(repo_path), "rev-parse", "--abbrev-ref", "HEAD"
                ])
                run_command([
                    "git", "-C", str(repo_path), "reset", "--hard", f"origin/{branch}"
                ])
            # Else, skip updating
    else:
        if has_remote_changes:
            logger.info(f"Pulling updates for {repo_name}")
            run_command(["git", "-C", str(repo_path), "pull"])
        else:
            logger.info(f"Repository {repo_name} is up to date")
    
    return repo_name

def manage_repositories(root_path: Path, repos_config: Dict[str, str], 
                          force: bool = False, dry_run: bool = False) -> List[str]:
    """Manage multiple repositories.
    
    Args:
        root_path: Root directory for repositories
        repos_config: Dictionary of repository names and URLs
        force: If True, automatically reset local changes without prompting
        dry_run: If True, simulate updates without making changes
        
    Returns:
        List of successfully managed repository names
    """
    managed_repos = []
    for repo_name, repo_url in repos_config.items():
        repo_path = root_path / repo_name
        try:
            result = manage_repository(repo_name, repo_url, repo_path, force=force, dry_run=dry_run)
            if result:
                managed_repos.append(result)
        except Exception as e:
            logger.error(f"Error managing repository {repo_name}: {e}")
            logger.debug(traceback.format_exc())
    
    return managed_repos