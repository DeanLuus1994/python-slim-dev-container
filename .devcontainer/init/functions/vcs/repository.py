"""Repository management utilities."""

import os
from pathlib import Path
from typing import List, Optional
from ...log.logger import get_logger
from ...core.config.loader import load_config
from ...core.utils.validation import validate_path, ensure_list
from .git import clone_or_update_repo

logger = get_logger()

def process_solution_repo() -> Optional[str]:
    """Process the solution repository specified in config.
    
    Returns:
        Repository name if successful, None otherwise
    """
    try:
        config = load_config("github")
        solution_repo = config.get('repositories', {}).get('solution')
        
        if not solution_repo:
            logger.warning("No solution repository defined")
            return None
        
        workspace_root = os.environ.get('WORKSPACE_FOLDER', 'workspace')
        project_name = os.environ.get('PROJECT_NAME', 'python-slim')
        root_path = Path(f"/{workspace_root}/{project_name}")
        validate_path(root_path, create_dir=True)
        solution_path = root_path / 'solution'
        
        token = config.get('token', os.environ.get('GITHUB_PAT', ''))
        if not token:
            logger.error("GitHub token not found")
            return None
            
        solution_url = f"https://{token}@github.com/{solution_repo}.git"
        logger.info(f"Processing solution repository: {solution_repo}")
        
        return clone_or_update_repo(str(solution_path), solution_url)
    except Exception as e:
        logger.error(f"Error processing solution repo: {e}")
        return None

def process_local_repos() -> List[str]:
    """Process local repositories specified in environment variables.
    
    Returns:
        List of successfully processed repository names
    """
    try:
        config = load_config("github")
        local_repos_str = os.environ.get('GITHUB_LOCAL_REPOS', '')
        
        if not local_repos_str:
            logger.info("No local repositories specified")
            return []
            
        local_repos = local_repos_str.split(',')
        workspace_folder = os.environ.get('WORKSPACE_FOLDER', 'workspace')
        project_name = os.environ.get('PROJECT_NAME', 'python-slim')
        root_path = Path(f"/{workspace_folder}/{project_name}")
        validate_path(root_path, create_dir=True)
        
        github_username = os.environ.get('GITHUB_USERNAME')
        github_token = config.get('token', os.environ.get('GITHUB_PAT', ''))
        
        if not github_username or not github_token:
            logger.error("GitHub username or token not found")
            return []
            
        repos_config = {}
        for repo in local_repos:
            repo_name = repo.split('/')[-1] if '/' in repo else repo
            repo_url = f"https://{github_token}@github.com/{github_username}/{repo}.git"
            repos_config[repo_name] = repo_url
            
        # Process repositories sequentially with user interaction
        processed_repos = []
        for repo_name, repo_url in repos_config.items():
            try:
                repo_path = root_path / repo_name
                result = clone_or_update_repo(str(repo_path), repo_url)
                if result:
                    processed_repos.append(result)
            except Exception as e:
                logger.error(f"Error processing repository {repo_name}: {e}")
                
        return processed_repos
    except Exception as e:
        logger.error(f"Error processing local repositories: {e}")
        return []