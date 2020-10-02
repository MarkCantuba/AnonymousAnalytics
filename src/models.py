from pydantic import BaseModel
from datetime import datetime


class NewDoc(BaseModel):
    content: str

#TODO: The Time and Date are currently in string format. We need to process this when getting ranges on get request!
class Event(BaseModel):
    Event_ID: str
    Time: str = datetime.now().strftime("%H:%M:%S")
    Date: str = str(datetime.now().date())
    Params: dict
