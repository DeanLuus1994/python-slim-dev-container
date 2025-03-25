# Python Slim Dev Container

<!-- 
<p align="center">
    <picture>
        <source type="image/avif" srcset="./assets/banner.avif">
        <source type="image/webp" srcset="./assets/banner.webp">
        <img src="./assets/banner.png" alt="Python Slim Dev Container" style="width: 90%;" />
    </picture>
</p>
-->

With a decade of experience in IT I knew nothing at all about Python or AI 2 years ago. Diving head first into the depths with deep understanding of programming logic, best practices and principles, I got lost in a whole new ever-changing and fast-paced evolving world.

This highly minimal implementation of the most current best practices aims to add some color to those grey areas for anybody that feels they're in the same situation that I was in.

Feel free to contribute, just note that the coding governance and standards are extremely strictly aligned with the most current PEP guidelines and DRY modular architecture.

This is done so that at least I can follow the spaghetti packages and code implementations that needed to be ironed out.

**The only dependencies you need installed are:**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Visual Studio Code](https://code.visualstudio.com/)

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Configuration Philosophy](#configuration-philosophy)
- [Project Structure](#project-structure)
- [Container Components](#container-components)
- [Python Environment](#python-environment)
- [Code Quality & Standards](#code-quality--standards)
- [Security Features](#security-features)
- [CI/CD Integration](#cicd-integration)
- [Getting Started](#getting-started)
- [Configuration Files Explained](#configuration-files-explained)

## Architecture Overview

This development container uses a microservices architecture with two primary services:

1. **Python Application Container**: A slim Python environment with development tools
2. **PostgreSQL Database**: Persistent data storage with proper volume mapping

The architecture emphasizes:
- **Performance**: Minimal footprint with binary-only packages and slim images
- **Reproducibility**: Precisely pinned dependencies and explicit configurations
- **Security**: Non-root user by default with toggle option
- **Standards**: PEP-compliant tools with centralized configuration

## Configuration Philosophy

The project follows a "centralized configuration with practical exceptions" approach:

- **Central Configuration Hub**: `pyproject.toml` serves as the primary configuration source
- **Domain-Specific Configurations**: Certain tools require their own files due to technical limitations
- **Environment Segregation**: Clear separation between development and production environments
- **Feature Toggles**: Boolean flags for controlling major features (e.g., root access, dev mode)

## Project Structure

The repository is organized into a hierarchical structure that separates concerns:

### Root Directory
Contains project-wide configuration and documentation files:
- [`pyproject.toml`](pyproject.toml) - Central configuration for Python tools
- [`.flake8`](.flake8) - Flake8 linting configuration
- [`.pre-commit-config.yaml`](.pre-commit-config.yaml) - Git hooks automation
- [`README.md`](README.md) - Project documentation (this file)

### [`.devcontainer/`](.devcontainer)
Contains all container configuration files to define the development environment:
- [`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json) - VS Code dev container settings
- [`.devcontainer/Dockerfile`](.devcontainer/Dockerfile) - Container image definition
- [`.devcontainer/docker-compose.yml`](.devcontainer/docker-compose.yml) - Multi-container orchestration
- [`.devcontainer/.env`](.devcontainer/.env) - Environment variables and configuration
- [`.devcontainer/requirements.txt`](.devcontainer/requirements.txt) - Python dependencies

#### [`.devcontainer/common/`](.devcontainer/common)
Contains shared scripts and utilities for container setup:
- [`.devcontainer/common/install-zsh-plugins.sh`](.devcontainer/common/install-zsh-plugins.sh) - Shell environment setup

### [`.github/`](.github)
Contains GitHub-specific configuration files:
- [`.github/dependabot.yml`](.github/dependabot.yml) - Automated dependency updates

#### [`.github/workflows/`](.github/workflows)
Contains CI/CD workflow definitions:
- [`.github/workflows/code-quality.yml`](.github/workflows/code-quality.yml) - Linting and standards enforcement
- [`.github/workflows/python-tests.yml`](.github/workflows/python-tests.yml) - Automated testing

## Container Components

### Dockerfile ([`.devcontainer/Dockerfile`](.devcontainer/Dockerfile))

The Dockerfile implements:
- Python 3.11 slim image for minimal footprint
- Non-root user creation with sudo capabilities
- BuildKit caching for efficient builds
- Conditional dependency installation based on DEV_MODE
- Mode switching between root/non-root with USE_ROOT_USER flag

### Docker Compose ([`.devcontainer/docker-compose.yml`](.devcontainer/docker-compose.yml))

The Docker Compose file defines:
- Service networking between app and database
- Volume persistence for PostgreSQL data
- Port forwarding for multiple services
- Environment variable injection from .env
- Secure credential handling
- Health checking for database

### Environment Variables ([`.devcontainer/.env`](.devcontainer/.env))

The .env file organizes settings in logical sections:
- Resource allocation (CPU, memory)
- Container configuration (feature toggles)
- User settings
- Database credentials

### Shell Configuration ([`.devcontainer/common/install-zsh-plugins.sh`](.devcontainer/common/install-zsh-plugins.sh))

This script enhances the developer experience by:
- Installing Oh My Zsh for improved shell functionality
- Setting up autosuggestions for faster command-line work
- Configuring plugins for Git and Docker integration
- Creating a consistent terminal environment

## Python Environment

### Package Management ([`.devcontainer/requirements.txt`](.devcontainer/requirements.txt))

Dependencies are managed with:
- Pinned versions for reproducibility
- Binary-only package installation for performance
- Conditional installation of dev dependencies
- Dependency visualization tools (pipdeptree)

### VS Code Integration ([`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json))

The VS Code configuration includes:
- Categorized extensions by purpose (core, documentation, etc.)
- Pre-configured editor settings aligned with code standards
- Docker-in-Docker support
- GPU passthrough capability
- User selection based on environment variables

## Code Quality & Standards

### Centralized Tool Configuration ([`pyproject.toml`](pyproject.toml))

The pyproject.toml centralizes:
- Black configuration for code formatting
- isort for import sorting
- mypy for type checking
- pylint for Microsoft-aligned code quality and spell checking
- pytest for test configuration
- bandit for security scanning

### Pre-commit Hooks ([`.pre-commit-config.yaml`](.pre-commit-config.yaml))

Pre-commit ensures:
- Code is formatted properly before commits
- Imports are sorted consistently
- Type checking is performed
- Security scanning is run
- Style guides are enforced

### Flake8 Configuration ([`.flake8`](.flake8))

The Flake8 configuration:
- Enforces PEP 8 style guidelines
- Aligns with Black's formatting decisions
- Implements Google docstring conventions
- Customizes rules per file type

## Security Features

Key security implementations:

1. **Non-root User**: Default operation as non-root with optional toggle
2. **Credential Management**: Environment variables from .env with validation
3. **Security Scanning**: Bandit integration in pre-commit and CI/CD
4. **Input Validation**: Type checking with mypy
5. **Updated Dependencies**: Dependabot configuration for security updates

## CI/CD Integration

### GitHub Workflows ([`.github/workflows/`](.github/workflows))

Two primary workflows:

1. **Code Quality** ([`.github/workflows/code-quality.yml`](.github/workflows/code-quality.yml)):
   - Runs linters, formatters, and security scanners
   - Ensures code meets project standards
   - Fails CI on critical issues

2. **Python Tests** ([`.github/workflows/python-tests.yml`](.github/workflows/python-tests.yml)):
   - Runs pytest suite
   - Generates coverage reports
   - Uploads results to Codecov

### Dependabot Configuration ([`.github/dependabot.yml`](.github/dependabot.yml))

- Separate update policies for core vs. dev dependencies
- Conservative updates for production dependencies
- More frequent updates for development tools
- Security updates prioritized

## Getting Started

1. Ensure Docker and VS Code with Remote Containers extension are installed
2. Clone this repository
3. Open the folder in VS Code
4. When prompted, click "Reopen in Container"
5. The environment will build automatically
6. Start developing with all tools pre-configured!

## Configuration Files Explained

| File | Purpose | Implementation Details |
|------|---------|------------------------|
| [`pyproject.toml`](pyproject.toml) | Central configuration hub | Configures Black, isort, mypy, pylint, pytest, bandit |
| [`.flake8`](.flake8) | Flake8 configuration | References values from pyproject.toml for consistency |
| [`.pre-commit-config.yaml`](.pre-commit-config.yaml) | Git hook automation | Ensures code quality before commits |
| [`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json) | VS Code integration | Configures editor and extensions |
| [`.devcontainer/Dockerfile`](.devcontainer/Dockerfile) | Container definition | Builds Python environment with tools |
| [`.devcontainer/docker-compose.yml`](.devcontainer/docker-compose.yml) | Service orchestration | Defines app and database services |
| [`.devcontainer/.env`](.devcontainer/.env) | Environment variables | Configures container behavior and resources |
| [`.devcontainer/requirements.txt`](.devcontainer/requirements.txt) | Python dependencies | Lists exact package versions |
| [`.devcontainer/common/install-zsh-plugins.sh`](.devcontainer/common/install-zsh-plugins.sh) | Shell setup | Configures ZSH for better developer experience |
| [`.github/workflows/code-quality.yml`](.github/workflows/code-quality.yml) | Code quality workflow | Automates linting and security checks |
| [`.github/workflows/python-tests.yml`](.github/workflows/python-tests.yml) | Testing workflow | Automates test execution and coverage |
| [`.github/dependabot.yml`](.github/dependabot.yml) | Dependency updates | Manages security and version updates |

Each file plays a specific role in creating a cohesive, standards-compliant, and secure development environment while minimizing duplication and maintenance overhead.