#!/usr/bin/env python3
# filepath: create_workspace.py

# region Imports
import os
import json
import shutil
import sys
from pathlib import Path
# endregion

# region Helper Functions
def create_file(path, content="# Placeholder\n"):
    """Create a file with the given content."""
    with open(path, 'w') as f:
        f.write(content)

def create_init_file(path):
    """Create an __init__.py file."""
    with open(path / "__init__.py", 'w') as f:
        f.write('"""Module initialization."""\n')
# endregion

# region Main Workspace Creation Function
def create_workspace(base_path):
    """Create the full directory structure for the autonomous Hugging Face agent."""
    base_path = Path(base_path)
    
    # Create the base directory
    os.makedirs(base_path, exist_ok=True)
    
    # region Directory Structure Definition
    structure = {
        ".devcontainer": {
            "container": ["config.yaml", "dev.dockerignore", "docker-compose.dev.yaml", "Dockerfile.dev"],
            "init": {
                "core": {
                    "config": ["__init__.py", "env.py", "loader.py"],
                    "system": ["__init__.py", "commands.py", "cpu.py", "memory.py", "paths.py"],
                    "tests": ["__init__.py", "conftest.py", "test_env.py"],
                    "utils": ["__init__.py", "helpers.py", "validation.py"],
                    "__init__.py": None,
                    "__about__.py": None,
                    "__main__.py": None,
                    "constants.py": None,
                    "exceptions.py": None,
                    "py.typed": None
                },
                "functions": {
                    "concurrency": ["__init__.py", "executor.py"],
                    "optimization": ["__init__.py", "binary.py", "compiler.py"],
                    "resource": ["__init__.py", "detection.py", "gpu.py"],
                    "tests": ["__init__.py", "conftest.py", "test_executor.py", "test_resource.py"],
                    "ui": ["__init__.py", "prompt.py"],
                    "vcs": ["__init__.py", "git.py", "repository.py"],
                    "__init__.py": None,
                    "__about__.py": None,
                    "__main__.py": None,
                    "constants.py": None,
                    "exceptions.py": None,
                    "py.typed": None
                },
                "log": ["__init__.py", "formatter.py", "logger.py"],
                "orchestration": ["__init__.py", "enable_debugging.py", "github_provisioner.py", "python_optimizer.py", "repository_manager.py"],
                "__init__.py": None,
                "bytecode_optimizer.py": None,
                "example.env": None,
                "optimize.py": None
            },
            "devcontainer.json": None
        },
        "accelerators": {
            "__init__.py": None,
            "cuda": {
                "__init__.py": None,
                "profilers": {
                    "__init__.py": None,
                    "memory_tracker.py": None,
                    "operation_profiler.py": None
                },
                "optimizers": {
                    "__init__.py": None,
                    "kernel_fusion.py": None,
                    "memory_planning.py": None
                },
                "rtx": {
                    "__init__.py": None,
                    "models": {
                        "__init__.py": None,
                        "rtx_2000.py": None,
                        "rtx_3000.py": None,
                        "rtx_4000.py": None
                    },
                    "tensor_cores.py": None,
                    "utils": {
                        "__init__.py": None,
                        "shared_memory.py": None
                    }
                }
            },
            "tpu": {
                "__init__.py": None,
                "optimizers.py": None
            },
            "cpu": {
                "__init__.py": None,
                "avx_optimizations.py": None,
                "threading.py": None
            }
        },
        "api": {
            "__init__.py": None,
            "v1": {
                "__init__.py": None,
                "endpoints": {
                    "__init__.py": None,
                    "huggingface_agent.py": None
                },
                "models": {
                    "__init__.py": None,
                    "request_models.py": None
                },
                "middleware": {
                    "__init__.py": None,
                    "auth.py": None
                }
            },
            "clients": {
                "__init__.py": None,
                "python": {
                    "__init__.py": None,
                    "client.py": None
                },
                "js": {
                    "package.json": None,
                    "index.js": None
                }
            },
            "docs": {
                "__init__.py": None,
                "openapi.json": None,
                "generator.py": None
            },
            "versioning": {
                "__init__.py": None,
                "strategy.py": None
            }
        },
        "ai_integration": {
            "__init__.py": None,
            "copilot": {
                "config": ["copilot_config.yaml"],
                "indexing": ["__init__.py", "indexer.py", "vectorizer.py"],
                "preload": ["__init__.py", "loader.py"]
            },
            "vector_store": ["__init__.py", "index_config.yaml", "model_info.json", "retriever.py"],
            "model_registry": ["__init__.py", "versioning.py", "metadata.py"],
            "embeddings": ["__init__.py", "engine.py"],
            "safetensors": {
                "__init__.py": None,
                "converters": {
                    "__init__.py": None,
                    "from_pytorch.py": None,
                    "to_pytorch.py": None
                },
                "handlers": {
                    "__init__.py": None,
                    "memory_mapped.py": None,
                    "streaming.py": None
                },
                "quantization": {
                    "__init__.py": None,
                    "int8.py": None,
                    "mixed_precision.py": None
                },
                "security": {
                    "__init__.py": None,
                    "validators.py": None
                }
            }
        },
        "caching": {
            "__init__.py": None,
            "binary": {
                "__init__.py": None,
                "container": {
                    "__init__.py": None,
                    "docker_volume.py": None
                },
                "local": {
                    "__init__.py": None,
                    "disk_cache.py": None,
                    "memory_cache.py": None
                },
                "policies": {
                    "__init__.py": None,
                    "eviction.py": None,
                    "prefetching.py": None
                }
            },
            "computation": {
                "__init__.py": None,
                "checkpointing.py": None,
                "memoization.py": None
            },
            "models": {
                "__init__.py": None,
                "weights_cache.py": None,
                "inference_cache.py": None
            },
            "distributed": {
                "__init__.py": None,
                "coordination.py": None,
                "replication.py": None
            }
        },
        "precompilation": {
            "__init__.py": None,
            "aot": {
                "__init__.py": None,
                "graph_capture.py": None,
                "tracing.py": None
            },
            "bytecode": {
                "__init__.py": None,
                "optimizer.py": None,
                "rewriter.py": None
            },
            "kernels": {
                "__init__.py": None,
                "fusion.py": None,
                "specialization.py": None
            },
            "container": {
                "__init__.py": None,
                "layers.py": None,
                "caching.py": None
            },
            "pipeline": {
                "__init__.py": None,
                "stages.py": None,
                "executor.py": None
            }
        },
        "cloud": {
            "aws": {
                "cloudformation": ["agent_stack.yaml", "network_stack.yaml"],
                "scripts": ["deploy.py", "teardown.py"]
            },
            "azure": {
                "arm_templates": ["deployment.json"],
                "scripts": ["provision.py"]
            },
            "gcp": {
                "terraform": ["main.tf", "variables.tf"],
                "scripts": ["deploy.sh"]
            },
            "kubernetes": {
                "base": ["deployment.yaml", "service.yaml", "kustomization.yaml"],
                "overlays": {
                    "dev": ["kustomization.yaml"],
                    "prod": ["kustomization.yaml"]
                }
            },
            "__init__.py": None
        },
        "config": {
            "__init__.py": None,
            "default.yaml": None,
            "environments": {
                "__init__.py": None,
                "development.yaml": None,
                "testing.yaml": None,
                "production.yaml": None
            },
            "feature_flags": {
                "__init__.py": None,
                "flags.yaml": None,
                "manager.py": None
            },
            "schema": {
                "__init__.py": None,
                "validation.py": None
            }
        },
        "distribution": {
            "__init__.py": None,
            "packaging": {
                "__init__.py": None,
                "build.py": None,
                "release.py": None
            },
            "versioning": {
                "__init__.py": None,
                "compatibility.py": None,
                "migrations": {
                    "__init__.py": None,
                    "scripts": {
                        "__init__.py": None,
                        "v1_to_v2.py": None
                    }
                },
                "semver.py": None
            }
        },
        "docs": {
            "api": {
                "index.md": None,
                "reference": {
                    "endpoints.md": None
                }
            },
            "architecture": {
                "diagrams": {
                    "component_model.png": None,
                    "sequence_diagrams": {
                        "agent_flow.png": None
                    }
                },
                "index.md": None
            },
            "examples": {
                "notebooks": {
                    "quickstart.ipynb": None
                },
                "tutorials": {
                    "first_agent.md": None
                }
            },
            "usage": {
                "getting_started.md": None,
                "advanced": {
                    "customization.md": None
                }
            },
            "metrics": {
                "__init__.py": None,
                "doc_usage_tracker.py": None
            },
            "conf.py": None,
            "index.md": None
        },
        "governance": {
            "CHANGELOG.md": None,
            "CODE_OF_CONDUCT.md": None,
            "CONTRIBUTING.md": None,
            "GOVERNANCE.md": None,
            "LICENSE": None,
            "SECURITY.md": None,
            "templates": {
                "issue_template.md": None,
                "pull_request_template.md": None
            }
        },
        "hooks": {
            "__init__.py": None,
            "git_hooks.py": None,
            "registry.py": None,
            "plugins": {
                "__init__.py": None,
                "security_scan.py": None
            }
        },
        "infrastructure": {
            "docker": {
                "prod": {
                    "Dockerfile": None,
                    "docker-compose.yaml": None
                },
                "multi-stage": {
                    "Dockerfile": None
                }
            },
            "ci_cd": {
                "jenkins": {
                    "Jenkinsfile": None
                },
                "scripts": {
                    "build.py": None,
                    "deploy.py": None
                }
            },
            "__init__.py": None
        },
        "observability": {
            "metrics": {
                "__init__.py": None,
                "collectors": {
                    "__init__.py": None,
                    "performance.py": None
                },
                "exporters": {
                    "__init__.py": None,
                    "prometheus.py": None
                }
            },
            "logging": {
                "__init__.py": None,
                "formatters": {
                    "__init__.py": None,
                    "json_formatter.py": None
                },
                "handlers": {
                    "__init__.py": None,
                    "cloud_handler.py": None
                }
            },
            "tracing": {
                "__init__.py": None,
                "middleware.py": None,
                "exporters": {
                    "__init__.py": None,
                    "jaeger.py": None
                }
            },
            "dashboards": {
                "grafana": {
                    "agent_dashboard.json": None
                },
                "datadog": {
                    "metrics.json": None
                }
            },
            "alerting": {
                "__init__.py": None,
                "rules.yaml": None,
                "channels.py": None
            },
            "__init__.py": None
        },
        "performance": {
            "__init__.py": None,
            "benchmarks": {
                "__init__.py": None,
                "core_benchmarks.py": None,
                "scenarios": {
                    "__init__.py": None,
                    "high_load.py": None
                }
            },
            "distributed": {
                "__init__.py": None,
                "worker.py": None,
                "scaling": {
                    "__init__.py": None,
                    "auto_scaler.py": None
                }
            },
            "profiling": {
                "__init__.py": None,
                "memory_profiler.py": None,
                "reports": {
                    "__init__.py": None,
                    "analyzer.py": None
                }
            }
        },
        "platform": {
            "__init__.py": None,
            "adapters": {
                "__init__.py": None,
                "linux.py": None,
                "macos.py": None,
                "windows.py": None
            },
            "detector.py": None
        },
        "plugins": {
            "__init__.py": None,
            "core": {
                "__init__.py": None,
                "registry.py": None
            },
            "interfaces": {
                "__init__.py": None,
                "plugin_base.py": None
            },
            "samples": {
                "__init__.py": None,
                "example_plugin.py": None
            }
        },
        "security": {
            "__init__.py": None,
            "analysis": {
                "__init__.py": None,
                "code_scanner.py": None
            },
            "compliance": {
                "__init__.py": None,
                "verifier.py": None,
                "standards": {
                    "__init__.py": None,
                    "gdpr.py": None,
                    "hipaa.py": None
                }
            },
            "dependency_check": {
                "__init__.py": None,
                "vulnerability_scanner.py": None
            },
            "secrets": {
                "__init__.py": None,
                "manager.py": None,
                "vault_integration.py": None
            }
        },
        "static_analysis": {
            "__init__.py": None,
            "linters": {
                "__init__.py": None,
                "config": {
                    ".pylintrc": None,
                    ".flake8": None,
                    "mypy.ini": None
                }
            },
            "reports": {
                "__init__.py": None,
                "generator.py": None
            }
        },
        "edge": {
            "__init__.py": None,
            "deployment": {
                "__init__.py": None,
                "embedded": {
                    "__init__.py": None,
                    "flash_optimizations.py": None
                },
                "containerized": {
                    "__init__.py": None,
                    "minimal_runtime.py": None
                }
            },
            "networking": {
                "__init__.py": None,
                "protocols": {
                    "__init__.py": None,
                    "mqtt.py": None
                },
                "offline": {
                    "__init__.py": None,
                    "sync.py": None
                }
            },
            "optimization": {
                "__init__.py": None,
                "quantization.py": None,
                "pruning.py": None
            }
        },
        "i18n": {
            "__init__.py": None,
            "locales": {
                "__init__.py": None,
                "en": {
                    "__init__.py": None,
                    "messages.json": None
                },
                "registry.py": None
            },
            "translation": {
                "__init__.py": None,
                "engine.py": None,
                "markers.py": None
            },
            "middleware": {
                "__init__.py": None,
                "locale_detector.py": None
            }
        },
        "integration": {
            "__init__.py": None,
            "adapters": {
                "__init__.py": None,
                "rest": {
                    "__init__.py": None,
                    "client.py": None
                },
                "graphql": {
                    "__init__.py": None,
                    "client.py": None
                },
                "streaming": {
                    "__init__.py": None,
                    "kafka.py": None
                }
            },
            "connectors": {
                "__init__.py": None,
                "database": {
                    "__init__.py": None,
                    "orm.py": None
                },
                "services": {
                    "__init__.py": None,
                    "aws.py": None
                }
            },
            "patterns": {
                "__init__.py": None,
                "circuit_breaker.py": None,
                "retry.py": None
            }
        },
        "dependencies": {
            "__init__.py": None,
            "management": {
                "__init__.py": None,
                "resolver.py": None,
                "updater.py": None
            },
            "security": {
                "__init__.py": None,
                "audit.py": None
            },
            "compatibility": {
                "__init__.py": None,
                "version_matrix.py": None
            }
        },
        ".github": {
            "workflows": {
                "ci.yml": None,
                "cd.yml": None,
                "dependency_check.yml": None,
                "cross_platform_test.yml": None,
                "docs_builder.yml": None,
                "static_analysis.yml": None,
                "dependency_updater.yml": None,
                "rtx_performance_tests.yml": None
            },
            "dependabot.yml": None,
            "CODEOWNERS": None
        },
        ".vscode": {
            "extensions.json": None,
            "launch.json": None,
            "settings.json": None
        },
        ".env": None,
        ".gitattributes": None,
        ".gitignore": None,
        "CHANGELOG.md": None,
        "pyproject.toml": None,
        "README.md": None,
        "setup.py": None,
        "Makefile": None
    }
    # endregion

    # region File Content Templates
    readme_content = """# Autonomous Hugging Face Agent

A comprehensive, future-proofed framework for building autonomous agents with Hugging Face integration.

## Features

- Robust modular architecture
- SafeTensor integration for secure model handling
- Advanced binary/bytes caching for performance
- Precompilation optimizations for RTX consumer cards
- Full cloud, edge, and container deployment support
- Comprehensive monitoring and observability
- Strong security and compliance frameworks

## Getting Started

See `docs/usage/getting_started.md` for initial setup instructions.

## Architecture

This project follows a highly modular, future-proofed architecture designed for extensibility and performance.
Key components include:

- AI Integration modules
- Performance optimization and caching
- Cloud deployment configurations
- Security and compliance frameworks

## License

See the LICENSE file for details.
"""

    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/

