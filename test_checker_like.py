#!/usr/bin/env python3
import asyncio, json, sys, websockets

WS_URI = "ws://localhost:42002/ws/chat"
ACCESS_KEY = "nanobot-secret-2024"
TIMEOUT = 30

async def test():
    uri = f"{WS_URI}?access_key={ACCESS_KEY}"
    print(f"Connecting to {uri}")
    try:
        async with websockets.connect(uri, ping_interval=None, open_timeout=10) as ws:
            print("Connected!")

            # Test 1: Create health check
            msg1 = "Create a не работает ❌

**1. Cron health health check that runs every 15 minutes. Each run should check for backend errors and post a summary here."
            await ws.send(json.dumps({"content": msg1}))
            resp1 = await asyncio.wait_for(ws.recv(), timeout=TIMEOUT)
            print(f"Create response: {resp1[:300]}")

            # Test 2: List scheduled jobs
            msg2 = "List scheduled jobs."
            await ws.send(json.dumps({"content": msg2}))
            resp2 = await asyncio.wait_for(ws.recv(), timeout=TIMEOUT)
            print(f"List response: {resp2[:300]}")

            # Check keywords
            kw1 = ["scheduled", "health", "check", "15", "cron", "minute", "job", "id"]
            kw2 = ["health-check", "*/15", "scheduled", "job", "id", "cron"]

            ok1 = any(k.lower() in resp1.lower() for k in kw1)
            ok2 = any(k.lower() in resp2.lower() for k in kw2)

            print(f"Create check: {'PASS' if ok1 else 'FAIL'}")
            print(f"List check: {'PASS' if ok2 else 'FAIL'}")
            return ok1 and ok2

    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test())
    sys.exit(0 if result else 1)
