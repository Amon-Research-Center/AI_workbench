# Create the bootstrap script for wiring both repos quickly.
import os, stat, textwrap

script_path = "/mnt/data/bootstrap.sh"
script = r"""#!/usr/bin/env bash
# High security, low drag bootstrap for:
# 1) atlas-memory-trust
# 2) arl-atft
set -euo pipefail

echo "=== Bootstrap: Memory Trust + ATFT ==="

# --- Read inputs ---
read -r -p "Path to atlas-memory-trust.zip [./atlas-memory-trust.zip]: " MT_ZIP
MT_ZIP=${MT_ZIP:-./atlas-memory-trust.zip}
read -r -p "Path to arl-atft_skeleton.zip [./arl-atft_skeleton.zip]: " ATFT_ZIP
ATFT_ZIP=${ATFT_ZIP:-./arl-atft_skeleton.zip}

read -r -p "Memory Trust repo URL (SSH): " MT_URL
read -r -p "ATFT repo URL (SSH): " ATFT_URL
read -r -p "Initial Memory Trust project slug (e.g., amon_turing_2025): " PROJ

# --- Checks ---
for f in "$MT_ZIP" "$ATFT_ZIP"; do
  [[ -f "$f" ]] || { echo "Missing: $f"; exit 2; }
done
command -v git >/dev/null || { echo "git not found"; exit 3; }
command -v unzip >/dev/null || { echo "unzip not found"; exit 4; }
command -v sha256sum >/dev/null || { echo "sha256sum not found"; exit 5; }
# gpg optional

# --- Utility: signed commit if possible ---
signed_commit() {
  local msg="$1"
  if git config --get commit.gpgsign >/dev/null; then
    git commit -S -m "$msg" || git commit -m "$msg"
  else
    # try to enable signing if key exists
    if gpg --list-secret-keys >/dev/null 2>&1; then
      git config commit.gpgsign true || true
      git commit -S -m "$msg" || git commit -m "$msg"
    else
      git commit -m "$msg"
    fi
  fi
}

# --- 1) Memory Trust repo ---
echo "[1/2] Setting up atlas-memory-trust…"
rm -rf atlas-memory-trust
unzip -q "$MT_ZIP" -d .
cd atlas-memory-trust

git init -b main
git add .
signed_commit "init: atlas-memory-trust skeleton"

# install pre-commit hook
if [[ -f scripts/hooks/pre-commit.sample ]]; then
  mkdir -p .git/hooks
  cp scripts/hooks/pre-commit.sample .git/hooks/pre-commit
  chmod +x .git/hooks/pre-commit
fi

# create first project namespace and run integrity
if [[ -d 10_projects/example ]]; then
  cp -r 10_projects/example "10_projects/${PROJ}"
fi

if [[ -x tools/integrity.sh ]]; then
  ./tools/integrity.sh "${PROJ}" update
  git add "10_projects/${PROJ}/manifest.yaml" "10_projects/${PROJ}/"*.sha256 || true
  signed_commit "proj: start ${PROJ} + checksums"
fi

git remote add origin "$MT_URL"
git push -u origin main

cd ..

# --- 2) ATFT repo ---
echo "[2/2] Setting up ARL-ATFT…"
rm -rf arl-atft
unzip -q "$ATFT_ZIP" -d .
cd arl-atft

git init -b main
git add .
signed_commit "init: ARL-ATFT skeleton"

git remote add origin "$ATFT_URL"
git push -u origin main

echo "=== Done. Repos pushed ==="
echo "Next steps:"
echo " - In GitHub, enable branch protection on 'main' for both repos."
echo " - In atlas-memory-trust, verify Actions 'verify-integrity' runs on push."
echo " - Drop your latest ATFT PDF into 'papers/' and commit."
"""
with open(script_path, "w") as f:
    f.write(script)

# Make executable
os.chmod(script_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | 
                      stat.S_IRGRP | stat.S_IXGRP | 
                      stat.S_IROTH | stat.S_IXOTH)

script_path
