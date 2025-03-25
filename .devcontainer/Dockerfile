FROM python:3.11-slim-bullseye

ARG DEV_MODE=true
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000

# Create a non-root user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # Add sudo support
    && apt-get update \
    && apt-get install -y --no-install-recommends sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Install minimal dependencies 
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Use single layer for pip installation with build cache
COPY requirements.txt /tmp/requirements.txt

# Use pip cache and optimized compilation with PGO
RUN --mount=type=cache,target=/root/.cache/pip \
    PYTHONOPTIMIZE=2 \
    python3 -m pip install --no-cache-dir --compile --prefer-binary \
    $([ "$DEV_MODE" = "true" ] && cat /tmp/requirements.txt || \
    grep -v "^# Dev requirements\|^pytest\|^black\|^isort\|^flake8\|^bandit" /tmp/requirements.txt)

# Set optimization flags for the runtime environment
ENV PYTHONOPTIMIZE=2

# Quick validation of core dependencies
RUN python -c "import yaml, rich, typer, pydantic; print('Core packages verified')"

USER $USERNAME