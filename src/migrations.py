from datetime import datetime, timezone

from elasticsearch import Elasticsearch
from fastapi.logger import logger

import config

conf = config.get()
es = Elasticsearch([
    {
        "host": conf["elasticsearch"]["private_ip"],
        "port": conf["elasticsearch"]["rest_port"]
    }
])


def add_projects_index():
    # Get all existing visible indices
    indices = es.cat.indices(h="index").split()
    es.indices.create(index=".projects", body={
        "settings": {
            "hidden": True
        }
    })

    for index in indices:
        es.create(index=".projects", id=index, body={
            "id": index,
            "name": index,
            "description": None
        })

    es.indices.refresh(index=".projects")


def add_event_type():
    update_doc_script = '''
        if (!ctx._source.containsKey('event_type') || ctx._source.event_type == '') {
            ctx._source.event_type = 'default_event';
        }
        if (!ctx._source.containsKey('client_timestamp')) {
            ctx._source.client_timestamp = ctx._source.server_timestamp;
        }
        if (ctx._source.containsKey('event')) {
            ctx._source.event_body = ctx._source.event ;
            ctx._source.remove('event');
        }
    '''

    result = es.search(index=".projects", body={
        "query": {
            "match_all": {}
        },
        "size": 100
    })
    projects = result["hits"]["hits"]
    project_ids = [project["_source"]["id"] for project in projects]

    for project_id in project_ids:
        try:
            es.update_by_query(index=project_id, body={
                "script": update_doc_script
            })
        except Exception as e:
            # TODO: investigage logging -- it is not shwoing in uvicorn logger
            logger.error("migrations.py:", e)


VERSIONS = [
    {
        "name": "add .projects",
        "version": 1,
        "fn": add_projects_index
    },
    {
        "name": "add event_type",
        "version": 2,
        "fn": add_event_type
    }
]


def migrate():
    if not es.indices.exists(index=".schema"):
        es.indices.create(index=".schema", body={
            "settings": {
                "hidden": True
            }
        })
        logger.info("migrations.py: .schema index created")
        latest_version = 0
    else:
        result = es.search(index=".schema", size=1, body={
            "query": {
                "match_all": {}
            },
            "sort": [{
                "version": {
                    "order": "desc"
                }
            }]
        })
        latest_migration = result["hits"]["hits"][0]
        if latest_migration is None:
            latest_version = 0
        else:
            latest_version = latest_migration["_source"]["version"]

    unapplied_migrations = VERSIONS[latest_version:]

    for migration in unapplied_migrations:
        migration["fn"]()
        es.index(index=".schema", body={
            "name": migration["name"],
            "version": migration["version"],
            "created_timestamp": datetime.now(timezone.utc)
        })

    es.indices.refresh(index=".schema")
