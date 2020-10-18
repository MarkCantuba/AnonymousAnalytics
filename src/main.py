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
# get all projects currently recorded
# return a list of dictionaries, each dictionary contains all the fields (id, name, description) for one project.
async def get_all_projects():
    # check if the index .projects exists, raise 404 error if not
    if not await es.indices.exists(index='.projects'):
        raise ElasticIndexNotFound('.projects')
    query = {
        'query': {
            'match_all': {}
        },
        'size': 100  # override the limit of number returned to 100
    }
    res = await es.search(
        index='.projects',
        # project fields are stored in the _source of document
        body=query
    )

    # extract projects from res['hits']['hits'].source
    projects = [doc['_source'] for doc in res['hits']['hits']]
    return projects


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
