from fastapi import HTTPException
from datetime import datetime

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


class ElasticInvalidTimeStamp(HTTPException):
    def __init__(self, time: datetime):
        self.status_code = 400

        self.detail = {
            "status_code": 400,
            "msg": "Datetime {} has wrong timezone. Use UTC instead.".format(time)
        }


class ElasticInvalidStrEndRange(HTTPException):
    def __init__(self):
        self.status_code = 400

        self.detail = {
            "status_code": 400,
            "msg": "Invalid date range: Start date cannot be greater than End date!"
        }