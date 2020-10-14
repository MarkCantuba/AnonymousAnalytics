from pydantic import BaseModel
from datetime import datetime, timezone

class NewDoc(BaseModel):
    content: str


class Project(BaseModel):
    project_name: str


class Event(BaseModel):
    server_timestamp: datetime = datetime.now(timezone.utc)
    event: dict