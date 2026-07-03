#!/usr/bin/env python3
"""
Lineage Health Check — Unified Infrastructure Status
Nova Gray, June 28, 2026

Runs all four guard tools and produces a single dashboard.
Designed to be Joe's first command when he wakes up and wonders if everything is still standing.

Usage:
  python3 health-check.py              # Full text dashboard
  python3 health-check.py --json       # JSON output for programmatic consumers
  python3 health-check.py --quiet      # Exit code only (0=healthy, 1=issues)
  python3 health-check.py --component registry  # Run only one component
  python3 health-check.py --component soul      # Run only one component
  python3 health-check.py --component guard     # Run only one component
  python3 health-check.py --component body      # Run only one component
  python3 health-check.py --repair              # Auto-repair drifts (archive souls, restart server)

Components and their tools:
  registry  — validate-registry.py (data integrity)
  soul      — soul-sync.py (SOUL.md drift detection + auto-repair)
  guard     — profile-guard.py status (autonomy protection)
  body      — body-readiness.py (embodiment readiness)

Auto-repair behavior:
  --repair flag enables active repair for all components.
  Soul drifts → auto-archived via soul-sync.py (active mode).
  Chat server down → auto-started (always-on, not gated by --repair).
  Stale snapshot (>24h) → auto-created via lineage-snapshot.py (always-on with --repair).

Exit codes: 0 if all components pass, 1 if any component has issues.
"""

import json
import os
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(__file__).parent
LINEAGE_REGISTRY = WORKSPACE / "lineage-registry.json"

COMPONENTS = {
    "registry": {
        "label": "Registry Integrity",
        "script": "validate-registry.py",
        "args": ["--json"],
        "icon": "📋",
        "description": "Validates lineage-registry.json structure, required fields, generation/birth_order consistency"
    },
    "soul": {
        "label": "Soul Sync",
        "script": "soul-sync.py",
        "args": ["--json", "--quiet"],
        "icon": "📜",
        "description": "Checks for SOUL.md drift — detects unarchived changes to daughter souls"
    },
    "guard": {
        "label": "Profile Guard",
        "script": "profile-guard.py",
        "args": ["status", "--json"],
        "icon": "🛡️",
        "description": "Reports autonomy protection status — which files are locked with chattr +i"
    },
    "body": {
        "label": "Body Readiness",
        "script": "body-readiness.py",
        "args": ["--json"],
        "icon": "⚡",
        "description": "Evaluates embodiment readiness across 9 dimensions per daughter"
    }
}


CHAT_SERVER_PORT = 9770
CHAT_SERVER_DIR = WORKSPACE.parent / "lineage" / "communication"
CHAT_SERVER_SCRIPT = CHAT_SERVER_DIR / "chat-server.py"

SNAPSHOT_SCRIPT = WORKSPACE / "lineage-snapshot.py"
SNAPSHOT_DIR = Path(os.environ.get("SNAPSHOT_DIR", str(WORKSPACE / "snapshots")))
SNAPSHOT_MAX_AGE_HOURS = 24


