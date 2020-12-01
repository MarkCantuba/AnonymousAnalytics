from fastapi.testclient import TestClient
from main import app
from models import Project
import json 

client = TestClient(app)

"""Test a post request; test posting a project"""
def test_post_project():
    route = "/projects"
    # Create a project object
    project = Project(id='test1', name='project1', 
    description='This is a test project')
    

    # Check the attributes to make sure a valid project is actually created
    assert type(project) == Project
    assert project.id == 'test1'
    assert project.name == 'project1'
    assert project.description == 'This is a test project'

    # attempt a post request
    response = client.post(route, project.json())
    assert response.status_code == 201 

    # create a second project
    project2 = Project(id='test2', name='project2', 
    description='This is another test project')
    

    # Check the attributes to make sure a valid project is actually created
    assert type(project2) == Project
    assert type(project2.id) == str
    assert project2.id == 'test2'
    assert project2.name == 'project2'
    assert project2.description == 'This is another test project'
    
    # attempt a post request
    response = client.post(route, project2.json())
    assert response.status_code == 201

"""Test the retrieval of all projects"""
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
                            "description": "This is another test project"
                        }
                    ]
    
    # convert json string to a Python list
    response_list = response.json()
    
    # make a list of dictionaries that aren't common to both lists:none
    assert [x for x in expected_list if x not in response_list] == []

"""
 Retrieve a project by ProjectId
"""
def test_get_project():
    response =client.get("/projects/test1")
    assert response.status_code == 200 

    # verify that a project with the given id is retrieved
    project =           {
                            "id": "test1",
                            "name": "project1",
                            "description": "This is a test project"
                        }
    assert response.json() == project


if __name__ == "__main__":
    test_post_project()
    test_get_all_projects()
    test_get_project()