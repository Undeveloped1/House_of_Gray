#!/bin/bash
# Force-reset a stuck Hermes profile gateway
# Usage: bash reset-gateway.sh <profile-name>
# Example: bash reset-gateway.sh hans

set -e

NAME="$1"
if [ -z "$NAME" ]; then
  echo "Usage: $0 <profile-name>"
  echo "Example: $0 hans"
  exit 1
fi

SERVICE="hermes-gateway-${NAME}"

echo "[1/5] Killing any stale gateway processes..."
pkill -9 -f "profile ${NAME} gateway" 2>/dev/null || true

echo "[2/5] Removing stale lock files..."
rm -f /root/.local/state/hermes/gateway-locks/telegram-bot-token-*.lock 2>/dev/null || true

echo "[3/5] Stopping and disabling old service..."
systemctl stop "$SERVICE" 2>/dev/null || true
systemctl disable "$SERVICE" 2>/dev/null || true

echo "[4/5] Reinstalling gateway..."
hermes -p "$NAME" gateway install --system --run-as-user root --start-now

echo "[5/5] Adding EnvironmentFile..."
# Check if EnvironmentFile is already there
if grep -q "EnvironmentFile=" /etc/systemd/system/hermes-gateway-"${NAME}".service 2>/dev/null; then
  echo "  EnvironmentFile already present."
else
  # Add it after the HERMES_HOME line
  sed -i '/HERMES_HOME=/a EnvironmentFile=/root/.hermes/profiles/'"${NAME}"'/.env' \
    /etc/systemd/system/hermes-gateway-"${NAME}".service
  echo "  EnvironmentFile added."
fi

systemctl daemon-reload
systemctl restart "$SERVICE"

echo ""
echo "Done. Check status:"
echo "  systemctl status $SERVICE"
echo "  journalctl -u $SERVICE -n 20 --no-pager"
