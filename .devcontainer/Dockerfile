# syntax=docker/dockerfile:1.4

# ARG for Python version ensures it must be specified
ARG PYTHON_VERSION

# Base Python image with optimization flags
FROM python:${PYTHON_VERSION}-alpine AS python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PYTHONOPTIMIZE=2

# Install poetry
FROM python-base AS poetry-builder
ARG POETRY_VERSION=1.7.1
RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

# Build dependencies
FROM poetry-builder AS deps-builder
WORKDIR /app
COPY pyproject.toml ./

# Generate proper lock file and install dependencies
RUN --mount=type=cache,target=/root/.cache \
    poetry config virtualenvs.create false && \
    poetry lock --no-update && \
    poetry install $(test "$DEV_MODE" != "true" && echo "--only main") && \
    find /usr/local -name '*.pyc' -delete && \
    find /usr/local -name '__pycache__' -delete

# Runtime image
FROM python-base AS runtime
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000

# Copy only the installed packages
COPY --from=deps-builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages/
COPY --from=deps-builder /usr/local/bin /usr/local/bin/

# Create non-root user with sudo
RUN apk add --no-cache sudo git bash && \
    addgroup -g $USER_GID $USERNAME && \
    adduser -D -u $USER_UID -G $USERNAME $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# Configure SSH for development
RUN echo '#!/bin/bash\nif [ ! -f ~/.ssh/id_rsa ]; then\n    mkdir -p ~/.ssh\n    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" -C "devcontainer-ssh-key" >/dev/null 2>&1\nfi\necho -e "SSH: $(cat ~/.ssh/id_rsa.pub 2>/dev/null || echo "No SSH key found")"' > /usr/local/bin/display-ssh-key \
    && chmod +x /usr/local/bin/display-ssh-key \
    && echo "display-ssh-key" >> /home/$USERNAME/.bashrc \
    && chown -R $USERNAME:$USERNAME /home/$USERNAME

COPY . /workspaces/python-slim-dev-container
WORKDIR /workspaces/python-slim-dev-container
USER $USERNAME