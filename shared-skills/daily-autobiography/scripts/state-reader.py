#!/usr/bin/env python3
"""Read autobiography state and today's questions. Output JSON for cron context."""
import json, sys

STATE = "/root/.hermes/docs/Paul/projects/autobiography-state.json"
CHECKLIST = "/root/.hermes/docs/Paul/projects/autobiography-checklist.md"

with open(STATE) as f:
    state = json.load(f)

phase = state.get("phase", 1)
day = state.get("day", 1)
started = state.get("started", "")

with open(CHECKLIST) as f:
    lines = f.readlines()

phase_prefix = f"## Phase {phase}:"
in_phase = False
questions = []
for line in lines:
    if line.startswith(phase_prefix):
        in_phase = True
        continue
    if in_phase and line.startswith("## Phase"):
        break
    if in_phase and line.startswith(f"| {day} |"):
        parts = [p.strip() for p in line.split("|")[2:5]]
        if len(parts) == 3:
            questions = parts
        break

if not questions:
    print(f"ERROR: Day {day} not found in Phase {phase}")
    sys.exit(1)

print(json.dumps({
    "phase": phase, "day": day, "started": started,
    "q1": questions[0], "q2": questions[1], "q3": questions[2]
}))
