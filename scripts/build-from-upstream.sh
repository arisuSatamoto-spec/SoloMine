#!/usr/bin/env bash
set -euo pipefail
# Reproducible build from a user-specified upstream revision.
# Usage: bash scripts/build-from-upstream.sh <40-char-commit-sha>
if [[ $# -ne 1 || ! "$1" =~ ^[0-9a-fA-F]{40}$ ]]; then
  echo "Usage: $0 <40-character upstream CKPool commit SHA>" >&2
  exit 2
fi
root="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$root/build"
if [[ -e "$root/build/ckpool" ]]; then
  echo "Remove build/ckpool before rebuilding to avoid modifying existing source" >&2
  exit 1
fi
git clone https://github.com/ckolivas/ckpool.git "$root/build/ckpool"
cd "$root/build/ckpool"
git checkout --detach "$1"
python3 "$root/scripts/apply-fee-patch.py" "$PWD"
./autogen.sh
./configure
make -j2
echo "Built upstream checkout at $PWD. Do NOT use on mainnet before regtest integration testing."
