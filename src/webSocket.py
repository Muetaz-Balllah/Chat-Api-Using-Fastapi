from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

ws_router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    await manager.broadcast(f"Connected From The Server ***")

    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            # هنا يمكنك تنفيذ العملية المطلوبة بناءً على محتوى الرسالة
            # مثلاً: if data == "1": قم بتنفيذ إجراء معين
            await manager.broadcast(f"from servier {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
