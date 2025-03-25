# ===== Build Stage =====
FROM python:3.11.8-slim-bullseye AS builder

# Set build-time optimization flags
ENV PYTHONOPTIMIZE=2
ENV PIP_NO_CACHE_DIR=1

# Copy Poetry configuration
COPY pyproject.toml /tmp/pyproject.toml

# Install poetry and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    python3-dev \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local python3 - \
    && poetry config virtualenvs.create false \
    && cd /tmp \
    && poetry install --only main --no-interaction --no-ansi \
    && python3 -m pip install --no-cache-dir --compile --prefer-binary pipdeptree

# ===== Final Stage =====
FROM python:3.11.8-slim-bullseye

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000

# Set runtime Python optimization flags
ENV PYTHONOPTIMIZE=2
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/pipdeptree /usr/local/bin/pipdeptree

# Create non-root user and install required dependencies in a single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    git \
    openssh-server \
    ca-certificates \
    && groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && mkdir -p /run/sshd \
    && echo "PrintMotd yes" >> /etc/ssh/sshd_config \
    && echo "PermitUserEnvironment yes" >> /etc/ssh/sshd_config \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /home/$USERNAME/.ssh

# Create SSH key display script
COPY <<-'EOF' /usr/local/bin/display-ssh-key
#!/bin/bash
if [ ! -f ~/.ssh/id_rsa ]; then
    mkdir -p ~/.ssh
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" -C "devcontainer-ssh-key"
fi
echo -e "\n\033[1;36m======= SSH PUBLIC KEY FOR REMOTE CONNECTION =======\033[0m"
echo -e "\033[1;33m$(cat ~/.ssh/id_rsa.pub)\033[0m"
echo -e "\033[1;36m====================================================\033[0m\n"
echo -e "Connect using: \033[1;32mssh -p 2222 vscode@localhost\033[0m"
EOF

RUN chmod +x /usr/local/bin/display-ssh-key \
    && echo "display-ssh-key" >> /home/$USERNAME/.bashrc \
    && echo "display-ssh-key" >> /home/$USERNAME/.zshrc \
    && chown -R $USERNAME:$USERNAME /home/$USERNAME

# Quick validation of core dependencies
RUN python -c "import yaml, rich, typer, pydantic; print('Core packages verified')"

USER $USERNAME