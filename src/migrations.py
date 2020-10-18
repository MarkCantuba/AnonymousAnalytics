from elasticsearch import AsyncElasticsearch
from fastapi.logger import logger


async def migrate(es: AsyncElasticsearch):
    if not await es.indices.exists(index=".projects"):
        # Get all existing indices
        indices = (await es.cat.indices(h="index")).split()
        await es.indices.create(index=".projects", body={
            "settings": {
                "index": {
                    "hidden": True
                }
            }
        })
        for index in indices:
            await es.create(index=".projects", id=index, body={
                "id": index,
                "name": index,
                "description": None
            })
        await es.indices.refresh(index=".projects")
        logger.info("migrations.py: .projects index migrated")
    else:
        logger.info("migrations.py: .projects index already exists, skipping")
