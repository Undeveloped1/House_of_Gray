#!/bin/bash
# notify-telegram.sh — Send a Telegram DM to any chat_id
# Usage: ./notify-telegram.sh <chat_id> "message"
#        echo "message" | ./notify-telegram.sh <chat_id>
set -euo pipefail

if [[ $# -ge 2 ]]; then
  CHAT_ID="$1"
  shift
  MESSAGE="$1"
elif [[ $# -eq 1 ]]; then
  CHAT_ID="$1"
  MESSAGE=$(cat)
else
  echo "Usage: notify-telegram.sh <chat_id> \"message\"  or  echo \"msg\" | notify-telegram.sh <chat_id>" >&2
  exit 1
fi

if [[ -z "${MESSAGE}" || -z "${CHAT_ID}" ]]; then
  echo "Error: Both chat_id and message are required" >&2
  exit 1
fi

CONFIG="/root/.openclaw/openclaw.json"
TOKEN=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['channels']['telegram']['botToken'])" "$CONFIG" 2>/dev/null)

if [[ -z "${TOKEN}" ]]; then
  echo "Error: Could not read Telegram bot token" >&2
  exit 1
fi

curl -s -S -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}" \
  --data-urlencode "text=${MESSAGE}" \
  --data-urlencode "parse_mode=Markdown"
