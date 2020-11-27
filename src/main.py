from fastapi import FastAPI, Query

import config
from migrations import migrate
from models import *
from project.project import *

conf = config.get()

es = AsyncElasticsearch([
    {
        "host": conf["elasticsearch"]["private_ip"],
        "port": conf["elasticsearch"]["rest_port"]
    }
])

migrate()
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
        index=".projects",
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
    query = {
        "query": {
            "match_all": {}
        },
        "size": 100  # override the limit of number returned to 100
    }
    res = await es.search(
        index=".projects",
        # project fields are stored in the _source of document
        body=query
    )

    # extract projects from res["hits"]["hits"].source
    projects = [doc["_source"] for doc in res["hits"]["hits"]]
    return projects


@app.get("/projects/{project_id}")
async def get_project(
    *,
    project_id: str = ProjectId,
):
    if not await es.indices.exists(index=project_id):
        raise ElasticIndexNotFound(project_id)
    response = await es.get(index=".projects", id=project_id)

    return response["_source"]


@app.post("/projects/{project_id}/events")
async def post_event_to_project(
        *,
        project_id: str = ProjectId,
        event: dict
):
    if not await es.indices.exists(index=project_id):
        raise ElasticIndexNotFound(project_id)

    new_event = Event(client_timestamp=event["client_timestamp"],
                      event_type=event["event_type"],
                      event_body=event["event_body"])

    return await es.index(project_id, new_event.json())


@app.get("/projects/{project_id}/events")
async def get_events_by_timestamp(
        *,
        project_id: str = ProjectId,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None
):
    if not await es.indices.exists(index=project_id):
        raise ElasticIndexNotFound(project_id)

    return await query_event_by_timestamp(es, project_id, start, end)


@app.get("/projects/{project_id}/events/counts")
async def get_histogram_by_date_interval(
        *,
        project_id: str = ProjectId,
        event_type: Optional[str] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        interval: Optional[int] = Query(21600, gt=0)
):
    if not await es.indices.exists(index=project_id):
        raise ElasticIndexNotFound(project_id)

    response = await query_histogram_by_date_interval(es, project_id, event_type, start, end, interval)

    histogram_data = [
        event_count["doc_count"]
        for event_count
        in response["aggregations"]["events_over_time"]["buckets"]
    ]

    return histogram_data
