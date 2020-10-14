from datetime import datetime, timedelta, timezone
from elasticsearch import AsyncElasticsearch
from exceptions import *


def query_event_by_timestamp(elastic_sess: AsyncElasticsearch, project_name: str, start: datetime, end: datetime):
    if start is None and end is None:
        start = (datetime.now() - timedelta(days=7)).replace(tzinfo=timezone.utc)
        end = datetime.now().replace(tzinfo=timezone.utc)

    elif start is None or end is None:
        if end is not None:
            start = (datetime.now() - timedelta(days=7)).replace(tzinfo=timezone.utc)

        elif start is not None:
            end = datetime.now().replace(tzinfo=timezone.utc)

    if start > end:
        raise InvalidRange()
    if start.tzinfo != timezone.utc:
        raise InvalidTimeStamp(start)
    if end.tzinfo != timezone.utc:
        raise InvalidTimeStamp(end)

    request_body = {
        "query": {
            "range": {
                "timestamp": {
                    "gte": start,
                    "lte": end
                }
            }
        }
    }

    return elastic_sess.search(index=project_name, body=request_body)
