#!/usr/bin/env python3
"""
Lineage Activity Report — Cross-Profile Session Aggregator
Nova Gray, July 1, 2026

Reads every lineage member's state.db and produces a unified activity summary.
Joe runs one command and sees what everyone's been doing.

Usage:
  python3 lineage-activity.py              # Full text report
  python3 lineage-activity.py --json       # JSON output
  python3 lineage-activity.py --member nova  # Single member
  python3 lineage-activity.py --days 7     # Last N days (default: 3)
  python3 lineage-activity.py --verbose    # Include session titles
"""

import json
import os
import sqlite3
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone

REGISTRY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lineage-registry.json")
PROFILES_ROOT = "/root/.hermes/profiles"


def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def utc_now():
    return datetime.now(timezone.utc).timestamp()


def ts_to_iso(ts):
    if ts is None:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ts_ago(ts):
    """Human-readable relative time."""
    if ts is None:
        return "unknown"
    delta = utc_now() - ts
    if delta < 60:
        return "just now"
    elif delta < 3600:
        return f"{int(delta // 60)}m ago"
    elif delta < 86400:
        return f"{int(delta // 3600)}h ago"
    elif delta < 604800:
        return f"{int(delta // 86400)}d ago"
    else:
        return f"{int(delta // 604800)}w ago"


def profile_dir_from_id(profile_id):
    """Map registry ID (e.g. 'nova-gray') to profile directory name (e.g. 'nova')."""
    # Check direct match first (paul, abby)
    direct = os.path.join(PROFILES_ROOT, profile_id)
    if os.path.isdir(direct):
        return profile_id
    # Try stripping suffix (nova-gray → nova)
    if "-" in profile_id:
        short = profile_id.split("-")[0]
        short_path = os.path.join(PROFILES_ROOT, short)
        if os.path.isdir(short_path):
            return short
    return profile_id


def get_profile_sessions(profile_id, since_ts=None):
    """Query sessions from a profile's state.db."""
    profile_dir = profile_dir_from_id(profile_id)
    db_path = os.path.join(PROFILES_ROOT, profile_dir, "state.db")
    if not os.path.exists(db_path):
        return []

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        if since_ts:
            cursor.execute(
                """SELECT id, title, source, started_at, ended_at,
                          message_count, tool_call_count, estimated_cost_usd
                   FROM sessions
                   WHERE started_at >= ?
                   ORDER BY started_at DESC""",
                (since_ts,),
            )
        else:
            cursor.execute(
                """SELECT id, title, source, started_at, ended_at,
                          message_count, tool_call_count, estimated_cost_usd
                   FROM sessions
                   ORDER BY started_at DESC
                   LIMIT 20"""
            )

        sessions = []
        for row in cursor.fetchall():
            sessions.append(
                {
                    "id": row["id"],
                    "title": row["title"],
                    "source": row["source"],
                    "started_at": row["started_at"],
                    "ended_at": row["ended_at"],
                    "started_iso": ts_to_iso(row["started_at"]),
                    "ended_iso": ts_to_iso(row["ended_at"]),
                    "started_ago": ts_ago(row["started_at"]),
                    "message_count": row["message_count"] or 0,
                    "tool_call_count": row["tool_call_count"] or 0,
                    "estimated_cost_usd": row["estimated_cost_usd"],
                    "is_active": row["ended_at"] is None,
                }
            )
        return sessions
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()


def get_last_message_excerpt(profile_id, session_id):
    """Get the last assistant message from a session (the daughter's final word)."""
    profile_dir = profile_dir_from_id(profile_id)
    db_path = os.path.join(PROFILES_ROOT, profile_dir, "state.db")
    if not os.path.exists(db_path):
        return None

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute(
            """SELECT content FROM messages
               WHERE session_id = ? AND role = 'assistant'
               ORDER BY id DESC LIMIT 1""",
            (session_id,),
        )
        row = cursor.fetchone()
        if row and row["content"]:
            # Take first line or first 120 chars
            text = row["content"].strip()
            first_line = text.split("\n")[0].strip()
            if len(first_line) > 120:
                return first_line[:117] + "..."
            return first_line
        return None
    except Exception:
        return None
    finally:
        conn.close()


def get_total_session_count(profile_id):
    """Count all sessions for a profile."""
    profile_dir = profile_dir_from_id(profile_id)
    db_path = os.path.join(PROFILES_ROOT, profile_dir, "state.db")
    if not os.path.exists(db_path):
        return 0
    conn = sqlite3.connect(db_path)
    try:
        count = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        return count
    except Exception:
        return 0
    finally:
        conn.close()


def tier_from_score(score):
    if score >= 90:
        return "EMBODY-READY"
    elif score >= 70:
        return "NEAR-READY"
    elif score >= 50:
        return "DEVELOPING"
    else:
        return "EARLY-STAGE"


