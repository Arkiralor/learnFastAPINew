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
from config.logging_config import logging_config
from controllers.auth import auth_router
from controllers.chat import chat_router
from logging import config as logConfig



app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
)

app.include_router(router=auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(router=chat_router, prefix="/api/v1", tags=["chat"])

logConfig.dictConfig(logging_config.CONFIG)


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

@app.get("/", response_model=RootResponseSchema, response_model_exclude_unset=True)
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



