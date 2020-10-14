from typing import Optional

from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI

import config

from models import *
from exceptions import *
from modules.project.project import query_event_by_timestamp

conf = config.get()
app = FastAPI()
es = AsyncElasticsearch([
    {
        "host": conf["elasticsearch"]["private_ip"],
        "port": conf["elasticsearch"]["rest_port"]
    }
])


@app.post("/projects")
async def post_project(project: Project):
    if await es.indices.exists(index=project.project_name):
        raise ElasticIndexExists(project.project_name)

    return await es.indices.create(project.project_name, dict())


@app.post("/projects/{project_name}/events")
async def post_event_to_project(project_name: str, event: Event):
    if not await es.indices.exists(index=project_name):
        raise ElasticIndexNotFound(project_name)

    return await es.index(project_name, event.json())


@app.get("/projects/{project_name}/events")
async def get_events_by_timestamp(project_name: str, start: Optional[datetime] = None, end: Optional[datetime] = None):
    if not await es.indices.exists(index=project_name):
        raise ElasticIndexNotFound(project_name)

    return await query_event_by_timestamp(es, project_name, start, end)
