from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from controllers import logger

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)

@chat_router.websocket("/chat/{channel_id}/").on_connect
async def websocket_chat(websocket: WebSocket, channel_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        logger.info(f"Client disconnected from channel {channel_id}")

@chat_router.get("/chat/{channel_id}/")
async def get_channel(channel_id: str):
    """
    Get chat channel by ID.
    """
    with open("html/chat.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
