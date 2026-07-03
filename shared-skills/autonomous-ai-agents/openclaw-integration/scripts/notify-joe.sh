#!/bin/bash
# Rook -> Joe Telegram DM (reminders, notifications — not group posts)
# Copy to ~/.openclaw/agents/<agent>/workspace/notify-joe.sh and chmod +x
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: notify-joe.sh \"message\"" >&2
  exit 1
fi

CONTENT="$1"
CHAT_ID="<JOE_TELEGRAM_USER_ID>"
CONFIG="${OPENCLAW_CONFIG:-/root/.openclaw/openclaw.json}"

TOKEN="$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['channels']['telegram']['botToken'])" "$CONFIG")"

curl -s -S -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}" \
  --data-urlencode "text=${CONTENT}"