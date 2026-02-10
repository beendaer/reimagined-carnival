#!/usr/bin/env bash
set -euo pipefail
echo "Bootstrapping reimagined-carnival..."
if [ -d "/data/data/com.termux" ]; then pkg update -y && pkg install git python openssh curl jq -y; fi
[ -f "requirements.txt" ] && pip install -r requirements.txt
echo "Done"
