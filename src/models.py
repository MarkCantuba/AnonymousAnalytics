from datetime import datetime, timezone
from typing import Optional

from fastapi import Path
from pydantic import BaseModel, Field, validator

ProjectId = Path(..., max_length=50, regex=r"^[0-9a-z]+[0-9a-z\.\-_]*$")


class NewDoc(BaseModel):
    content: str


class Project(BaseModel):
    id: str = Field(max_length=50, regex=r"^[0-9a-z]+[0-9a-z\.\-_]*$")
    name: str
    description: Optional[str] = Field(
        None, title="The description of the project"
    )


class Event(BaseModel):
    server_timestamp: datetime = None
    client_timestamp: datetime
    event_type: str
    event_body: dict

    @validator('server_timestamp', pre=True, always=True)
    def set_ts_now(cls, v):
        return v or datetime.now(timezone.utc)