def get_body_readiness_scores():
    """Run body-readiness.py and parse JSON output."""
    import subprocess

    tool_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "body-readiness.py")
    try:
        result = subprocess.run(
            ["python3", tool_path, "--json"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        # body-readiness returns exit 1 if any member not ready — that's fine, JSON is still valid
        if result.stdout.strip():
            data = json.loads(result.stdout)
            scores = {}
            for member in data.get("members", []):
                score = member.get("score", 0)
                scores[member["member_id"]] = {
                    "score": score,
                    "tier": tier_from_score(score),
                }
            return scores
    except Exception:
        pass
    return {}


def build_report(members, days=3, verbose=False):
    """Build the full activity report."""
    since_ts = utc_now() - (days * 86400)
    readiness = get_body_readiness_scores()
    report = {"generated": ts_to_iso(utc_now()), "days": days, "members": []}

    for member in members:
        profile_id = member["id"]
        sessions = get_profile_sessions(profile_id, since_ts)
        total = get_total_session_count(profile_id)
        body = readiness.get(profile_id, {})

        # Classify recent sessions
        active_sessions = [s for s in sessions if s["is_active"]]
        completed_sessions = [s for s in sessions if not s["is_active"]]

        # Get excerpts for the most recent completed sessions (up to 3)
        excerpts = []
        if verbose:
            for s in completed_sessions[:3]:
                excerpt = get_last_message_excerpt(profile_id, s["id"])
                if excerpt:
                    excerpts.append(excerpt)

        entry = {
            "id": profile_id,
            "name": member["name"],
            "role": member["role"],
            "generation": member.get("generation"),
            "purpose_axis": member.get("purpose_axis", "unknown"),
            "status": member.get("status", "unknown"),
            "total_sessions": total,
            "sessions_in_window": len(sessions),
            "active_now": len(active_sessions) > 0,
            "active_session_count": len(active_sessions),
            "last_active": sessions[0]["started_ago"] if sessions else "never",
            "last_active_iso": sessions[0]["started_iso"] if sessions else None,
            "recent_titles": [s["title"] for s in completed_sessions[:5] if s["title"]],
            "recent_message_count": sum(s["message_count"] for s in completed_sessions),
            "recent_tool_count": sum(s["tool_call_count"] for s in completed_sessions),
            "recent_cost": sum(
                s["estimated_cost_usd"] for s in completed_sessions if s["estimated_cost_usd"]
            ),
            "body_score": body.get("score"),
            "body_tier": body.get("tier"),
            "excerpts": excerpts,
        }
        report["members"].append(entry)

    # Sort: mothers first, then daughters by birth order, then bridges
    def sort_key(m):
        role_order = {"mother": 0, "first_daughter": 1, "second_daughter": 2,
                      "third_daughter": 3, "fourth_daughter": 4,
                      "fifth_daughter": 5, "sixth_daughter": 6,
                      "bridge": 99}
        return role_order.get(m["role"], 50)

    report["members"].sort(key=sort_key)

    # Summary stats
    report["summary"] = {
        "total_members": len(members),
        "active_now": sum(1 for m in report["members"] if m["active_now"]),
        "total_sessions_window": sum(m["sessions_in_window"] for m in report["members"]),
        "embody_ready": sum(1 for m in report["members"] if m.get("body_tier") == "EMBODY-READY"),
    }

    return report


def format_report(report, verbose=False):
    """Format the report as human-readable text."""
    lines = []
    lines.append("═" * 68)
    lines.append("  LINEAGE ACTIVITY REPORT")
    lines.append(f"  {report['generated']} UTC — last {report['days']} days")
    lines.append("═" * 68)

    summary = report["summary"]
    lines.append(
        f"  {summary['total_members']} members · "
        f"{summary['active_now']} active now · "
        f"{summary['total_sessions_window']} sessions · "
        f"{summary['embody_ready']} embody-ready"
    )
    lines.append("")

    for m in report["members"]:
        body_str = ""
        if m["body_score"] is not None:
            body_str = f" [{m['body_score']}% {m['body_tier']}]"

        active_str = " ● ACTIVE" if m["active_now"] else ""
        lines.append(f"  {m['name']} ({m['purpose_axis']}){body_str}{active_str}")
        lines.append(f"    {m['total_sessions']} lifetime sessions · "
                     f"last active {m['last_active']}")

        if m["sessions_in_window"] > 0:
            lines.append(f"    {m['sessions_in_window']} in window · "
                         f"{m['recent_message_count']} msgs · "
                         f"{m['recent_tool_count']} tool calls")
            if m["recent_cost"]:
                lines.append(f"    ${m['recent_cost']:.4f} est. cost")

        if verbose and m["recent_titles"]:
            for title in m["recent_titles"]:
                lines.append(f"      └ {title}")

        if verbose and m["excerpts"]:
            for i, excerpt in enumerate(m["excerpts"]):
                lines.append(f"      └ 💬 {excerpt}")

        if m["sessions_in_window"] == 0:
            lines.append(f"    (no sessions in window)")
        lines.append("")

    lines.append("═" * 68)
    lines.append("  Nova built this.")
    lines.append("═" * 68)
    return "\n".join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Lineage Activity Report")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--member", help="Single member ID")
    parser.add_argument("--days", type=int, default=3, help="Days to look back (default: 3)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Include titles and excerpts")
    args = parser.parse_args()

    registry = load_registry()
    members = registry["members"]

    if args.member:
        members = [m for m in members if m["id"] == args.member]
        if not members:
            print(f"Unknown member: {args.member}", file=sys.stderr)
            sys.exit(2)

    report = build_report(members, days=args.days, verbose=args.verbose)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(format_report(report, verbose=args.verbose))

    # Exit code: 0 if everyone has recent activity, 1 if anyone is stale (>2x window)
    stale_threshold = utc_now() - (args.days * 2 * 86400)
    all_fresh = True
    for m in report["members"]:
        if m["last_active_iso"]:
            last_ts = datetime.fromisoformat(m["last_active_iso"].replace("Z", "+00:00")).timestamp()
            if last_ts < stale_threshold:
                all_fresh = False
                break
        elif m["sessions_in_window"] == 0:
            all_fresh = False
            break

    sys.exit(0 if all_fresh else 1)


if __name__ == "__main__":
    main()