# IDE
.idea/
.vscode/*
!.vscode/extensions.json
!.vscode/settings.json
!.vscode/launch.json
*.swp
*.swo

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
.env
.cache/
logs/
"""

    pyproject_content = """[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 88
target-version = ["py38", "py39", "py310"]
include = '\\.pyi?$'

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true

[tool.pytest.ini_options]
minversion = "6.0"
testpaths = ["tests"]
python_files = "test_*.py"
"""

    setup_content = """import os
from setuptools import setup, find_packages

# Read the contents of README.md
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="autonomous_huggingface_agent",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
        "rich>=10.0.0",
        "typer>=0.4.0",
        "pydantic>=1.9.0",
        "transformers>=4.18.0",
        "safetensors>=0.2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=22.3.0",
            "isort>=5.10.1",
            "mypy>=0.950",
            "flake8>=4.0.1",
        ],
        "docs": [
            "sphinx>=4.4.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.17.0",
        ],
    },
    description="A comprehensive, future-proofed framework for building autonomous agents with Hugging Face integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Organization",
    author_email="contact@example.com",
    url="https://github.com/yourusername/autonomous_huggingface_agent",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
"""
    
    makefile_content = """# Makefile for Autonomous Hugging Face Agent

.PHONY: setup develop clean lint test docs build

# Environment setup
setup:
\tpython -m pip install --upgrade pip
\tpython -m pip install -e ".[dev,docs]"
\tpre-commit install

develop:
\tpython -m pip install -e ".[dev]"

# Cleaning
clean:
\trm -rf build/
\trm -rf dist/
\trm -rf *.egg-info
\tfind . -type d -name __pycache__ -exec rm -rf {} +
\tfind . -type f -name "*.pyc" -delete

# Code quality
lint:
\tflake8 .
\tblack --check .
\tisort --check .
\tmypy .

# Testing
test:
\tpytest

# Documentation
docs:
\tsphinx-build -b html docs/source docs/build

# Build
build:
\tpython -m build
"""

    devcontainer_json_content = """{
  "name": "Autonomous Hugging Face Agent Dev",
  "dockerComposeFile": "container/docker-compose.dev.yaml",
  "service": "app",
  "workspaceFolder": "/workspace",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-azuretools.vscode-docker",
        "github.copilot",
        "github.copilot-chat",
        "ryanluker.vscode-coverage-gutters",
        "matangover.mypy"
      ],
      "settings": {
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
        "python.linting.flake8Enabled": true,
        "python.formatting.provider": "black",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
          "source.organizeImports": true
        }
      }
    }
  },
  "postCreateCommand": "pip install -e '.[dev,docs]'",
  "remoteUser": "vscode"
}
"""

    dockerfile_content = """FROM python:3.10-slim-bullseye

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create non-root user and set up environment
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo git build-essential curl \
    && echo $USERNAME ALL=\\(root\\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install dependencies for development
RUN apt-get update && apt-get install -y \\
    curl \\
    git \\
    wget \\
    build-essential \\
    libffi-dev \\
    pkg-config \\
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Optional: Install CUDA drivers for GPU support
# Uncomment the following sections if GPU support is needed
# RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb && \\
#     dpkg -i cuda-keyring_1.0-1_all.deb && \\
#     apt-get update && \\
#     apt-get install -y cuda-toolkit-11-8 && \\
#     apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
ENV PYTHONPATH=/workspace
ENV PATH=$PATH:/home/$USERNAME/.local/bin

# Switch to non-root user
USER $USERNAME

# Ensure pip is up to date
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install pre-commit
RUN pip install --no-cache-dir pre-commit
"""

    docker_compose_content = """version: '3.8'

services:
  app:
    build: 
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - ../..:/workspace:cached
    command: sleep infinity
    environment:
      - PYTHONPATH=/workspace
      # Uncomment the following line to enable GPU support
      # - NVIDIA_VISIBLE_DEVICES=all
    # Uncomment the following section to enable GPU support
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: 1
    #           capabilities: [gpu]
"""

    vscode_settings_content = """{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.nosetestsEnabled": false,
  "python.testing.pytestArgs": [
    "tests"
  ],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "python.analysis.typeCheckingMode": "basic",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
"""

    vscode_extensions_content = """{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.black-formatter",
    "ms-azuretools.vscode-docker",
    "github.copilot",
    "github.copilot-chat",
    "ryanluker.vscode-coverage-gutters",
    "matangover.mypy"
  ]
}
"""

    vscode_launch_content = """{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": false
    },
    {
      "name": "Python: Module",
      "type": "python",
      "request": "launch",
      "module": "autonomous_huggingface_agent",
      "justMyCode": false
    }
  ]
}
"""

    gitattributes_content = """# Auto detect text files and perform LF normalization
* text=auto eol=lf

# Python files
*.py text diff=python

# Documentation
*.md text
*.rst text
*.txt text

# Jupyter notebooks
*.ipynb text

# Binary files
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.mov binary
*.mp4 binary
*.mp3 binary
*.zip binary
*.tar binary
*.gz binary
*.whl binary
"""

    github_workflow_ci_content = """name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10"]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install flake8 pytest
        pip install -e ".[dev]"
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    - name: Test with pytest
      run: |
        pytest
"""

    github_codeowners_content = """# Default owners for everything in the repo
* @yourusername

# Specialized ownership
/ai_integration/ @yourusername
/accelerators/ @yourusername
"""

    github_dependabot_content = """version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "automated"
"""
    # endregion

    # region Directory Structure Processing
    def process_structure(current_path, structure_dict):
        for key, value in structure_dict.items():
            path = current_path / key
            
            if isinstance(value, dict):
                # Create directory
                os.makedirs(path, exist_ok=True)
                # Process nested structure
                process_structure(path, value)
            elif isinstance(value, list):
                # Create directory if it doesn't exist
                os.makedirs(path, exist_ok=True)
                # Create files in the list
                for file_name in value:
                    create_file(path / file_name)
            else:
                # It's a file
                if key.endswith('.py'):
                    # Create Python file
                    create_file(path)
                elif key == "__init__.py":
                    # Create init file with specific content
                    create_file(path, '"""Module initialization."""\n')
                elif key == "README.md":
                    create_file(path, readme_content)
                elif key == ".gitignore":
                    create_file(path, gitignore_content)
                elif key == "pyproject.toml":
                    create_file(path, pyproject_content)
                elif key == "setup.py":
                    create_file(path, setup_content)
                elif key == "Makefile":
                    create_file(path, makefile_content)
                elif key == "devcontainer.json":
                    create_file(path, devcontainer_json_content)
                elif key == "Dockerfile.dev":
                    create_file(path, dockerfile_content)
                elif key == "docker-compose.dev.yaml":
                    create_file(path, docker_compose_content)
                elif key == "settings.json":
                    create_file(path, vscode_settings_content)
                elif key == "extensions.json":
                    create_file(path, vscode_extensions_content)
                elif key == "launch.json":
                    create_file(path, vscode_launch_content)
                elif key == ".gitattributes":
                    create_file(path, gitattributes_content)
                elif key == "ci.yml":
                    create_file(path, github_workflow_ci_content)
                elif key == "CODEOWNERS":
                    create_file(path, github_codeowners_content)
                elif key == "dependabot.yml":
                    create_file(path, github_dependabot_content)
                else:
                    # Create other file types
                    create_file(path)
    # endregion

    # Process the structure dictionary
    process_structure(base_path, structure)
    
    # Initialize git repository
    init_git_repository(base_path)
    
    print(f"Workspace created successfully at {base_path}")
    print("Next steps:")
    print("1. cd into your new workspace")
    print("2. Install dependencies: make setup")
    print("3. Start developing!")
# endregion

# region Git Repository Initialization
def init_git_repository(path):
    """Initialize a git repository in the given path."""
    try:
        import subprocess
        subprocess.run(["git", "init"], cwd=path, check=True)
        print(f"Initialized git repository in {path}")
        return True
    except Exception as e:
        print(f"Failed to initialize git repository: {e}")
        return False
# endregion

# region Main Entry Point
if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Default to one directory up when no path is provided
        parent_dir = Path(__file__).absolute().parent.parent
        create_workspace(parent_dir)
    elif len(sys.argv) == 2:
        # Use the provided path
        create_workspace(sys.argv[1])
    else:
        print("Usage: python create_workspace.py [workspace_path]")
        print("If no path is provided, workspace will be created one directory up.")
        sys.exit(1)
# endregion