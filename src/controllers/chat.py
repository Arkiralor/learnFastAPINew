from os import path

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from config.globals import settings
from utils.ws_manager import connection_manager
from controllers import logger

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)


@chat_router.websocket("/chat/{client_id}/")
async def websocket_chat(websocket: WebSocket, client_id):
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.send_personal_message(f"You wrote: {data}", websocket)
            await connection_manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        await connection_manager.broadcast(f"Client #{client_id} left the chat")


@chat_router.get("/get/chat/")
async def get_channel():
    """
    Get chat channel by ID.
    """
    file_path = path.join(
        settings.BASE_DIR, "controllers", "html", "chat.html")
    with open(file=file_path, mode="r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
