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


class InvalidTimeStamp(HTTPException):
    def __init__(self, time: datetime):
        self.status_code = 400

        self.detail = {
            "status_code": 400,
            "msg": "Datetime {} has wrong timezone. Use UTC instead.".format(time)
        }


class InvalidRange(HTTPException):
    def __init__(self):
        self.status_code = 400

        self.detail = {
            "status_code": 400,
            "msg": "Invalid Range: Start range cannot be greater than the End range!"
        }
