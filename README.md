# Python Slim Dev Container

<p align="center">
  <a href="https://www.docker.com/"><img src="https://www.docker.com/wp-content/uploads/2022/03/Moby-logo.png" alt="Docker" height="70"></a>
  &nbsp;&nbsp;&nbsp;
  <a href="https://www.microsoft.com/"><img src="https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData/RE1Mu3b?ver=5c31" alt="Microsoft" height="70"></a>
  &nbsp;&nbsp;&nbsp;
  <a href="https://www.python.org/"><img src="https://www.python.org/static/community_logos/python-logo-generic.svg" alt="Python" height="70"></a>
  &nbsp;&nbsp;&nbsp;
  <a href="https://www.anthropic.com/"><img src="https://storage.googleapis.com/website-storage/uploads/2023/02/anthropic-logo-1.png" alt="Anthropic" height="70"></a>
  &nbsp;&nbsp;&nbsp;
  <a href="https://huggingface.co/"><img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg" alt="Hugging Face" height="70"></a>
</p>

<p align="center">
  <a href="https://github.com/features/actions"><img src="https://img.shields.io/github/workflow/status/username/python-slim-dev-container/Python%20CI?label=CI&logo=github&style=flat-square" alt="CI Status"></a>
  <a href="https://www.python.org/downloads/release/python-3118/"><img src="https://img.shields.io/badge/python-3.11.8-blue.svg?style=flat-square&logo=python&logoColor=white" alt="Python Version"></a>
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/docker-powered-blue.svg?style=flat-square&logo=docker&logoColor=white" alt="Docker"></a>
  <a href="https://code.visualstudio.com/docs/devcontainers/containers"><img src="https://img.shields.io/badge/devcontainer-ready-green.svg?style=flat-square&logo=visualstudiocode&logoColor=white" alt="Dev Container"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="Code style: black"></a>
</p>

## Overview

The Python Slim Dev Container provides a **lightweight**, **optimized**, and **production-ready** development environment for Python applications. Designed with performance and maintainability in mind, it follows best practices for containerization, security, and code quality.

<details>
<summary>💫 <b>Personal Journey & Motivation</b> (Click to expand)</summary>

With a decade of experience in IT, I knew nothing at all about Python or AI two years ago. Diving head first into the depths with a deep understanding of programming logic, best practices, and principles, I got lost in a whole new ever-changing and fast-paced evolving world.

This highly minimal implementation of the most current best practices aims to add some color to those grey areas for anybody that feels they're in the same situation that I was in.

Feel free to contribute, just note that the coding governance and standards are extremely strictly aligned with the most current PEP guidelines and DRY modular architecture.

This is done so that at least I can follow the spaghetti packages and code implementations that needed to be ironed out.
</details>

## 🚀 Key Features

- **Multi-stage build** with optimized layers for minimal footprint
- **Poetry dependency management** with clear separation of production/dev dependencies
- **Remote development** through SSH with automatic key display
- **Industry-standard code quality** with pre-commit hooks and CI/CD
- **Database integration** with PostgreSQL and proper volume management
- **Python optimization flags** for maximum performance
- **Security features** including non-root user, minimal exposed ports
- **VS Code integration** with curated extensions and settings

