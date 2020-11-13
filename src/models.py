from datetime import datetime, timezone
from typing import Optional

from fastapi import Path
from pydantic import BaseModel, Field

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
    server_timestamp: datetime = datetime.now(timezone.utc)
    client_timestamp: datetime
    event_type: str
    event_body: dict
