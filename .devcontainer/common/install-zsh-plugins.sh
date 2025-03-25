#!/usr/bin/env bash
set -euo pipefail

REPO="${ZSH_AUTOSUGGESTIONS_REPO:-https://github.com/zsh-users/zsh-autosuggestions.git}"

# Install Oh My Zsh if not already installed
[ ! -d "$HOME/.oh-my-zsh" ] && \
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Install zsh-autosuggestions plugin if not already installed
if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autosuggestions" ]; then
  git clone "$REPO" "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autosuggestions"
fi

# Create/update zsh configuration
ZSH_CONFIG="$HOME/.zshrc"
# Remove existing plugin line if it exists to avoid duplication
grep -v "^plugins=(" "$ZSH_CONFIG" > "$ZSH_CONFIG.tmp" || true
echo 'plugins=(git docker docker-compose zsh-autosuggestions)' >> "$ZSH_CONFIG.tmp"
echo 'export PATH=$PATH:$HOME/.local/bin' >> "$ZSH_CONFIG.tmp"
mv "$ZSH_CONFIG.tmp" "$ZSH_CONFIG"