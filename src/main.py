import os
import config

from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from elasticsearch import AsyncElasticsearch

from exceptions import *

from models import *

conf = config.get()
app = FastAPI()
es = AsyncElasticsearch([
    { 'host': conf['elasticsearch']['private_ip'], 'port': conf['elasticsearch']['rest-port'] }
])

@app.get("/info")
async def info():
    return await es.info()

@app.get("/index/{index_name}")
async def get_index(index_name: str):
    try:
        return await es.search(index=index_name)
    except Exception as e:
        return str(e)

@app.get("/index/{index_name}/{doc_id}")
async def get_doc(index_name: str, doc_id: str):
    try:
        return await es.get(index_name, doc_id)
    except Exception as e:
        return str(e)

# @app.post("/index/{index_name}")
# async def post_doc(index_name: str, doc: NewDoc):
#     try:
#         return await es.index(index_name, doc.content)
#     except Exception as e:
#         return str(e)



@app.post("/projects")
async def post_project(project: Project):
    if await es.indices.exists(index=project.project_name):
        raise HTTPElasticIndexExists(project.project_name)

    try:
        return await es.indices.create(project.project_name, dict())
    except Exception as e:
        return e


@app.post("/projects/{project_name}/events/")
async def post_event_to_project(project_name: str, new_event: Event):
    if not await es.indices.exists(index=project_name):
        raise HTTPElasticIndexDoesntExists(project_name)

    try:
        return await es.index(project_name, new_event.dict())
    except Exception as e:
        return str(e)