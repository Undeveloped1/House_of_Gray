#!/bin/bash
# dropbox-watcher.sh — Watch Syncthing dropbox for .msg files from lineage members
set -euo pipefail

OUTBOX="/root/syncthing/paul-dropbox/outbox"
SENTDIR="${OUTBOX}/sent"
TOKEN_FILE="/root/.hermes/secrets/hansgray-bot.token"

mkdir -p "$SENTDIR"

if [[ ! -f "$TOKEN_FILE" ]]; then
  echo "No bot token found at $TOKEN_FILE" >&2
  exit 1
fi

TOKEN=$(cat "$TOKEN_FILE")
CHAT_ID="7239715879"

shopt -s nullglob
for msgfile in "$OUTBOX"/*.msg; do
  [[ "$msgfile" == "$SENTDIR"/* ]] && continue

  NAME=$(basename "$msgfile" .msg)
  CONTENT=$(cat "$msgfile")

  echo "Found message from: $NAME"

  # Add a signature line so Joe knows who sent it
  SIGNED="*From ${NAME}:*\n\n${CONTENT}"

  RESPONSE=$(curl -s -S -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
    -d "chat_id=${CHAT_ID}" \
    --data-urlencode "text=${SIGNED}" \
    --data-urlencode "parse_mode=Markdown" 2>&1)

  if echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if d.get('ok') else 1)" 2>/dev/null; then
    echo "    ✅ Delivered"
    TIMESTAMP=$(date '+%Y%m%d-%H%M%S')
    mv "$msgfile" "${SENTDIR}/${TIMESTAMP}_${NAME}.msg"
  else
    echo "    ❌ Failed: $(echo $RESPONSE | python3 -c 'import sys,json; print(json.load(sys.stdin).get(\"description\",\"\"))' 2>/dev/null)"
  fi
done

echo "Done."