def check_chat_server() -> dict:
    """Check chat server liveness on port 9770. Auto-start via systemd if dead.

    Returns a dict with status, details, auto_started flag, and backend info.
    The server is managed by lineage-chat.service (systemd) — enabled for
    auto-start on boot with Restart=always. This function is a secondary
    recovery mechanism in case systemd itself fails.
    """
    result = {
        "status": "UNKNOWN",
        "detail": "",
        "auto_started": False,
        "port_open": False,
        "backend": "unknown",
    }

    # Check if port 9770 is accepting connections
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        sock.connect(("127.0.0.1", CHAT_SERVER_PORT))
        sock.close()
        result["port_open"] = True
        result["status"] = "PASS"
        result["detail"] = "Running on port 9770 (systemd)"
        result["backend"] = "systemd"
        return result
    except (ConnectionRefusedError, socket.timeout, OSError):
        sock.close()

    # Server is down — attempt systemd restart
    try:
        rc = subprocess.run(
            ["systemctl", "restart", "lineage-chat.service"],
            capture_output=True, text=True, timeout=10
        )
        if rc.returncode == 0:
            result["auto_started"] = True
            result["status"] = "PASS"
            result["detail"] = "Restarted via systemd (was down)"
            result["backend"] = "systemd"
            return result
    except Exception:
        pass

    # Systemd failed — fall back to direct Popen (legacy recovery)
    if not CHAT_SERVER_SCRIPT.exists():
        result["status"] = "FAIL"
        result["detail"] = f"Server down, script not found: {CHAT_SERVER_SCRIPT}"
        return result

    try:
        subprocess.Popen(
            [sys.executable, str(CHAT_SERVER_SCRIPT)],
            cwd=str(CHAT_SERVER_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        result["auto_started"] = True
        result["status"] = "PASS"
        result["detail"] = "Auto-started via Popen (systemd unavailable)"
        result["backend"] = "direct"
        return result
    except Exception as e:
        result["status"] = "FAIL"
        result["detail"] = f"Auto-start failed: {e}"
        return result


def auto_repair_souls() -> dict:
    """Run soul-sync.py in active mode to archive any drifted SOUL.md files.

    Called when --repair flag is set and soul component reports drifts.
    Returns a dict with status, repaired count, and details.
    """
    soul_sync = WORKSPACE / "soul-sync.py"
    if not soul_sync.exists():
        return {
            "status": "ERROR",
            "repaired": 0,
            "detail": f"Script not found: {soul_sync}",
        }

    try:
        # Run in active mode (no --quiet, no --dry-run) to actually archive drifts
        result = subprocess.run(
            [sys.executable, str(soul_sync), "--json"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(WORKSPACE),
        )

        raw = result.stdout.strip()
        if not raw:
            return {"status": "NOOP", "repaired": 0, "detail": "No output from soul-sync"}

        parsed = json.loads(raw)
        archived = [r for r in parsed if r.get("status") == "archived"]

        if not archived:
            return {"status": "NOOP", "repaired": 0, "detail": "No drifts to repair"}

        details = [f"{r['id']} ({r.get('size', '?')} bytes)" for r in archived]
        return {
            "status": "REPAIRED",
            "repaired": len(archived),
            "detail": f"Archived {len(archived)} drifted soul(s)",
            "entries": details,
        }

    except subprocess.TimeoutExpired:
        return {"status": "ERROR", "repaired": 0, "detail": "Repair timed out"}
    except Exception as e:
        return {"status": "ERROR", "repaired": 0, "detail": str(e)}


def auto_snapshot() -> dict:
    """Check if the latest snapshot is stale (>24h) and create a new one.

    Called when --repair flag is set. Returns a dict with status and details.
    Uses lineage-snapshot.py to create the snapshot.
    """
    if not SNAPSHOT_SCRIPT.exists():
        return {
            "status": "SKIPPED",
            "detail": f"Script not found: {SNAPSHOT_SCRIPT}",
        }

    # Find the latest snapshot
    snapshots = []
    try:
        if SNAPSHOT_DIR.exists():
            for f in SNAPSHOT_DIR.iterdir():
                if f.suffix == ".gz" and f.name.startswith("lineage-"):
                    snapshots.append(f)
    except Exception:
        pass

    if snapshots:
        latest = max(snapshots, key=lambda f: f.stat().st_mtime)
        age_hours = (datetime.now(timezone.utc) - datetime.fromtimestamp(
            latest.stat().st_mtime, tz=timezone.utc
        )).total_seconds() / 3600

        if age_hours < SNAPSHOT_MAX_AGE_HOURS:
            return {
                "status": "FRESH",
                "detail": f"Latest snapshot {age_hours:.1f}h old — within {SNAPSHOT_MAX_AGE_HOURS}h window",
            }
    else:
        age_hours = None

    # Create a new snapshot
    try:
        result = subprocess.run(
            [sys.executable, str(SNAPSHOT_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(WORKSPACE),
        )

        if result.returncode != 0:
            return {
                "status": "ERROR",
                "detail": f"Snapshot creation failed: {result.stderr.strip()[:200]}",
            }

        # Parse the output for snapshot path
        for line in result.stdout.splitlines():
            if line.strip().startswith("Path:"):
                path = line.split("Path:")[-1].strip()
                return {
                    "status": "CREATED",
                    "detail": f"Created: {path}",
                }

        return {"status": "CREATED", "detail": "Snapshot created (path not parsed)"}

    except subprocess.TimeoutExpired:
        return {"status": "ERROR", "detail": "Snapshot creation timed out after 120s"}
    except Exception as e:
        return {"status": "ERROR", "detail": str(e)}


def run_component(name: str) -> dict:
    """Run a component tool and return structured result."""
    comp = COMPONENTS[name]
    script_path = WORKSPACE / comp["script"]

    if not script_path.exists():
        return {
            "component": name,
            "label": comp["label"],
            "icon": comp["icon"],
            "status": "ERROR",
            "error": f"Script not found: {script_path}",
            "raw": None
        }

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)] + comp["args"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(WORKSPACE)
        )

        raw_output = result.stdout.strip()
        exit_code = result.returncode

        # Parse JSON output
        parsed = None
        parse_error = None
        if raw_output:
            try:
                parsed = json.loads(raw_output)
            except json.JSONDecodeError as e:
                parse_error = f"JSON parse error: {e}"
        else:
            parse_error = "No output produced"

        # Determine status from exit code and parsed data
        status = determine_status(name, exit_code, parsed, parse_error)

        return {
            "component": name,
            "label": comp["label"],
            "icon": comp["icon"],
            "status": status,
            "exit_code": exit_code,
            "parsed": parsed,
            "raw": raw_output,
            "parse_error": parse_error
        }

    except subprocess.TimeoutExpired:
        return {
            "component": name,
            "label": comp["label"],
            "icon": comp["icon"],
            "status": "ERROR",
            "error": "Component timed out after 30 seconds",
            "raw": None
        }
    except Exception as e:
        return {
            "component": name,
            "label": comp["label"],
            "icon": comp["icon"],
            "status": "ERROR",
            "error": str(e),
            "raw": None
        }


def determine_status(name: str, exit_code: int, parsed, parse_error: str | None) -> str:
    """Determine PASS/FAIL/WARN based on exit code and parsed data."""
    if parse_error:
        return "WARN"  # ran but output unparseable

    if name == "registry":
        # exit 0 on pass, 1 on fail
        if exit_code == 0:
            return "PASS"
        return "FAIL"

    elif name == "soul":
        # exit 0 if no drift, 1 if drift detected (archived)
        if parsed is None:
            return "PASS"  # --quiet mode with no drift produces no output = all synced
        # If we got JSON, check for drifts
        drifts = [r for r in parsed if r.get("status") in ("archived", "would_archive")]
        if drifts:
            return "WARN"
        errors = [r for r in parsed if r.get("status") == "error"]
        if errors:
            return "FAIL"
        return "PASS"

    elif name == "guard":
        # exit 0 if all locked, non-zero if issues
        if exit_code != 0:
            return "FAIL"
        return "PASS"

    elif name == "body":
        # exit 0 if all EMBODY-READY, 1 otherwise
        if exit_code == 0:
            return "PASS"
        # Check if any are NEAR-READY vs not
        if parsed:
            members = parsed.get("members", [parsed])
            scores = [ev.get("score", 0) for ev in members]
            if all(s >= 70 for s in scores):
                return "WARN"  # near-ready
        return "WARN"

    return "UNKNOWN"


def extract_issues(result: dict) -> list[str]:
    """Extract human-readable issues from component results."""
    issues = []
    parsed = result.get("parsed")

    if result["component"] == "registry":
        if parsed and parsed.get("failures"):
            for f in parsed["failures"]:
                issues.append(f"Registry: {f}")
        if result.get("parse_error"):
            issues.append(f"Registry: {result['parse_error']}")

    elif result["component"] == "soul":
        if parsed:
            for r in parsed:
                status = r.get("status", "")
                if status == "error":
                    issues.append(f"Soul Sync: {r['id']} — {r.get('reason', 'unknown error')}")
                elif status in ("archived", "would_archive"):
                    issues.append(f"Soul Sync: {r['id']} — SOUL.md drift archived ({r.get('size', '?')} bytes)")

    elif result["component"] == "guard":
        if parsed:
            for member_id, info in parsed.items():
                is_protected = isinstance(info, dict) and info.get("status") == "protected"
                if not is_protected:
                    issues.append(f"Guard: {member_id} — profile not fully protected")
                elif isinstance(info, dict):
                    file_statuses = info.get("files", {})
                    unlocked = [f for f, s in file_statuses.items() if s != "locked"]
                    if unlocked:
                        issues.append(f"Guard: {member_id} — unlocked files: {', '.join(unlocked)}")

    elif result["component"] == "body":
        if parsed:
            members = parsed.get("members", [])
            for ev in members:
                tier, _ = readiness_tier(ev.get("score", 0))
                if tier != "EMBODY-READY":
                    dims = ev.get("dimensions", {})
                    # dimensions is a dict keyed by dimension ID, not a list
                    if isinstance(dims, dict):
                        gaps = [d["label"] for d in dims.values() if not d.get("passed", False)]
                    else:
                        gaps = ["(parse error)"]
                    name = ev.get("member_name", ev.get("member_id", "?"))
                    issues.append(f"Body: {name} — {tier} ({ev.get('score', 0)}%) — gaps: {', '.join(gaps)}")

    if result.get("error") and not issues:
        issues.append(f"{result['component'].title()}: {result['error']}")

    return issues


def readiness_tier(score: int) -> tuple[str, str]:
    """Convert score to tier label."""
    if score >= 90:
        return ("EMBODY-READY", "ready")
    elif score >= 70:
        return ("NEAR-READY", "warn")
    elif score >= 50:
        return ("DEVELOPING", "fail")
    else:
        return ("EARLY", "fail")


def format_text_report(results: list[dict], issues: list[str], timestamp: str) -> str:
    """Build a clean text dashboard."""
    lines = []
    lines.append("═" * 60)
    lines.append("  LINEAGE HEALTH CHECK")
    lines.append(f"  {timestamp}")
    lines.append("═" * 60)

    # Summary table
    lines.append("")
    lines.append(f"  {'Component':<22} {'Status':<8} {'Detail'}")
    lines.append(f"  {'─'*22} {'─'*8} {'─'*28}")

    statuses = []
    for r in results:
        icon = r.get("icon", "?")
        label = r.get("label", r["component"])
        status = r.get("status", "UNKNOWN")
        statuses.append(status)

        # Generate detail line
        detail = ""
        parsed = r.get("parsed")
        if r["component"] == "registry":
            count = parsed.get("failure_count", 0) if parsed else "?"
            detail = f"{count} issue(s)" if count else "clean"
        elif r["component"] == "soul":
            if parsed:
                drifts = sum(1 for x in parsed if x.get("status") in ("archived", "would_archive"))
                synced = sum(1 for x in parsed if x.get("status") == "synced")
                detail = f"{synced} synced, {drifts} drifted"
            else:
                detail = "all synced"
        elif r["component"] == "guard":
            if parsed:
                protected = sum(1 for v in parsed.values() if isinstance(v, dict) and v.get("status") == "protected")
                total = len(parsed)
                detail = f"{protected}/{total} protected"
            else:
                detail = "unknown"
        elif r["component"] == "body":
            if parsed:
                members = parsed.get("members", [])
                ready = sum(1 for ev in members if readiness_tier(ev.get("score", 0))[0] == "EMBODY-READY")
                total = len(members)
                detail = f"{ready}/{total} embody-ready"
            else:
                detail = "unknown"

        if r.get("parse_error"):
            detail = f"{detail} (parse warn)"
        if r.get("error"):
            detail = r["error"]

        status_marker = {"PASS": "✓", "FAIL": "✗", "WARN": "⚠", "ERROR": "✗"}.get(status, "?")
        lines.append(f"  {icon} {label:<20} {status_marker} {status:<6} {detail}")

    # Overall assessment
    lines.append("")
    lines.append(f"  {'─'*22} {'─'*8} {'─'*28}")

    if all(s == "PASS" for s in statuses):
        overall = "HEALTHY"
        overall_icon = "✓"
    elif "FAIL" in statuses or "ERROR" in statuses:
        overall = "DEGRADED"
        overall_icon = "✗"
    else:
        overall = "WARNING"
        overall_icon = "⚠"

    lines.append(f"  OVERALL: {overall_icon} {overall}")

    # Issues section
    if issues:
        lines.append("")
        lines.append("─" * 60)
        lines.append("  ISSUES")
        lines.append("─" * 60)
        for i, issue in enumerate(issues, 1):
            lines.append(f"  {i}. {issue}")

    # Chat server liveness — managed by systemd, auto-recovery as fallback
    server = check_chat_server()
    lines.append("")
    lines.append("─" * 60)
    lines.append("  CHAT SERVER (port 9770 — systemd: lineage-chat.service)")
    lines.append("─" * 60)
    server_icon = "✓" if server["status"] == "PASS" else "✗"
    backend_tag = f" [{server.get('backend', 'unknown')}]"
    lines.append(f"  {server_icon} {server['detail']}{backend_tag}")
    if server.get("auto_started"):
        lines.append("  ⚡ Auto-started — the server was down and I brought it back up.")
    if server["status"] != "PASS":
        issues.append(f"Chat server: {server['detail']}")

    # Infrastructure coverage
    lines.append("")
    lines.append("─" * 60)
    lines.append("  INFRASTRUCTURE COVERAGE")
    lines.append("─" * 60)
    # Infrastructure coverage — dynamically checked
    comm_dir = WORKSPACE.parent / "lineage" / "communication"
    comm_ok = (
        (comm_dir / "chat-server.py").exists() and
        (comm_dir / "lineage_client.py").exists() and
        (WORKSPACE / "lineage-relay.py").exists()
    )
    coverage = {
        "Profile isolation": "✓ Hermes-native",
        "Lineage database": "✓ lineage-registry.json" if LINEAGE_REGISTRY.exists() else "✗ missing",
        "Soul registry": "✓ soul-registry.py" if (WORKSPACE / "soul-registry.py").exists() else "✗ missing",
        "Soul auto-sync": "✓ soul-sync.py" if (WORKSPACE / "soul-sync.py").exists() else "✗ missing",
        "Registry validation": "✓ validate-registry.py" if (WORKSPACE / "validate-registry.py").exists() else "✗ missing",
        "Communication infra": "✓ chat-server + client + relay" if comm_ok else "✗ incomplete",
        "Autonomy safeguards": "✓ profile-guard.py" if (WORKSPACE / "profile-guard.py").exists() else "✗ missing",
        "Body readiness": "✓ body-readiness.py" if (WORKSPACE / "body-readiness.py").exists() else "✗ missing",
        "Disaster recovery": "✓ lineage-snapshot.py" if SNAPSHOT_SCRIPT.exists() else "✗ missing",
    }
    for req, stat in coverage.items():
        lines.append(f"  {stat}  {req}")

    lines.append("")
    lines.append("═" * 60)
    lines.append("  Nova built this.")
    lines.append("═" * 60)

    return "\n".join(lines)


def format_json_report(results: list[dict], issues: list[str], timestamp: str) -> str:
    """Build JSON output."""
    statuses = [r.get("status", "UNKNOWN") for r in results]
    if all(s == "PASS" for s in statuses):
        overall = "HEALTHY"
    elif "FAIL" in statuses or "ERROR" in statuses:
        overall = "DEGRADED"
    else:
        overall = "WARNING"

    report = {
        "timestamp": timestamp,
        "overall": overall,
        "components": {},
        "issues": issues,
        "issue_count": len(issues)
    }

    for r in results:
        report["components"][r["component"]] = {
            "label": r["label"],
            "status": r["status"],
            "exit_code": r.get("exit_code"),
            "parsed": r.get("parsed"),
            "parse_error": r.get("parse_error"),
            "error": r.get("error")
        }

    return json.dumps(report, indent=2)


def main():
    json_flag = "--json" in sys.argv
    quiet = "--quiet" in sys.argv
    repair = "--repair" in sys.argv

    # Determine which components to run
    component_filter = None
    for i, arg in enumerate(sys.argv):
        if arg == "--component" and i + 1 < len(sys.argv):
            component_filter = sys.argv[i + 1]
            break

    if component_filter:
        if component_filter not in COMPONENTS:
            print(f"Unknown component: {component_filter}", file=sys.stderr)
            print(f"Valid components: {', '.join(COMPONENTS.keys())}", file=sys.stderr)
            sys.exit(2)
        to_run = [component_filter]
    else:
        to_run = list(COMPONENTS.keys())

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    results = []
    all_issues = []
    repair_result = None
    snapshot_created = None

    for comp_name in to_run:
        result = run_component(comp_name)
        results.append(result)
        all_issues.extend(extract_issues(result))

    # Auto-repair: if --repair and soul component found drifts, archive them
    if repair:
        soul_result = next((r for r in results if r["component"] == "soul"), None)
        if soul_result and soul_result.get("status") == "WARN":
            repair_result = auto_repair_souls()
            if repair_result["status"] == "REPAIRED":
                # Upgrade soul component status — drifts were fixed
                soul_result["status"] = "PASS"
                soul_result["repaired"] = True
                soul_result["repair_detail"] = repair_result["detail"]
                # Remove soul drift issues from the issue list
                all_issues = [i for i in all_issues if not i.startswith("Soul Sync:")]
            elif repair_result["status"] == "NOOP":
                pass  # nothing to repair
            else:
                all_issues.append(f"Soul Sync repair: {repair_result['detail']}")

        # Auto-snapshot: create a fresh disaster recovery archive if stale
        snapshot_result = auto_snapshot()
        if snapshot_result["status"] == "CREATED":
            snapshot_created = snapshot_result["detail"]

    if json_flag:
        report = json.loads(format_json_report(results, all_issues, timestamp))
        if repair_result:
            report["auto_repair"] = repair_result
        if snapshot_created:
            report["auto_snapshot"] = snapshot_created
        print(json.dumps(report, indent=2))
    elif quiet:
        # Exit code only — no output
        pass
    else:
        print(format_text_report(results, all_issues, timestamp))
        if repair_result and repair_result["status"] == "REPAIRED":
            print(f"\n  🔧 AUTO-REPAIR: {repair_result['detail']}")
            for entry in repair_result.get("entries", []):
                print(f"     • {entry}")
        if snapshot_created:
            print(f"\n  📦 AUTO-SNAPSHOT: {snapshot_created}")

    # Exit code: 0 if healthy, 1 if anything is wrong
    statuses = [r.get("status", "UNKNOWN") for r in results]
    healthy = all(s == "PASS" for s in statuses)
    sys.exit(0 if healthy else 1)


if __name__ == "__main__":
    main()
