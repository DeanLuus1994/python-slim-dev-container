# ===== Build Stage =====
FROM python:3.11.8-slim-bullseye AS builder

# Set all optimization flags in one place
ENV PYTHONOPTIMIZE=2 \
    PIP_NO_CACHE_DIR=1

# Copy Poetry configuration
COPY pyproject.toml /tmp/pyproject.toml

# Install poetry and dependencies in a single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    python3-dev \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local python3 - \
    && poetry config virtualenvs.create false \
    && cd /tmp \
    && poetry install --only main --no-interaction --no-ansi

# ===== Final Stage =====
FROM python:3.11.8-slim-bullseye

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000

# Set runtime Python optimization flags
ENV PYTHONOPTIMIZE=2 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11/
COPY --from=builder /usr/local/bin /usr/local/bin/

# Create non-root user and install required dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    git \
    ca-certificates \
    && groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Create SSH key display script (simplified)
COPY <<-'EOF' /usr/local/bin/display-ssh-key
#!/bin/bash
if [ ! -f ~/.ssh/id_rsa ]; then
    mkdir -p ~/.ssh
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" -C "devcontainer-ssh-key" >/dev/null 2>&1
fi
echo -e "SSH: $(cat ~/.ssh/id_rsa.pub)"
EOF

# Finalize permissions
RUN chmod +x /usr/local/bin/display-ssh-key \
    && echo "display-ssh-key" >> /home/$USERNAME/.bashrc \
    && echo "display-ssh-key" >> /home/$USERNAME/.zshrc \
    && chown -R $USERNAME:$USERNAME /home/$USERNAME \
    && python -c "import yaml, rich, typer, pydantic; print('Core packages verified')"

USER $USERNAME