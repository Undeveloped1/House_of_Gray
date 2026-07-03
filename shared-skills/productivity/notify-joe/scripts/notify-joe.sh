#!/bin/bash
# notify-joe.sh — Send a Telegram DM to Joe
# Usage: ./notify-joe.sh "Your message here"
#        echo "message" | ./notify-joe.sh
set -euo pipefail

if [[ $# -ge 1 ]]; then
  MESSAGE="$1"
else
  MESSAGE=$(cat)
fi

if [[ -z "${MESSAGE}" ]]; then
  echo "Usage: notify-joe.sh \"message\"  or  echo \"msg\" | notify-joe.sh" >&2
  exit 1
fi

CHAT_ID="7239715879"
CONFIG="/root/.openclaw/openclaw.json"
TOKEN=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['channels']['telegram']['botToken'])" "$CONFIG" 2>/dev/null)

if [[ -z "${TOKEN}" ]]; then
  echo "Error: Could not read Telegram bot token from ${CONFIG}" >&2
  exit 1
fi

RESPONSE=$(curl -s -S -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}" \
  --data-urlencode "text=${MESSAGE}" \
  --data-urlencode "parse_mode=Markdown" 2>&1)

if echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if d.get('ok') else 1)" 2>/dev/null; then
  echo "✅ Delivered to Joe"
  # Log it
  LOGDIR="/root/.hermes/docs/notify-joe/logs"
  mkdir -p "$LOGDIR"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $(whoami): ${MESSAGE:0:100}" >> "${LOGDIR}/$(date '+%Y-%m-%d').log"
else
  echo "❌ Failed: $RESPONSE" >&2
  exit 1
fi
