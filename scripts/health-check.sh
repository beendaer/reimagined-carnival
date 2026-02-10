#!/usr/bin/env bash
set -euo pipefail
echo "Health Check $(date -u)"
git --version 2>&1; python3 --version 2>&1; node --version 2>&1; docker --version 2>&1 || true
