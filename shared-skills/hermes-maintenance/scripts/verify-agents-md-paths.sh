#!/bin/bash
# Verify an AGENTS.md was correctly migrated to a new profile path.
# Usage: bash scripts/verify-agents-md-paths.sh <profile_name>
# Example: bash scripts/verify-agents-md-paths.sh paul

PROFILE="${1:?Usage: $0 <profile_name>}"
FILE="$HOME/.hermes/profiles/$PROFILE/AGENTS.md"

if [ ! -f "$FILE" ]; then
  echo "FAIL: AGENTS.md not found at $FILE"
  exit 1
fi

errors=0

# 1. No old default paths remaining
if grep -q '/root/.hermes/docs/' "$FILE" 2>/dev/null; then
  echo "FAIL: old default paths (/root/.hermes/docs/) still present"
  grep -n '/root/.hermes/docs/' "$FILE"
  ((errors++))
else
  echo "PASS: no old /root/.hermes/docs/ paths"
fi

# 2. New profile paths present in key locations
PROFILE_PREFIX="/root/.hermes/profiles/$PROFILE"
declare -a required=(
  "$PROFILE_PREFIX/docs/"
  "$PROFILE_PREFIX/docs/Paul/workspace/"
  "$PROFILE_PREFIX/docs/Paul/Brain/"
)
for path in "${required[@]}"; do
  if grep -qF "$path" "$FILE" 2>/dev/null; then
    echo "PASS: $path found"
  else
    echo "FAIL: $path NOT found (may not be used in this AGENTS.md)"
  fi
done

# 3. External paths preserved (not profile-specific)
declare -a external=("/root/tcg-engine/" "/root/syncthing/" "/root/.hermes/rag-venv/")
for path in "${external[@]}"; do
  if grep -qF "$path" "$FILE" 2>/dev/null; then
    echo "INFO: external path $path preserved (unchanged)"
  fi
done

echo ""
if [ $errors -eq 0 ]; then
  echo "=== ALL CHECKS PASSED ==="
  exit 0
else
  echo "=== $errors FAILURES ==="
  exit 1
fi
