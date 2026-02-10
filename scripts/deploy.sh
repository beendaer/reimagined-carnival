#!/usr/bin/env bash
set -euo pipefail
ENV="${1:-staging}"
echo "Deploying to ${ENV} at $(date -u) commit $(git rev-parse --short HEAD)"
case "${ENV}" in staging) echo "Staging deploy";; production) echo "Production deploy";; *) echo "Unknown env" && exit 1;; esac
