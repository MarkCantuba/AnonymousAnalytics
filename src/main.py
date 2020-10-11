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


@app.get("/projects/{project_name}/events")
async def get_events_by_timestamp(project_name: str,
                                  start: datetime = datetime.now(timezone.utc) - timedelta(days=7),
                                  end: datetime = datetime.now(timezone.utc)):
    # validate start & end when they are not given as default value
    if start.tzinfo == None:
        raise HTTPException(status_code=500, detail='Error: the given datetime: {} has no timezone information'.format(start))
    if end.tzinfo == None:
        raise HTTPException(status_code=500, detail='Error: the given datetime: {} has no timezone information'.format(end))
    if not start.tzinfo == pytz.utc:
        raise HTTPException(status_code=500, detail='Error: timezone of the given datetime: {} is not UTC'.format(start))
    if not end.tzinfo == pytz.utc:
        raise HTTPException(status_code=500, detail='Error: timezone if the given datetime: {} is not UTC'.format(end))

    try:
        request_body = {
            "query": {
                "range": {
                    "timestamp": {
                        "gte": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "lte": end.strftime("%Y-%m-%dT%H:%M:%SZ")
                    }
                }
            }
        }

        return await es.search(index=project_name, body=request_body)

    except Exception as e:
        return str(e)
