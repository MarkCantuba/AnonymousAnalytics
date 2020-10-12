from fastapi import HTTPException


class ElasticIndexExists(HTTPException):
    def __init__(self, project_name: str):
        self.status_code = 409

        self.detail = {
            "status_code": 409,
            "msg": "Given project {} already exists".format(project_name)
        }


class ElasticIndexNotFound(HTTPException):
    def __init__(self, project_name: str):
        self.status_code = 404

        self.detail = {
            "status_code": 404,
            "msg": "Given project {} does not exist".format(project_name)
        }


class ElasticInternalError(HTTPException):
    def __init__(self):
        self.status_code = 500

        self.detail = {
            "status_code": 500,
            "msg": "Elasticsearch has returned an error from the request"
        }
