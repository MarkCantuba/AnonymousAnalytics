from datetime import datetime, timezone, timedelta
from typing import Optional

from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, Query

import config
from exceptions import *
from models import *

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
            "server_timestamp": datetime.now(timezone.utc),
            "event": event
        })
    except Exception as e:
        raise ElasticInternalError() from e


@app.get("/projects/{project_name}/events")
async def get_events_by_timestamp(
        project_name: str,
        start: Optional[datetime] = Query(datetime.now(timezone.utc) - timedelta(days=7)),
        end: Optional[datetime] = Query(datetime.now(timezone.utc))
):
    # validate start & end when they are not given as default value
    if start.tzinfo != timezone.utc:
        raise BadRequest("Datetime {} has wrong timezone, use UTC instead".format(start))
    if end.tzinfo != timezone.utc:
        raise BadRequest("Datetime {} has wrong timezone, use UTC instead".format(end))
    if not await es.indices.exists(index=project_name):
        raise ElasticIndexNotFound(project_name)

    try:
        request_body = {
            "query": {
                "range": {
                    "server_timestamp": {
                        "gte": start,
                        "lte": end
                    }
                }
            }
        }

        return await es.search(index=project_name, body=request_body)

    except Exception as e:
        raise ElasticInternalError() from e
