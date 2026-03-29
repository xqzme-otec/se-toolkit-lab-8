import asyncio
import json
import websockets

async def handler(websocket):
    async for message in websocket:
        try:
            data = json.loads(message)
            response = {"content": f"Echo: {data.get('content', '')}"}
            await websocket.send(json.dumps(response))
        except:
            await websocket.send(json.dumps({"content": "Hello from LMS Bot!"}))

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server running on port 8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
