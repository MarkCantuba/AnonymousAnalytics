from pydantic import BaseModel


class NewDoc(BaseModel):
    content: str


class Project(BaseModel):
    project_name: str
