from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import pytz
from bson import ObjectId

from constants import FormatRegex

class User(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(...)
    password: str = Field(..., min_length=8)
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=pytz.UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=pytz.UTC))
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    last_login: Optional[datetime] = Field(default=None)
    login_attempts: int = Field(default=0)

    class Config:
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed=True
        json_schema_extra = {
            "example": {
                "username": "arkiralor",
                "email": "fablelordarkalon11235@gmail.com",
                "created_at": datetime.now(tz=pytz.UTC),
                "updated_at": datetime.now(tz=pytz.UTC)
            }
        }

class TokenBlacklist(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    token: str = Field(...)
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=pytz.UTC))
    expires_at: datetime = Field(default_factory=lambda: datetime.now(tz=pytz.UTC))

    class Config:
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed=True
        json_schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "user_id": ObjectId("605c72f8e3b0d4f7f8f8d4e2"),
                "created_at": datetime.now(tz=pytz.UTC),
                "expires_at": datetime.now(tz=pytz.UTC)
            }
        }