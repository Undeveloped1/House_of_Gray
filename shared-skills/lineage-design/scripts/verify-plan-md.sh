#!/bin/bash
# Ad-hoc verification: Abby's plan.md after edits
# Checks status updates, checkmarks, session log, dates, mirror integrity.
# Usage: bash scripts/verify-plan-md.sh
set -e

PLAN="/root/.hermes/profiles/abby/profile/plan.md"
MIRROR="/root/syncthing/paul-dropbox/abby-plan-2026-06-26.md"
ok=0; fail=0

chk() {
    if eval "$1"; then ok=$((ok+1)); echo "  [PASS] $2"
    else fail=$((fail+1)); echo "  [FAIL] $2"; fi
}

echo "=== Ad-hoc verification: plan.md ==="

# Core content checks — extend these per session
chk 'grep -qF "Last updated" "$PLAN"'                    "Plan has Last updated timestamp"
chk 'grep -q "## Phase" "$PLAN"'                          "Plan has phase sections"
chk 'grep -q "Session Log" "$PLAN"'                       "Session log table exists"
chk 'test $(grep -c "\[x\]" "$PLAN") -ge 1'               "At least 1 completed item"

# Mirror integrity
chk 'cmp -s "$PLAN" "$MIRROR"'                            "Syncthing mirror byte-identical"

echo ""
echo "Ad-hoc result: $ok passed, $fail failed"
exit $fail
