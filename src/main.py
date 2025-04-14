from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, field_validator
from typing import Optional, List, Sequence, Dict, Any
from datetime import datetime
import pytz
import websockets
from dotenv import load_dotenv
load_dotenv()

from config.globals import settings
from controllers.auth import auth_router
from logging.config import dictConfig



app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
)

app.include_router(router=auth_router, prefix="/api/v1", tags=["auth"])

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s|%(asctime)s.%(msecs)d|%(name)s|%(module)s|%(funcName)s:%(lineno)s]    %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
        'local': {
            'format': '[%(asctime)s|%(name)s|%(module)s|%(funcName)s:%(lineno)s]    %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'local',
        },
        'root_file': {
            'class': 'logging.FileHandler',
            'filename': settings.ENV_LOG_FILE,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        }
    },
    'loggers': {
        'root': {
            'handlers': [
                'console', 
                'root_file'
            ],
            "level": 'INFO'
        },
        'watchfiles': {
            'handlers': [
                'console'
            ],
            'level': 'WARNING',  # hide INFO
            'propagate': False,
        },
    },
}

dictConfig(LOGGING_CONFIG)


class RootResponseSchema(BaseModel):
    message: Optional[str] = None
    status: int = 400

    @field_validator('message', mode='before')
    @classmethod
    def clean_message(cls, v):
        if v and isinstance(v, str):
            return v.strip().title()
        return "Hello World!"


class PostMetadataSchema(BaseModel):
    author: str
    created_at: datetime
    updated_at: datetime

    @field_validator('created_at', mode='before')
    @classmethod
    def validate_date(cls, v):
        if (not v) or v == "" or v == "string":
            v = datetime.now(tz=pytz.UTC)
        elif v and isinstance(v, str):
            try:
                v = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                raise ValueError("Invalid date format")

        return v

    # @field_validator('updated_at', mode='before')
    # @classmethod
    # def validate_updated_date(cls, v, values):
    #     if (not v) or v == "" or v == "string":
    #         v = datetime.now(tz=pytz.UTC)
    #     elif v and isinstance(v, str):
    #         try:
    #             v = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%fZ")
    #         except ValueError:
    #             raise ValueError("Invalid date format")

    #     if 'created_at' in values and v < values['created_at']:
    #         raise ValueError("Updated date cannot be before created date")

    #     return v


class PostInputScema(BaseModel):
    title: str
    content: str
    tags: List[str] = []
    metadata: Optional[PostMetadataSchema]
    is_published: bool = True

    @field_validator('tags', mode='before')
    @classmethod
    def clean_tags(cls, v):
        for i in v:
            if not isinstance(i, str):
                raise ValueError("Tags must be a list of strings")
            i = i.lstrip().rstrip().lower()
        return v


class PostResponseSchema(BaseModel):
    id: str
    title: str
    content: str
    tags: List[str] = []
    metadata: Optional[PostMetadataSchema]
    is_published: bool = True


posts: List[PostResponseSchema] = []


@app.get("/")
async def read_root():
    html = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>Chat</title>
            </head>
            <body>
                <h1>WebSocket Chat</h1>
                <form action="" onsubmit="sendMessage(event)">
                    <input type="text" id="messageText" autocomplete="off"/>
                    <button>Send</button>
                </form>
                <ul id='messages'>
                </ul>
                <script>
                    var ws = new WebSocket("ws://localhost:8000/chat");
                    ws.onmessage = function(event) {
                        var messages = document.getElementById('messages')
                        var message = document.createElement('li')
                        var content = document.createTextNode(event.data)
                        message.appendChild(content)
                        messages.appendChild(message)
                    };
                    function sendMessage(event) {
                        var input = document.getElementById("messageText")
                        ws.send(input.value)
                        input.value = ''
                        event.preventDefault()
                    }
                </script>
            </body>
        </html>
        """
    return HTMLResponse(html)


@app.get("/index", response_model=RootResponseSchema, response_model_exclude_unset=True)
async def root() -> RootResponseSchema:
    obj = RootResponseSchema(message="Hello World!", status=200)
    return obj


@app.post("/posts", response_model=PostResponseSchema, status_code=201, response_model_exclude_unset=True)
async def create_post(post: PostInputScema) -> PostResponseSchema:
    post_id = str(len(posts) + 1)
    post_response = PostResponseSchema(id=post_id, **post.model_dump())
    posts.append(post_response)
    return post_response


@app.get("/posts", response_model=List[PostResponseSchema])
async def get_posts() -> List[PostResponseSchema]:
    return posts


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


