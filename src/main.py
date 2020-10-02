import os

from typing import Optional
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from elasticsearch import AsyncElasticsearch

import config
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

@app.post("/index/{index_name}")
async def post_doc(index_name: str, doc: NewDoc):
    try:
        return await es.index(index_name, doc.content)
    except Exception as e:
        return str(e)

@app.post("/{project_name}/")
async def post_doc(project_name: str, new_event: Event):
    try:
        return await es.index(project_name, new_event.dict())
    except Exception as e:
        return str(e)