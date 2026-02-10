#!/usr/bin/env bash
set -euo pipefail
echo "Bootstrapping reimagined-carnival..."
if [ -d "/data/data/com.termux" ]; then pkg update -y && pkg install git python nodejs-lts openssh curl jq -y; fi
[ -f "requirements.txt" ] && pip install -r requirements.txt
[ -f "package.json" ] && npm install
echo "Done"
