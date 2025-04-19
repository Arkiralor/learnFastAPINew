from pydantic import BaseModel, Field
from bson import ObjectId

from typing import Optional, List
from datetime import datetime
import pytz
from config.boilerplate import PydanticObjectId, TemplateSchema


class UserRegisterSchema(BaseModel):
    username: str
    email: str
    password: str

class UserGenericInfoSchema(TemplateSchema):
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    last_login: Optional[datetime]

    class Config:
        json_encoders = {
            str: str,
            ObjectId: str,
            PydanticObjectId: str
        }
        validate_by_name = True
        arbitrary_types_allowed = True

class UserRegisterOutputSchema(BaseModel):
    id: Optional[PydanticObjectId] = Field(...,alias="_id")
    username: str
    email: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_superuser: bool
    last_login: Optional[datetime]
    login_attempts: int

    class Config:
        json_encoders = {
            str: str,
            ObjectId: str
        }
        validate_by_name = True
        arbitrary_types_allowed = True

class UserPasswordLoginSchema(BaseModel):
    email: str
    password: str

class AuthTokenSchema(BaseModel):
    user: UserGenericInfoSchema
    access: str
    refresh: str

class TokenBlacklistSchema(BaseModel):
    id: Optional[PydanticObjectId] = Field(...,alias="_id")
    token: str
    created_at: datetime
    expires_at: datetime

    class Config:
        json_encoders = {
            str: str,
            ObjectId: str,
            PydanticObjectId: str
        }
        validate_by_name = True
        arbitrary_types_allowed = True