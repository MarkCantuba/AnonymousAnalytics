from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

class NewDoc(BaseModel):
    content: str


class Project(BaseModel):
    id: str = Field(max_length=300, regex="^[0-9a-z]+[0-9a-z\.\-_]*$")
    name: str
    description: Optional[str] = Field(
        None, title="The description of the project", max_length=300
    )


class Event(BaseModel):
    server_timestamp: datetime = datetime.now(timezone.utc)
    event: dict