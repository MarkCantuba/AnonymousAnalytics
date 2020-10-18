from datetime import timedelta
from typing import Optional

from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, Query

import config

import re

from migration import *
from models import *
from exceptions import *
from project.project import *

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


@app.post("/projects", status_code=201)
async def post_project(project: Project):
    # validate project_id
    if await es.exists(index=".projects", id=project.id):
        raise ElasticIndexExists(project.id)

    doc = project.dict()

    # add doc to .project
    await es.create(index='.projects',
                    id=project.id,
                    refresh=True, # refresh the .projects index after creating the doc, so it is immediately searchable
                    body=doc)
    # create index
    await es.indices.create(project.id)
    return project.dict()

@app.post("/projects/{project_id}/events")
async def post_event_to_project(project_id: str, event: dict):
    if not await es.indices.exists(index=project_id):
        raise ElasticIndexNotFound(project_id)

    new_event = Event(event=event)

    return await es.index(project_id, new_event.json())


@app.get("/projects/{project_id}/events")
async def get_events_by_timestamp(project_id: str,
                                  start: Optional[datetime] = Query(datetime.now(timezone.utc) - timedelta(days=7)),
                                  end: Optional[datetime] = Query(datetime.now(timezone.utc))):
    if not await es.indices.exists(index=project_id):
        raise ElasticIndexNotFound(project_id)

    return await query_event_by_timestamp(es, project_id, start, end)
