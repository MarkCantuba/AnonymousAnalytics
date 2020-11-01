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
