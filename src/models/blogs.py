from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import pytz
from bson import ObjectId

from models.auth import User

class BlogPost(BaseModel):
    id: Optional[ObjectId]
    author: ObjectId
    title: str
    content: str
    tags: List[ObjectId]
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            ObjectId: str
        }
        validate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "title": "My First Blog Post",
                "content": "This is the content of my first blog post.",
                "tags": ["fastapi", "mongodb", "python"],
                "created_at": datetime.now(tz=pytz.UTC),
                "updated_at": datetime.now(tz=pytz.UTC)
            }
        }

class Tag(BaseModel):
    id: Optional[ObjectId]
    name: str

    class Config:
        json_encoders = {
            ObjectId: str
        }
        validate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "name": "fastapi",
            }
        }


class Comment(BaseModel):
    id: Optional[ObjectId]
    post: ObjectId
    author: ObjectId
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            ObjectId: str
        }
        validate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "content": "This is a comment.",
                "created_at": datetime.now(tz=pytz.UTC),
                "updated_at": datetime.now(tz=pytz.UTC)
            }
        }