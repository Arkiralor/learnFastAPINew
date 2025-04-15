from pydantic import BaseModel, Field
from bson import ObjectId

from typing import Optional, List
from datetime import datetime
import pytz
from config.boilerplate import PydanticObjectId


class UserRegisterSchema(BaseModel):
    username: str
    email: str
    password: str

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
    access: str
    refresh: str