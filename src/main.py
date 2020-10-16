import asyncio

from fastapi import FastAPI, Query

import config
from migrations import *
from models import *
from project.project import *

conf = config.get()

es = AsyncElasticsearch([
    {
        "host": conf["elasticsearch"]["private_ip"],
        "port": conf["elasticsearch"]["rest_port"]
    }
])

asyncio.create_task(migrate(es))
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


@app.post("/projects", status_code=201)
async def post_project(*, project: Project):
    # validate project_id
    if await es.exists(index=".projects", id=project.id):
        raise ElasticIndexExists(project.id)

    doc = project.dict()

    # add doc to .project
    # refresh the .projects index after creating the doc, so it is immediately searchable
    await es.create(
        index='.projects', 
        id=project.id,
        refresh=True,
        body=doc
    )
    # create index
    await es.indices.create(project.id)
    return project.dict()


@app.get("/projects")
async def get_all_projects():
    res = await es.search(index='*', filter_path=['hits.hits._source'])
    return res['hits']['hits']


@app.post("/projects/{project_id}/events")
async def post_event_to_project(
        *,
        project_id: str = ProjectId,
        event: dict
):
    if not await es.indices.exists(index=project_id):
        raise ElasticIndexNotFound(project_id)

    new_event = Event(event=event)

    return await es.index(project_id, new_event.json())


@app.get("/projects/{project_id}/events")
async def get_events_by_timestamp(
        *,
        project_id: str = ProjectId,
        start: Optional[datetime] = Query(datetime.now(timezone.utc) - timedelta(days=7)),
        end: Optional[datetime] = Query(datetime.now(timezone.utc))
):
    if not await es.indices.exists(index=project_id):
        raise ElasticIndexNotFound(project_id)

    return await query_event_by_timestamp(es, project_id, start, end)
