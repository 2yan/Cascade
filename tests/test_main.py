
from app_data import main
import app_data.objects as objects
from app_data.objects import sql
#from app_data.objects import Node
import json
import pytest
import os

@pytest.fixture(autouse=True)
def run_around_tests():
    sql.database_name = 'test_database.db'
    try:
        os.remove('test_database.db')
    except Exception as e:
        pass
    sql.create_database()
    yield
    os.remove('test_database.db')
    
    


def test_api():

    example_data = """
    {
    "directed": true,
    "multigraph": false,
    "graph": {},
    "nodes": [
    {
    "description": "This is the description for source a",
    "id": "a"
    },
    {
    "description": "This is the description for source b",
    "id": "b"
    },
    {
    "description": "This is the description for source c",
    "id": "c"
    }
    ],
    "links": [
    {
    "source": "a",
    "target": "b"
    },
    {
    "source": "b",
    "target": "c"
    }
    ]
    }
    
    """
    example_data = json.loads(example_data)
    main.load_json(example_data)
    
    nodes = objects.load_all_nodes()
    assert len(nodes) == 3 # Ensure all Nodes are loaded
    
    for node in nodes:
        assert node.id in ['a', 'b', 'c']
        assert node.description == 'This is the description for source ' + node.id
        
    
    a = objects.load_node_from_id('a') 
    b = objects.load_node_from_id('b')
    c = objects.load_node_from_id('c')
    
    assert a in b.get_parents()
    assert b in c.get_parents()
    
    assert b in a.get_children()
    
