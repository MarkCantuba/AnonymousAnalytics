from fastapi.testclient import TestClient
from main import app
import json 

client = TestClient(app)

def test_get_all_projects():
    response = client.get("/projects")
    assert response.status_code == 200
    
    # expected lists of projects from the server datastore
    expected_list = [
                        {
                            "id": "test1",
                            "name": "project1",
                            "description": "This is a test project"
                        },
                        {
                            "id": "test2",
                            "name": "project2",
                            "description": "This is the second test project"
                        }
                    ]
    
    # convert json string to a Python list
    response_list = response.json()
    
    # make a list of dictionaries that aren't common to both lists:none
    assert [x for x in expected_list if x not in response_list] == []