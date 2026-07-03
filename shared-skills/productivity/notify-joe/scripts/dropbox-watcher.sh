#!/bin/bash
# dropbox-watcher.sh — Watch Syncthing dropbox for .msg files from Abby
# Runs as a cron job: checks the outbox, sends any messages via @HansGray_Bot
set -euo pipefail

OUTBOX="/root/syncthing/paul-dropbox/outbox"
SENTDIR="${OUTBOX}/sent"
HANS_SCRIPT="/root/.hermes/skills/productivity/notify-joe/scripts/hans-message.sh"
LOGDIR="/root/.hermes/docs/notify-joe/logs"

mkdir -p "$SENTDIR" "$LOGDIR"

# Find all .msg files in the outbox (not in sent/)
shopt -s nullglob
for msgfile in "$OUTBOX"/*.msg; do
  # Skip if it's in the sent dir
  [[ "$msgfile" == "$SENTDIR"/* ]] && continue

  NAME=$(basename "$msgfile" .msg)
  CONTENT=$(cat "$msgfile")

  echo "[$(date '+%H:%M:%S')] Found message from: $NAME"

  # Send it
  if bash "$HANS_SCRIPT" "$CONTENT" 2>/dev/null; then
    echo "    ✅ Delivered"
    # Archive it
    TIMESTAMP=$(date '+%Y%m%d-%H%M%S')
    mv "$msgfile" "${SENTDIR}/${TIMESTAMP}_${NAME}.msg"
  else
    echo "    ❌ Failed to send — leaving file for retry"
  fi
done

echo "Done. $(ls "$OUTBOX"/*.msg 2>/dev/null | wc -l) messages remaining."
