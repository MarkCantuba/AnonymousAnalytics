from pydantic import BaseModel
from datetime import datetime, timezone

class NewDoc(BaseModel):
    content: str


class Project(BaseModel):
    id: str
    name: str
    description: str


class Event(BaseModel):
    server_timestamp: datetime = datetime.now(timezone.utc)
    event: dict