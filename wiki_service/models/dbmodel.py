from datetime import datetime, timezone
from lib2to3.pytree import Base
from typing import Optional

from bson.objectid import ObjectId
from bson.errors import InvalidId

import pydantic
from pydantic import BaseConfig, BaseModel, Field, validator

class MongoOID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError('Not a valid ObjectId')

class WikiModel(BaseModel):
    class Config(BaseConfig):
        json_encoders = {
            ObjectId: lambda oid: str(oid),
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
                .isoformat()
                .replace("+00:00", "Z")
        }

pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

class TimestampsModelMixin(BaseModel):
    created_at: datetime = None
    updated_at: datetime = None

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime):
        return value or datetime.now()

class WikiModelMixin(TimestampsModelMixin):
    id: Optional[MongoOID] = Field(None, alias="_id")
    class Config(BaseConfig):
        fields = {'id': '_id'}
