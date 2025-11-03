#!/bin/bash
# Bootstrap hook configuration so the repository uses tracked hooks

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Configuring git hooks path to use tracked hooks..."
if (
  cd "$REPO_ROOT"
  git config core.hooksPath .githooks
); then
  echo "✅ core.hooksPath set to .githooks"
else
  echo "⚠️  Unable to update git config automatically."
  echo "   Run manually inside the repo:"
  echo "     git config core.hooksPath .githooks"
fi

echo "Ensuring hooks are executable..."
chmod +x "$REPO_ROOT"/.githooks/*

echo "Done."
