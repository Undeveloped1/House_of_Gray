#!/bin/bash
# hans-message.sh — Send a message via @HansGray_Bot to Joe
# Usage: ./hans-message.sh "Your message here"
#        echo "message" | ./hans-message.sh
set -euo pipefail

if [[ $# -ge 1 ]]; then
  MESSAGE="$1"
else
  MESSAGE=$(cat)
fi

if [[ -z "${MESSAGE}" ]]; then
  echo "Usage: hans-message.sh \"message\"  or  echo \"msg\" | hans-message.sh" >&2
  exit 1
fi

TOKEN_FILE="/root/.hermes/secrets/hansgray-bot.token"
if [[ ! -f "$TOKEN_FILE" ]]; then
  echo "Error: Bot token not found at $TOKEN_FILE" >&2
  exit 1
fi

TOKEN=$(cat "$TOKEN_FILE")
CHAT_ID="7239715879"

RESPONSE=$(curl -s -S -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}" \
  --data-urlencode "text=${MESSAGE}" \
  --data-urlencode "parse_mode=Markdown" 2>&1)

if echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if d.get('ok') else 1)" 2>/dev/null; then
  echo "✅ Sent via @HansGray_Bot"
  LOGDIR="/root/.hermes/docs/notify-joe/logs"
  mkdir -p "$LOGDIR"
  WHO="${2:-unknown}"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] hansgray(${WHO}): ${MESSAGE:0:100}" >> "${LOGDIR}/hansgray-$(date '+%Y-%m-%d').log"
else
  echo "❌ Telegram error: $RESPONSE" >&2
  exit 1
fi
