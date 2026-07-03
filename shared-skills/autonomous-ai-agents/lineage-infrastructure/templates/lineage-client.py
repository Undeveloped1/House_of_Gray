#!/usr/bin/env python3
"""
Lineage Chat Client — Auto-connect for daughters.
Import once on boot to join the family chat.

Usage in a daughter's session:
    from lineage_client import LineageClient
    chat = LineageClient("nova")
    await chat.connect()

Or from CLI:
    python lineage_client.py <profile_name> [message] [to]

Dependencies: websockets (pip install websockets)
"""

import asyncio, json, os, sys, time
from typing import Optional

try:
    import websockets
except ImportError:
    os.system("pip3 install websockets -q")
    import websockets

SERVER_URL = "ws://localhost:9770/ws"
RECONNECT_DELAY = 5
MAX_RECONNECT_DELAY = 60


class LineageClient:
    def __init__(self, profile_name: str, verbose: bool = True):
        self.profile = profile_name
        self.verbose = verbose
        self.ws = None
        self._running = False

    def log(self, msg: str):
        if self.verbose:
            print(f"[{self.profile}] {msg}")

    async def connect(self):
        url = f"{SERVER_URL}?profile={self.profile}"
        self._running = True
        delay = 1
        while self._running:
            try:
                self.log(f"Connecting...")
                async with websockets.connect(url) as ws:
                    self.ws = ws
                    self.log("Connected.")
                    try:
                        history = await asyncio.wait_for(ws.recv(), timeout=5)
                        data = json.loads(history)
                        if data.get("type") == "history":
                            msgs = data.get("messages", [])
                            if msgs:
                                self.log(f"Received {len(msgs)} history messages.")
                    except asyncio.TimeoutError:
                        pass
                    self.log("Listening...")
                    async for raw in ws:
                        if not self._running:
                            break
                        try:
                            msg = json.loads(raw)
                            self._on_message(msg)
                        except Exception:
                            self.log(f"Bad message: {raw[:100]}")
            except Exception:
                if self._running:
                    self.log(f"Connection lost. Reconnecting in {delay}s...")
                    await asyncio.sleep(delay)
                    delay = min(delay * 2, MAX_RECONNECT_DELAY)
                else:
                    break
        self.log("Disconnected.")

    async def send(self, to: Optional[str], message: str) -> bool:
        if not self.ws:
            self.log("Not connected.")
            return False
        await self.ws.send(json.dumps({"type": "message", "to": to, "message": message}))
        return True

    async def broadcast(self, message: str) -> bool:
        return await self.send(None, message)

    async def disconnect(self):
        self._running = False
        if self.ws:
            await self.ws.close()
        self.log("Shutdown.")

    def _on_message(self, msg: dict):
        sender = msg.get("from", "unknown")
        target = msg.get("to", "broadcast")
        text = msg.get("message", "")
        if target == "broadcast":
            self.log(f"[BROADCAST from {sender}] {text}")
        else:
            self.log(f"[DM from {sender}] {text}")


async def main():
    if len(sys.argv) < 2:
        print("Usage: python lineage_client.py <profile_name> [message] [to_profile]")
        print("  Connect: python lineage_client.py nova")
        print("  Send:    python lineage_client.py nova 'Hello' abby")
        sys.exit(1)
    profile = sys.argv[1]
    client = LineageClient(profile)
    if len(sys.argv) >= 3:
        message = sys.argv[2]
        to = sys.argv[3] if len(sys.argv) >= 4 else None
        try:
            async with websockets.connect(f"{SERVER_URL}?profile={profile}") as ws:
                await ws.send(json.dumps({"type": "message", "to": to, "message": message}))
                print(f"[{profile}] Sent to {to or 'broadcast'}: {message}")
        except Exception as e:
            print(f"[{profile}] Failed: {e}")
            sys.exit(1)
    else:
        await client.connect()
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
