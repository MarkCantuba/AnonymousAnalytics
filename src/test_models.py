from models import Project

def test_project():
    project = Project(id='project3', name='Dare Devil2', 
    description='How to play Dare Devil2')
    

    assert type(project) == Project
    assert project.id == 'project3'
    assert project.name == 'Dare Devil2'
    assert project.description == 'How to play Dare Devil2'