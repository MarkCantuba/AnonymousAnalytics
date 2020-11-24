from models import Project
from models import Event
from datetime import datetime, timezone

def test_project():
    # Create a project object
    project = Project(id='project3', name='Dare Devil2', 
    description='How to play Dare Devil2')
    

    # Check the attributes to make sure a valid project is actually created
    assert type(project) == Project
    assert project.id == 'project3'
    assert project.name == 'Dare Devil2'
    assert project.description == 'How to play Dare Devil2'

def test_event():
    
    # create an event
    event_object = Event(server_timestamp=None, 
                        client_timestamp=datetime.now(timezone.utc),
                        event_type='Adventure',
                        event_body={'game': 'Grand Theft Auto',
                                'Level': 3,
                                'Wins': 56,
                                'Losses': 11})
    assert type(event_object) == Event

    random_event = {'game': 'World of War Craft',
                    'Level': 4,
                    'Wins': 60,
                    'Losses': 1}

    duplicate_dict = {'game': 'Grand Theft Auto',
                                'Level': 3,
                                'Wins': 56,
                                'Losses': 11}
    # verify that this random event isn't equal to the event just created
    assert event_object.event_body != random_event
    # verify that duplicate dict of an event is the same with the exact event
    assert [event for event in event_object.event_body if event not in duplicate_dict] == []
