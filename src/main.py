from datetime import timedelta
from typing import Optional

from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, Query

import config

import re

from models import *
from exceptions import *
from project.project import query_event_by_timestamp

conf = config.get()
app = FastAPI()

if conf["enable_cors"]:
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"],
        expose_headers=["*"]
    )

es = AsyncElasticsearch([
    {
        "host": conf["elasticsearch"]["private_ip"],
        "port": conf["elasticsearch"]["rest_port"]
    }
])


@app.post("/projects")
async def post_project(project: Project):
    # validate project_id
    pattern = '^[0-9a-z]+[0-9a-z\.\-_]*$'
    id_pass = re.match(pattern, project.id)
    if not id_pass:
        raise InvalidProjectID(project.id)
    if await es.indices.exists(index=project.id):
        raise ElasticIndexExists(project.id)

    doc = {"id" : project.id,
        "name": project.name,
        "description": project.description}
    
    # add doc to .project
    await es.create( index= '.projects', id = project.id, body = doc)
    # create index
    return await es.indices.create(project.id, dict())

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
