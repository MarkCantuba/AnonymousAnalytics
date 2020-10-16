from datetime import datetime, timedelta, timezone
from elasticsearch import AsyncElasticsearch
from exceptions import *


def query_event_by_timestamp(elastic_sess: AsyncElasticsearch, project_name: str, start: datetime, end: datetime):
    if start > end:
        raise InvalidRange()
    if start.tzinfo != timezone.utc:
        raise InvalidTimestamp(start)
    if end.tzinfo != timezone.utc:
        raise InvalidTimestamp(end)

    request_body = {
        "query": {
            "range": {
                "server_timestamp": {
                    "gte": start,
                    "lte": end
                }
            }
        }
    }

    return elastic_sess.search(index=project_name, body=request_body)

def get_len_bytes(a_string):
    bytes_of_a_string = bytes(a_string, 'utf-8')
    return len(bytes_of_a_string)
