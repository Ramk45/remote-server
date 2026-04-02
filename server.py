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
            for cid, ws in list(connected_clients.items()):
                if cid != client_id:
                    try:
                        await ws.send(message)
                    except:
                        pass
    except Exception as e:
        print("Error: " + str(e))
    finally:
        if client_id in connected_clients:
            del connected_clients[client_id]
        print("Disconnected: " + client_id)

async def main():
    port = int(os.environ.get("PORT", 8765))
    async with websockets.serve(
        handler,
        "0.0.0.0",
        port,
        ping_interval=None
    ):
        print("Server Started on port " + str(port))
        await asyncio.Future()

asyncio.run(main())
