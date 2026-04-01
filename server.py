import asyncio
import websockets
import os

connected_clients = {}

async def handler(websocket):
    path = websocket.request.path
    client_id = path.strip("/")
    connected_clients[client_id] = websocket
    print("Connected: " + client_id)
    try:
        async for message in websocket:
            for cid, ws in connected_clients.items():
                if cid != client_id:
                    await ws.send(message)
    except:
        pass
    finally:
        if client_id in connected_clients:
            del connected_clients[client_id]
        print("Disconnected: " + client_id)

async def main():
    port = int(os.environ.get("PORT", 8765))
    async with websockets.serve(handler, "0.0.0.0", port):
        print("Server Started on port " + str(port))
        await asyncio.Future()

asyncio.run(main())
