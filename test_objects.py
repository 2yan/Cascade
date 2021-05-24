import objects
from objects import Node
import sql
import os
import pytest

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
    
    
    
def test_Node():
    """
    Test Node creation
    """
    n = Node(1,'Nodes must have a description & ID')
    
    assert n.id == '1'
    assert n.description == 'Nodes must have a description & ID'
    
def test_add_child():
    n1 = Node(1, 'Parent')
    n2 = Node(2, 'Child')
    assert n1.add_child(n2) == True
    
def test_add_parent():
    n1 = Node(1, 'Parent')
    n2 = Node(2, 'Child')
    
    assert n2.add_parent(n1) == True

    
    
def test_get_children():
    n1 = Node(1, 'Parent')
    n2 = Node(2, 'Child')
    n3 = Node(3, 'Child of n2')
    
    n1.add_child(n2)
    n2.add_child(n3)
    assert n2 in n1.get_children()
    assert n3 not in n1.get_children()
    
    
def test_get_parents():
    n1 = Node(1, 'Parent')
    n2 = Node(2, 'Child')
    n2.add_parent(n1)
    assert n2 in n1.get_children()
    
def test_save():
    n1 = Node(1, 'the one node')
    assert n1.save() == True
    

def test_load_all_nodes():
    n1 = Node(1, 'the one node')
    n2 = Node(2, 'The other Node')
    assert n1 in objects.load_all_nodes()  
    assert n2 in objects.load_all_nodes()  



def test_load_node_from_id():
    n1 = Node(1, 'the one node')
    n2 = Node(2, 'The other Node')
    """ Test loading one Node"""
    one_node = objects.load_node_from_id(n1.id)
    assert n1 == one_node
    assert n2 != one_node
    
    
def test_delete():
    n1 = Node(1, 'Parent')
    n2 = Node(2, 'Child')   
    
    delete_me = objects.Node(3, 'Delete Me')
    n1.add_child(delete_me)
    n2.add_parent(delete_me)
    
    # Check Deleting 
    assert delete_me.delete() == True

    assert delete_me not in objects.load_all_nodes()
    # Check if parent/child relationships are removed
    assert delete_me not in n1.get_children()
    assert delete_me not in n2.get_parents()
    # Ensure only the appropriate node is deleted
    assert n1 in objects.load_all_nodes()

    
    

    

    

    