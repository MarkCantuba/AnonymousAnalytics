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


def query_histogram_by_date_interval(elastic_sess: AsyncElasticsearch, project_name: str, start: datetime, end: datetime, interval: int):
    if start > end:
        raise InvalidRange()
    if start.tzinfo != timezone.utc:
        raise InvalidTimestamp(start)
    if end.tzinfo != timezone.utc:
        raise InvalidTimestamp(end)

    request_body = {
        "aggs": {
            "events_over_time": {
                "date_histogram": {
                    "field": "server_timestamp",
                    "fixed_interval": "{}s".format(interval)
                }
            }
        },
        "query": {
            "range": {
                "server_timestamp": {
                    "gte": start,
                    "lte": end
                }
            }
        },
        "size": "0"
    }

    return elastic_sess.search(index=project_name, body=request_body)
