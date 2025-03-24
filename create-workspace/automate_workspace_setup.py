#!/usr/bin/env python3

import os
import sys
import shutil
import tempfile
import subprocess
import importlib.util
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("workspace-automation")

REQUIRED_PACKAGES = [
    "pytest>=6.0.0",
    "pyyaml>=6.0",
    "rich>=10.0.0",
    "typer>=0.4.0",
    "pydantic>=1.9.0",
    "black>=22.3.0",
    "isort>=5.10.1",
    "flake8>=4.0.1",
]

def run_command(cmd, cwd=None, env=None):
    """Run a shell command and return the result"""
    logger.info(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(
        cmd, 
        cwd=cwd, 
        env=env, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    
    if result.returncode != 0:
        logger.error(f"Command failed with code {result.returncode}")
        logger.error(f"STDERR: {result.stderr}")
        return False, result.stdout, result.stderr
    
    return True, result.stdout, result.stderr

def test_workspace_creation():
    """Run tests on the workspace creation functionality"""
    logger.info("=== STEP 1: Testing workspace creation ===")
    
    # Create a temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    logger.info(f"Created temporary test directory: {temp_dir}")
    
    try:
        # Import the create_workspace function
        module_path = Path(__file__).parent / "create_workspace.py"
        spec = importlib.util.spec_from_file_location("create_workspace", module_path)
        create_workspace_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(create_workspace_module)
        
        # Create a test workspace in the temporary directory
        test_workspace_dir = Path(temp_dir) / "test_workspace"
        logger.info(f"Creating test workspace at: {test_workspace_dir}")
        create_workspace_module.create_workspace(test_workspace_dir)
        
        # Verify that key directories and files exist
        expected_paths = [
            ".devcontainer/container/config.yaml",
            ".devcontainer/init/core/config/__init__.py",
            "accelerators/__init__.py",
            "api/__init__.py",
            "ai_integration/__init__.py",
            "README.md",
            "pyproject.toml",
        ]
        
        all_paths_exist = True
        for path in expected_paths:
            full_path = test_workspace_dir / path
            if not full_path.exists():
                logger.error(f"Expected path does not exist: {path}")
                all_paths_exist = False
        
        if all_paths_exist:
            logger.info("✅ Workspace structure validation passed")
            return True
        else:
            logger.error("❌ Workspace structure validation failed")
            return False
    
    except Exception as e:
        logger.error(f"An error occurred during testing: {str(e)}")
        return False
    
    finally:
        # Clean up the temporary directory
        logger.info(f"Cleaning up temporary directory: {temp_dir}")
        shutil.rmtree(temp_dir)

def validate_dependencies():
    """Validate compatibility of required dependencies"""
    logger.info("=== STEP 2: Validating dependencies ===")
    
    # Try importing key modules to validate installations
    try:
        import pkg_resources
        
        # Check if packages are installed
        for package_req in REQUIRED_PACKAGES:
            package_name = package_req.split('>=')[0]
            try:
                pkg_resources.get_distribution(package_name)
                logger.info(f"✓ {package_name} is already installed")
            except pkg_resources.DistributionNotFound:
                logger.warning(f"✗ {package_name} is not installed")
                
        logger.info("Dependency validation completed")
        return True
    
    except Exception as e:
        logger.error(f"Dependency validation failed: {str(e)}")
        return False

def install_dependencies():
    """Install required dependencies"""
    logger.info("=== STEP 3: Installing dependencies ===")
    
    # Install required packages
    success, stdout, stderr = run_command(
        [sys.executable, "-m", "pip", "install", "--upgrade"] + REQUIRED_PACKAGES
    )
    
    if success:
        logger.info("✅ Dependencies installed successfully")
        return True
    else:
        logger.error("❌ Failed to install dependencies")
        return False

def create_production_workspace(path=None):
    """Create the actual production workspace"""
    logger.info("=== STEP 4: Creating production workspace ===")
    
    if path is None:
        # Default to parent directory
        path = Path(__file__).parent.parent
    
    # Import the create_workspace function
    module_path = Path(__file__).parent / "create_workspace.py"
    spec = importlib.util.spec_from_file_location("create_workspace", module_path)
    create_workspace_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(create_workspace_module)
    
    try:
        # Create the production workspace
        logger.info(f"Creating workspace at: {path}")
        create_workspace_module.create_workspace(path)
        logger.info("✅ Production workspace created successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create production workspace: {str(e)}")
        return False

def run_pytest():
    """Run pytest on the tests directory"""
    logger.info("Running pytest for more thorough testing")
    
    success, stdout, stderr = run_command(
        [sys.executable, "-m", "pytest", "-v"],
        cwd=Path(__file__).parent
    )
    
    if success:
        logger.info("✅ Pytest tests passed")
        return True
    else:
        logger.error("❌ Pytest tests failed")
        logger.error(stderr)
        return False

def main():
    """Main function to orchestrate the automation process"""
    logger.info("Starting workspace setup automation")
    
    # Step 1: Test workspace creation
    if not test_workspace_creation():
        logger.error("Testing failed. Aborting automation.")
        return False
    
    # Optional: Run pytest for additional testing
    run_pytest()
    
    # Step 2: Validate dependencies
    if not validate_dependencies():
        logger.warning("Dependency validation had issues. Continuing with installation...")
    
    # Step 3: Install dependencies
    if not install_dependencies():
        logger.error("Dependency installation failed. Aborting automation.")
        return False
    
    # Step 4: Create production workspace
    target_path = None
    if len(sys.argv) > 1:
        target_path = Path(sys.argv[1])
    
    if not create_production_workspace(target_path):
        logger.error("Workspace creation failed.")
        return False
    
    logger.info("✅ Workspace automation completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)