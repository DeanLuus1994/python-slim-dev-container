# syntax=docker/dockerfile:1.4

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG DEV_MODE=true
ARG USE_ROOT_USER=false

# Install minimal dev tools with no recommended extras
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends git procps sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user with sudo access
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set up pip cache for both root and non-root user
ENV PIP_CACHE_DIR=/tmp/.pip-cache
RUN mkdir -p $PIP_CACHE_DIR && chmod 777 $PIP_CACHE_DIR

# Copy requirements files
COPY requirements.txt /tmp/requirements.txt
# Amended: Copy pyproject.toml from the root folder (one level up)
COPY ../pyproject.toml /tmp/pyproject.toml

# Install Python packages based on DEV_MODE
RUN --mount=type=cache,target=/tmp/.pip-cache \
    if [ "$DEV_MODE" = "true" ]; then \
    echo "Installing development dependencies..." && \
    pip3 --disable-pip-version-check install --prefer-binary -r /tmp/requirements.txt; \
    else \
    echo "Installing production dependencies only..." && \
    grep -v "^# Dev requirements" /tmp/requirements.txt | grep -v "^pytest\|^black\|^isort\|^flake8\|^bandit" > /tmp/prod-requirements.txt && \
    pip3 --disable-pip-version-check install --prefer-binary -r /tmp/prod-requirements.txt; \
    fi && \
    pip3 cache purge

# Final validation to ensure core packages work correctly
RUN python -c "import yaml, rich, typer, pydantic; print('Core packages verified')"

# Add validation for dev packages when in dev mode
RUN if [ "$DEV_MODE" = "true" ]; then \
    python -c "import pytest, black, isort, flake8, bandit, pipdeptree; print('Dev packages verified')"; \
    fi

# Set the default user conditionally based on USE_ROOT_USER flag
USER ${USE_ROOT_USER:+root} ${USE_ROOT_USER:-$USERNAME}