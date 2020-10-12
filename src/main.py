from datetime import datetime, timezone
from typing import Dict

from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI

import config
from exceptions import *
from models import *

conf = config.get()
app = FastAPI()
es = AsyncElasticsearch([
    {
        'host': conf['elasticsearch']['private_ip'],
        'port': conf['elasticsearch']['rest_port']
    }
])


@app.post("/projects")
async def post_project(project: Project):
    if await es.indices.exists(index=project.project_name):
        raise ElasticIndexExists(project.project_name)

    try:
        return await es.indices.create(project.project_name, dict())
    except Exception as e:
        raise ElasticInternalError() from e


@app.post("/projects/{project_name}/events")
async def post_event_to_project(project_name: str, event: dict):
    if not await es.indices.exists(index=project_name):
        raise ElasticIndexNotFound(project_name)

    try:
        return await es.index(project_name, {
            'server_timestamp': datetime.now(timezone.utc),
            'event': event
        })
    except Exception as e:
        raise ElasticInternalError() from e