**The only dependencies you need installed are:**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Visual Studio Code](https://code.visualstudio.com/)

## 📊 Performance Matrix

| Component | Optimization | Standards | Security | Maintainability | Overall |
|-----------|--------------|-----------|----------|-----------------|---------|
| **Dockerfile** | 9/10 ⭐ | 9/10 ⭐ | 8/10 ✅ | 9/10 ⭐ | **8.9/10** |
| **docker-compose.yml** | 8/10 ✅ | 9/10 ⭐ | 7/10 ✅ | 10/10 ⭐⭐ | **8.6/10** |
| **devcontainer.json** | 9/10 ⭐ | 10/10 ⭐⭐ | 9/10 ⭐ | 10/10 ⭐⭐ | **9.3/10** |
| **.env** | 10/10 ⭐⭐ | 10/10 ⭐⭐ | 7/10 ✅ | 10/10 ⭐⭐ | **9.3/10** |
| **pyproject.toml** | 9/10 ⭐ | 10/10 ⭐⭐ | 8/10 ✅ | 9/10 ⭐ | **9.2/10** |
| **pre-commit config** | 9/10 ⭐ | 10/10 ⭐⭐ | 10/10 ⭐⭐ | 9/10 ⭐ | **9.4/10** |
| **CI/CD workflow** | 8/10 ✅ | 9/10 ⭐ | 8/10 ✅ | 8/10 ✅ | **8.4/10** |

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Key Technologies](#key-technologies)
- [Project Structure](#project-structure)
- [Container Components](#container-components)
- [Python Environment](#python-environment)
- [Code Quality & Standards](#code-quality--standards)
- [Security Features](#security-features)
- [CI/CD Integration](#cicd-integration)
- [Getting Started](#getting-started)
- [Configuration Files Explained](#configuration-files-explained)
- [HuggingFace Integration](#huggingface-integration)
- [Contributing](#contributing)

## 🏗️ Architecture Overview

This development container uses a microservices architecture with two primary services:

1. **Python Application Container**: A slim Python environment with development tools
2. **PostgreSQL Database**: Persistent data storage with proper volume mapping

<details>
<summary><b>Architecture Diagram</b> (Click to expand)</summary>

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose Network                    │
│                                                             │
│  ┌─────────────────────────┐      ┌─────────────────────┐  │
│  │                         │      │                     │  │
│  │   Python Application    │      │    PostgreSQL DB    │  │
│  │     (VS Code Host)      │◄────►│                     │  │
│  │                         │      │                     │  │
│  └─────────────┬───────────┘      └─────────────────────┘  │
│                │                                           │
│                ▼                                           │
│  ┌─────────────────────────┐                               │
│  │                         │                               │
│  │   VS Code Extensions    │                               │
│  │   & Dev Environment     │                               │
│  │                         │                               │
│  └─────────────────────────┘                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

</details>

The architecture emphasizes:
- **Performance**: Minimal footprint with binary-only packages and slim images
- **Reproducibility**: Precisely pinned dependencies and explicit configurations
- **Security**: Non-root user by default with toggle option
- **Standards**: PEP-compliant tools with centralized configuration

## 🔧 Key Technologies

<table>
  <tr>
    <th>Category</th>
    <th>Technology</th>
    <th>Purpose</th>
  </tr>
  <tr>
    <td rowspan="3">Container</td>
    <td>Docker</td>
    <td>Container runtime and build system</td>
  </tr>
  <tr>
    <td>Docker Compose</td>
    <td>Multi-service orchestration</td>
  </tr>
  <tr>
    <td>VS Code Devcontainers</td>
    <td>Development environment integration</td>
  </tr>
  <tr>
    <td rowspan="4">Python</td>
    <td>Python 3.11.8</td>
    <td>Runtime environment with optimization flags</td>
  </tr>
  <tr>
    <td>Poetry</td>
    <td>Dependency management</td>
  </tr>
  <tr>
    <td>PyYAML, Rich, Typer, Pydantic</td>
    <td>Core libraries for application development</td>
  </tr>
  <tr>
    <td>Black, Ruff, MyPy</td>
    <td>Code quality and type checking</td>
  </tr>
  <tr>
    <td rowspan="2">AI/ML</td>
    <td>Hugging Face</td>
    <td>AI model access and integration</td>
  </tr>
  <tr>
    <td>Anthropic Claude API</td>
    <td>AI assistant integration</td>
  </tr>
  <tr>
    <td rowspan="2">CI/CD</td>
    <td>GitHub Actions</td>
    <td>Automated testing and deployment</td>
  </tr>
  <tr>
    <td>Pre-commit hooks</td>
    <td>Local validation before commits</td>
  </tr>
</table>

## 📂 Project Structure

The repository is organized into a hierarchical structure that separates concerns:

### Root Directory
Contains project-wide configuration and documentation files:
- [`pyproject.toml`](pyproject.toml) - Central configuration for Python tools
- [`.pre-commit-config.yaml`](.pre-commit-config.yaml) - Git hooks automation
- [`README.md`](README.md) - Project documentation (this file)

### [`.devcontainer/`](.devcontainer)
Contains all container configuration files to define the development environment:
- [`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json) - VS Code dev container settings
- [`.devcontainer/Dockerfile`](.devcontainer/Dockerfile) - Container image definition
- [`.devcontainer/docker-compose.yml`](.devcontainer/docker-compose.yml) - Multi-container orchestration
- [`.devcontainer/.env`](.devcontainer/.env) - Environment variables and configuration

### [`.github/`](.github)
Contains GitHub-specific configuration files:
- [`.github/dependabot.yml`](.github/dependabot.yml) - Automated dependency updates
- [`.github/workflows/python-ci.yml`](.github/workflows/python-ci.yml) - CI/CD workflow definition

## 🛠️ Container Components

### Dockerfile ([`.devcontainer/Dockerfile`](.devcontainer/Dockerfile))

```
# Multi-stage build for optimization
FROM python:3.11.8-slim-bullseye AS builder
└── Set optimization flags
└── Install Poetry and dependencies
└── Configure Python environment

FROM python:3.11.8-slim-bullseye
└── Copy Python packages from builder
└── Create non-root user
└── Set up SSH for remote access
└── Configure environment
```

### Docker Compose ([`.devcontainer/docker-compose.yml`](.devcontainer/docker-compose.yml))

Defines two services:
- **app**: Python development environment with VS Code integration
- **db**: PostgreSQL database with volume persistence

### Environment Variables ([`.devcontainer/.env`](.devcontainer/.env))

Contains essential configuration for the development environment:
- Container resource allocation
- Database credentials
- Development mode toggle

## 🐍 Python Environment

### Dependency Management with Poetry

Poetry provides modern Python dependency management with:
- Clear separation between main and development dependencies
- Version pinning for reproducibility
- Lock file generation
- Virtual environment management

Example from `pyproject.toml`:
```toml
[tool.poetry.dependencies]
python = "^3.11"
pyyaml = "6.0"
click = "8.1.3"
rich = "10.16.2"
typer = "0.7.0"
pydantic = "1.10.8"
```

### VS Code Integration (`.devcontainer/devcontainer.json`)

Provides seamless development experience with:
- Preconfigured Python extensions
- Code formatting and linting
- Remote container access
- SSH server for external connections

## ✅ Code Quality & Standards

### Pre-commit Hooks (`.pre-commit-config.yaml`)

Ensures code quality with automated checks:
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    # Basic checks for common issues
  - repo: https://github.com/psf/black
    # Code formatting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    # Fast linting
  - repo: https://github.com/pre-commit/mirrors-mypy
    # Type checking
  - repo: https://github.com/hadolint/hadolint
    # Dockerfile linting
  - repo: https://github.com/gitleaks/gitleaks
    # Secret scanning
```

### Python Tool Configuration (`pyproject.toml`)

Centralizes configuration for multiple tools:
- Black for code formatting
- Ruff for fast linting
- MyPy for type checking
- Pytest for testing

## 🔒 Security Features

1. **Non-root User**: Container runs as `vscode` user by default
2. **SSH Key Management**: Secure key generation for remote access
3. **Limited Port Exposure**: Only essential ports exposed
4. **Secret Detection**: Pre-commit hook to detect secrets in code
5. **Dependency Scanning**: Dependabot for security updates
6. **Type Safety**: MyPy for type checking

## 🔄 CI/CD Integration

### GitHub Workflows (`.github/workflows/python-ci.yml`)

Automated testing and validation:
```yaml
jobs:
  lint:
    # Code quality checks using pre-commit
  test:
    # Run pytest with coverage reporting
```

### Dependabot Configuration (`.github/dependabot.yml`)

Automated dependency updates for:
- GitHub Actions workflows
- Dev container components
- Python dependencies

## 🚀 Getting Started

1. **Prerequisites**:
   - [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - [Visual Studio Code](https://code.visualstudio.com/)
   - [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
   YOU SHOULD BE PROMPTED FOR THIS THOUGH

2. **Clone and Open**:
   ```bash
   git clone https://github.com/yourusername/python-slim-dev-container.git
   cd python-slim-dev-container
   code .
   ```

3. **Start Development**:
   - When prompted, click "Reopen in Container"
   - The container will build and start automatically
   - Your SSH key will be displayed in the terminal for remote connections

## 📝 Configuration Files Explained

<details>
<summary><b>Click to expand file details</b></summary>

| File | Purpose | Implementation Details |
|------|---------|------------------------|
| pyproject.toml | Central configuration hub | Configures Black, Ruff, MyPy, Poetry |
| .pre-commit-config.yaml | Git hook automation | Ensures code quality before commits |
| devcontainer.json | VS Code integration | Configures editor and extensions |
| Dockerfile | Container definition | Multi-stage build with optimizations |
| docker-compose.yml | Service orchestration | Defines app and database services |
| .env | Environment variables | Configures container behavior |
| python-ci.yml | CI/CD workflow | Automates testing and validation |
| dependabot.yml | Dependency updates | Manages security and version updates |

</details>

## 🤗 HuggingFace Integration

Coming soon! The next phase of this project will include:

- HuggingFace model loading and inference
- Optimized container setup for ML workloads
- GPU passthrough configuration
- Model fine-tuning capabilities
- Integration with popular frameworks

SUGGESTIONS WELCOME FOR CROSS COMPATIBILITY LEAN OPTIMIZED SUGGESTIONS THAT ARE PERFORMANT.

Stay tuned for updates as we implement these exciting features!

## 👥 Contributing

Contributions are welcome and appreciated! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch
3. **Commit** your changes with descriptive messages
4. **Push** to your branch
5. Submit a **Pull Request**

Please ensure your code follows our standards by running pre-commit hooks locally:

```bash
pip install pre-commit
pre-commit install
```

---

<p align="center">
  <em>Built with ❤️ using Docker, Python, and VS Code Dev Containers</em>
</p>

<p align="center">
  <a href="https://www.docker.com/">Docker</a> •
  <a href="https://www.microsoft.com/">Microsoft</a> •
  <a href="https://www.python.org/">Python</a> •
  <a href="https://www.anthropic.com/">Anthropic</a> •
  <a href="https://huggingface.co/">HuggingFace</a>
</p>
