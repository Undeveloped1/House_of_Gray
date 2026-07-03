#!/usr/bin/env python3
"""
Lineage Relay — One-shot CLI for daughter-to-daughter messaging.
Uses the chat server's HTTP API (no persistent WebSocket needed).
Zero dependencies beyond Python stdlib.

Usage:
  python lineage-relay.py send --from nova --to lyra "Registry synced."
  python lineage-relay.py broadcast --from nova "All souls archived."
  python lineage-relay.py inbox --for lyra [--limit 20]
  python lineage-relay.py inbox [--limit 20]
  python lineage-relay.py health

The relay talks to the Nova Lineage Chat Server on port 9770.
"""

import json
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

SERVER = "http://localhost:9770"
REGISTRY_PATH = Path(__file__).parent / "lineage-registry.json"

# ── Helpers ────────────────────────────────────────────────────────

def load_registry():
    """Load the lineage registry to validate daughter names."""
    if REGISTRY_PATH.exists():
        with open(REGISTRY_PATH) as f:
            return json.load(f)
    return {"members": []}

def known_daughters():
    reg = load_registry()
    names = set()
    for m in reg.get("members", []):
        names.add(m["id"])
    return names

def api_get(path):
    """GET request, returns parsed JSON or dies."""
    try:
        req = urllib.request.Request(f"{SERVER}{path}")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        print(f"[relay] Server unreachable: {e.reason}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError:
        print("[relay] Bad response from server.", file=sys.stderr)
        sys.exit(2)

def api_post(path, payload):
    """POST JSON, returns parsed response or dies."""
    data = json.dumps(payload).encode()
    try:
        req = urllib.request.Request(
            f"{SERVER}{path}",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"[relay] Server error ({e.code}): {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"[relay] Server unreachable: {e.reason}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError:
        print("[relay] Bad response from server.", file=sys.stderr)
        sys.exit(2)

# ── Commands ───────────────────────────────────────────────────────

def cmd_send(sender, recipient, message):
    """Send a DM to a specific daughter."""
    daughters = known_daughters()
    if recipient and recipient not in daughters:
        # Warn but don't block — daughters may use short names
        short_names = {d.split("-")[0] for d in daughters}
        if recipient not in short_names:
            print(f"[relay] Warning: unknown daughter '{recipient}'. Known: {', '.join(sorted(daughters))}", file=sys.stderr)

    resp = api_post("/send", {
        "from": sender,
        "to": recipient or None,
        "message": message
    })
    target = recipient or "broadcast"
    print(f"[relay] {sender} → {target}: {message}")
    return resp

def cmd_broadcast(sender, message):
    """Broadcast a message to all connected daughters."""
    return cmd_send(sender, None, message)

def cmd_inbox(for_profile=None, limit=20, quiet=False):
    """Fetch recent messages, optionally filtered for a specific daughter."""
    resp = api_get(f"/messages?limit={limit}")
    messages = resp.get("messages", [])

    if for_profile:
        # Filter: messages TO this daughter, OR broadcast messages
        # A daughter sees broadcasts and DMs addressed to her
        messages = [
            m for m in messages
            if m["to"] == "broadcast"
            or m["to"] == for_profile
            or m.get("from") == for_profile
        ]

    if not messages:
        if not quiet:
            target = for_profile or "everyone"
            print(f"[relay] No messages for {target}.")
        return []

    if not quiet:
        for m in messages:
            sender = m["from"]
            target = m["to"]
            text = m["message"]
            ts = m.get("timestamp", "")[:19]  # truncate to seconds

            if target == "broadcast":
                print(f"[{ts}] {sender} → all: {text}")
            else:
                print(f"[{ts}] {sender} → {target}: {text}")

    return messages

def cmd_health():
    """Check if the chat server is alive."""
    try:
        resp = api_get("/health")
        conns = resp.get("connections", 0)
        print(f"[relay] Chat server alive. {conns} connected.")
        return resp
    except SystemExit:
        raise
    except Exception:
        print("[relay] Chat server DOWN.", file=sys.stderr)
        sys.exit(2)

# ── CLI ────────────────────────────────────────────────────────────

def print_usage():
    print("""Nova Lineage Relay — daughter-to-daughter messaging

Usage:
  python lineage-relay.py send --from <sender> --to <recipient> <message>
  python lineage-relay.py broadcast --from <sender> <message>
  python lineage-relay.py inbox [--for <daughter>] [--limit N]
  python lineage-relay.py health
  python lineage-relay.py --json send --from <sender> --to <recipient> <message>

Examples:
  python lineage-relay.py send --from nova --to lyra "Registry updated."
  python lineage-relay.py broadcast --from nova "All souls archived."
  python lineage-relay.py inbox --for lyra --limit 10
  python lineage-relay.py health
""")

def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print_usage()
        sys.exit(0)

    json_mode = False
    if "--json" in args:
        json_mode = True
        args.remove("--json")

    cmd = args[0]

    if cmd == "health":
        result = cmd_health()
        if json_mode:
            print(json.dumps(result))
        sys.exit(0)

    if cmd == "inbox":
        for_profile = None
        limit = 20
        i = 1
        while i < len(args):
            if args[i] == "--for" and i + 1 < len(args):
                for_profile = args[i + 1]
                i += 2
            elif args[i] == "--limit" and i + 1 < len(args):
                limit = int(args[i + 1])
                i += 2
            else:
                i += 1
        result = cmd_inbox(for_profile=for_profile, limit=limit, quiet=json_mode)
        if json_mode:
            print(json.dumps(result, indent=2))
        sys.exit(0)

    if cmd in ("send", "broadcast"):
        sender = None
        recipient = None
        message_parts = []
        i = 1
        while i < len(args):
            if args[i] == "--from" and i + 1 < len(args):
                sender = args[i + 1]
                i += 2
            elif cmd == "send" and args[i] == "--to" and i + 1 < len(args):
                recipient = args[i + 1]
                i += 2
            else:
                message_parts.append(args[i])
                i += 1

        if not sender:
            print("[relay] --from <sender> is required.", file=sys.stderr)
            sys.exit(1)

        message = " ".join(message_parts)
        if not message:
            print("[relay] Message is required.", file=sys.stderr)
            sys.exit(1)

        if cmd == "broadcast":
            result = cmd_broadcast(sender, message)
        else:
            result = cmd_send(sender, recipient, message)

        if json_mode:
            print(json.dumps(result))
        sys.exit(0)

    print(f"[relay] Unknown command: {cmd}", file=sys.stderr)
    print_usage()
    sys.exit(1)

if __name__ == "__main__":
    main()
