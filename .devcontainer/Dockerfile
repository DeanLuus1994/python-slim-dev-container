# syntax=docker/dockerfile:1.4
# BUILDKIT=1

# ----------------- INITIAL BASE PYTHON STAGE -----------------
FROM python:3.13.2-alpine AS python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.1.1 \
    POETRY_NO_INTERACTION=1

# ----------------- BUILDER STAGE FOR POETRY -----------------
FROM python-base AS poetry-builder
WORKDIR /app
RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache gcc musl-dev && \
    pip install --no-cache-dir poetry==${POETRY_VERSION}

# ----------------- DEPENDENCY BUILDER STAGE -----------------
FROM poetry-builder AS deps-builder
WORKDIR /app
COPY pyproject.toml ./

# Install each package separately for better layer caching and cleanup
# Core package: PyYAML
RUN --mount=type=cache,target=/root/.cache \
    poetry config virtualenvs.create false && \
    poetry add pyyaml==6.0.2

# Core package: Rich
RUN --mount=type=cache,target=/root/.cache \
    poetry add rich==13.9.4

# Core package: Typer
RUN --mount=type=cache,target=/root/.cache \
    poetry add typer==0.15.2

# Core package: Pydantic
RUN --mount=type=cache,target=/root/.cache \
    poetry add pydantic==2.10.6

# Additional dependencies (examples, replace with actual dependencies as needed)
RUN --mount=type=cache,target=/root/.cache \
    poetry add findpython==0.6.3

RUN --mount=type=cache,target=/root/.cache \
    poetry add build==1.2.2

# Cleanup after all dependencies are installed
RUN find /usr/local -name '*.pyc' -delete && \
    find /usr/local -name '__pycache__' -delete

# ----------------- LEAN RUNTIME IMAGE -----------------
FROM python-base AS runtime
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000

# Essential runtime optimization flags
ENV PYTHONOPTIMIZE=2 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy only the installed packages from builder
COPY --from=deps-builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages/
COPY --from=deps-builder /usr/local/bin /usr/local/bin/

# Minimal system dependencies with immediate cleanup
RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache \
    sudo \
    git \
    ca-certificates \
    bash \
    && addgroup -g $USER_GID $USERNAME \
    && adduser -D -u $USER_UID -G $USERNAME $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    # Aggressive cleanup
    && find /usr/local -name '*.pyc' -delete \
    && find /usr/local -name '__pycache__' -delete \
    && find /usr/local -name '*.egg-info' -exec rm -rf {} +

# Create SSH key display script with here-doc to avoid extra layer
RUN echo '#!/bin/bash\nif [ ! -f ~/.ssh/id_rsa ]; then\n    mkdir -p ~/.ssh\n    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" -C "devcontainer-ssh-key" >/dev/null 2>&1\nfi\necho -e "SSH: $(cat ~/.ssh/id_rsa.pub 2>/dev/null || echo "No SSH key found")"' > /usr/local/bin/display-ssh-key \
    && chmod +x /usr/local/bin/display-ssh-key \
    && echo "display-ssh-key" >> /home/$USERNAME/.bashrc \
    && chown -R $USERNAME:$USERNAME /home/$USERNAME

# Verify only required packages are installed and nothing else
# Updated the package verification to use importlib.metadata instead of pkg_resources
RUN python -c "import sys; packages=['yaml', 'rich', 'typer', 'pydantic']; missing = [p for p in packages if p not in sys.modules and __import__(p) is None]; exit(1 if missing else 0)" \
    && python -c "from importlib.metadata import distributions; installed = {dist.metadata['Name'].lower() for dist in distributions()}; required = {'pyyaml', 'rich', 'typer', 'pydantic'}; extra = installed - required - {'pip', 'setuptools', 'wheel', 'markupsafe', 'typing-extensions', 'click', 'pygments', 'colorama', 'commonmark'}; print(f'Extra packages: {extra}'); exit(1 if extra else 0)"

# Switch to non-root user
USER $USERNAME
WORKDIR /workspaces