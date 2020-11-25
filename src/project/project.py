from datetime import timezone, timedelta

from elasticsearch import AsyncElasticsearch

from exceptions import *


def query_event_by_timestamp(
        elastic_sess: AsyncElasticsearch,
        project_name: str,
        start: datetime,
        end: datetime
):
    if start is None:
        start = datetime.now(timezone.utc) - timedelta(days=7)
    if end is None:
        end = datetime.now(timezone.utc)

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


def query_histogram_by_date_interval(
        elastic_sess: AsyncElasticsearch,
        project_name: str,
        start: datetime,
        end: datetime,
        interval: int
):
    if start is None:
        start = datetime.now(timezone.utc) - timedelta(days=7)
    if end is None:
        end = datetime.now(timezone.utc)

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
                    "fixed_interval": "{}s".format(interval),
                    "extended_bounds": {
                        "min": start,
                        "max": end
                    }
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
        "size": 0
    }

    return elastic_sess.search(index=project_name, body=request_body)

def query_event_mappings(
        elastic_sess: AsyncElasticsearch,
        project_name: str
):
    request_body = {
        "query" : {
            "bool": {
                "must" : [{ 
                    "terms" : { "event_type" : ["bool","number","text","list","object"] }, 
                    }]
            }
        }
    }

    return elastic_sess.search(index=project_name, body=request_body)
