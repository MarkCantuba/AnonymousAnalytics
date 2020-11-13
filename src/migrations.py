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


def migrate():
    if not es.indices.exists(index=".projects"):
        # Get all existing indices
        indices = es.cat.indices(h="index").split()
        es.indices.create(index=".projects", body={
            "settings": {
                "index": {
                    "hidden": True
                }
            }
        })
        for index in indices:
            es.create(index=".projects", id=index, body={
                "id": index,
                "name": index,
                "description": None
            })
        es.indices.refresh(index=".projects")
        logger.info("migrations.py: .projects index migrated")
    else:
        logger.info("migrations.py: .projects index already exists, skipping")

    all_projects = es.search(index=".projects")
    hits = all_projects["hits"]["hits"]
    project_ids = [hit["_source"]["id"] for hit in hits]

    for project in project_ids:
        bulk_update_documents(index=project)


def bulk_update_documents(*, index: str):
    update_doc_script = "if (!ctx._source.containsKey('event_type') || ctx._source.event_type == 'hello') {" \
                        "  ctx._source.event_type = 'default_event' } " \
                        "if (!ctx._source.containsKey('client_timestamp')) {" \
                        "  ctx._source.client_timestamp = ctx._source.server_timestamp }"

    request_body = {"script": update_doc_script}

    try:
        es.update_by_query(index=index, body=request_body)
    except Exception as e:
        return e


if __name__ == "__main__":
    migrate()