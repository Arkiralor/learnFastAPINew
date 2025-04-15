from pydantic import BaseModel, Field, GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from bson import ObjectId

from typing import Optional, List, Sequence, Dict, Any
from datetime import datetime
import pytz


class TemplateModel(BaseModel):
    """
    Template model for all models in the application.
    """
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=pytz.UTC))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=pytz.UTC))

    class Config:
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "created_at": datetime.now(tz=pytz.UTC),
                "updated_at": datetime.now(tz=pytz.UTC)
            }
        }

    def model_dump(self, *args, **kwargs):
        return super(TemplateModel, self).model_dump(by_alias=True, *args, **kwargs)


class PydanticObjectId(ObjectId):
    """
    Custom Pydantic ObjectId type for MongoDB.
    This class extends the ObjectId class from the bson module and provides
    custom validation and JSON schema generation for Pydantic models.
    It is used to represent MongoDB ObjectId values in Pydantic models.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        return {"type": "string", "format": "objectid"}


class TemplateSchema(BaseModel):
    """
    Template schema for all schemas in the application.
    """
    id: Optional[PydanticObjectId] = Field(...,alias="_id")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=pytz.UTC))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=pytz.UTC))

    class Config:
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "created_at": datetime.now(tz=pytz.UTC),
                "updated_at": datetime.now(tz=pytz.UTC)
            }
        }
