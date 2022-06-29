from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseConfig, BaseModel, Field, validator

class WikiModel(BaseModel):
    class Config(BaseConfig):
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
                .isoformat()
                .replace("+00:00", "Z")
        }

class TimestampsModelMixin(BaseModel):
    created_at: datetime = None
    updated_at: datetime = None

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime):
        return value or datetime.now()

class WikiModelMixin(TimestampsModelMixin):
    id: Optional[int] = None
