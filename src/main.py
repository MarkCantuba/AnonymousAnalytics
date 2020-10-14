from datetime import timedelta
from typing import Optional

from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, Query

import config

from models import *
from exceptions import *
from project.project import query_event_by_timestamp

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
async def post_event_to_project(project_name: str, event: dict):
    if not await es.indices.exists(index=project_name):
        raise ElasticIndexNotFound(project_name)

    new_event = Event(event=event)

    return await es.index(project_name, new_event.json())


@app.get("/projects/{project_name}/events")
async def get_events_by_timestamp(project_name: str,
                                  start: Optional[datetime] = Query(datetime.now(timezone.utc) - timedelta(days=7)),
                                  end: Optional[datetime] = Query(datetime.now(timezone.utc))):
    if not await es.indices.exists(index=project_name):
        raise ElasticIndexNotFound(project_name)

    return await query_event_by_timestamp(es, project_name, start, end)
