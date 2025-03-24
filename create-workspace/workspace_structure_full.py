#!/usr/bin/env python3
"""
Defines the directory and file structure for the autonomous Hugging Face agent workspace.
This module is imported by create_workspace.py to separate structure definition from implementation.
"""

# The complete directory structure definition for the workspace
WORKSPACE_STRUCTURE_FULL = {
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

# Example of how to use this structure in create_workspace.py:
"""
from workspace_structure import WORKSPACE_STRUCTURE

def create_workspace(base_path):
    # ...
    # Use imported structure instead of defining it inline
    structure = WORKSPACE_STRUCTURE
    # ...
"""

if __name__ == "__main__":
    print("This module defines the workspace structure and should be imported, not run directly.")
    print(f"Total top-level directories: {len([k for k in WORKSPACE_STRUCTURE_FULL.keys() if not k.startswith('.')])}")
    print(f"Total configuration files: {len([k for k in WORKSPACE_STRUCTURE_FULL.keys() if k.startswith('.')])}")