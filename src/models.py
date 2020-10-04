from pydantic import BaseModel
import datetime as dt


class NewDoc(BaseModel):
    content: str

class Project(BaseModel):
    project_name: str

class Event(BaseModel):
    event_id: str
    timestamp : dt.datetime
    parameters: dict = {}
