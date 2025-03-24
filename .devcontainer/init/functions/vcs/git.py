"""Git operations utilities."""

import os
from pathlib import Path
from ...log.logger import get_logger
from ...core.system.commands import run_command

logger = get_logger()

def setup_git_config() -> None:
    """Configure Git global settings for better repository management."""
    configs = [
        ["credential.helper", "store"],
        ["user.name", os.environ.get("GITHUB_USERNAME", "GitHub User")],
        ["user.email", os.environ.get("GITHUB_EMAIL", "user@example.com")],
        ["core.autocrlf", "input"],
        ["init.defaultBranch", "main"],
        ["pull.rebase", "false"],
        ["fetch.parallel", "0"]
    ]
    
    for name, value in configs:
        run_command(["git", "config", "--global", name, value])

def clone_or_update_repo(repo_path: str, repo_url: str) -> str:
    """Clone or update a Git repository.
    
    Args:
        repo_path: Local path for the repository
        repo_url: URL to clone from
        
    Returns:
        Repository name
    """
    repo_name = Path(repo_path).name
    
    if Path(repo_path).joinpath(".git").is_dir():
        # Update existing repository
        run_command([
            "git", "-C", repo_path, "fetch", "--all", "--prune", "--jobs=4"
        ])
        
        current_branch = run_command([
            "git", "-C", repo_path, "symbolic-ref", "--short", "HEAD"
        ])
        
        run_command([
            "git", "-C", repo_path, "reset", "--hard", f"origin/{current_branch}"
        ])
        
        run_command([
            "git", "-C", repo_path, "submodule", "update", "--init", 
            "--recursive", "--jobs=4"
        ])
    else:
        # Clone new repository
        run_command([
            "git", "clone", "--recursive", "--jobs=4", repo_url, repo_path
        ])
    
    setup_lfs(repo_path)
    logger.info(f"✓ {repo_name} ready")
    return repo_name

def setup_lfs(repo_path: str) -> None:
    """Configure Git LFS for a repository if needed.
    
    Args:
        repo_path: Path to the repository
    """
    gitattributes = Path(repo_path) / ".gitattributes"
    
    if gitattributes.exists():
        with open(gitattributes, 'r') as f:
            if "lfs" in f.read():
                run_command(["git", "-C", repo_path, "lfs", "install"])
                run_command(["git", "-C", repo_path, "lfs", "pull"])