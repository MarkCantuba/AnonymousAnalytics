from fastapi import HTTPException


class HTTPElasticIndexExists(HTTPException):
    def __init__(self, project_name: str, status_code: int = 404, message: str = "Given index already exists!"):
        self.status_code = status_code

        self.detail = {
            "Status Code": status_code,
            "Project Name": project_name,
            "Error Message": message
        }


class HTTPElasticIndexDoesntExists(HTTPException):
    def __init__(self, project_name: str, status_code: int = 501, message: str = "Given index does not exists!"):
        self.status_code = status_code

        self.detail = {
            "Status Code": status_code,
            "Project Name": project_name,
            "Error Message": message
        }
