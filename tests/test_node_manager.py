import sys
import os
sys.path.append(os.path.abspath('../Title'))

import node_manager 
from node_manager import Node
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
    n1 = Node('save', 'Parent')
    n2 = Node('whales', 'Child')
    assert n1.add_child(n2) == True
    try:
        n1.add_child(n1)
        assert True == False # Should not be able to add a self reference
    except Exception as e:
        pass
    
    
def test_add_parent():
    n1 = Node('be', 'Parent')
    n2 = Node('good', 'Child')
    
    assert n2.add_parent(n1) == True
    
    try:
        n1.add_parent(n1)
        assert True == False # Should not be able to add a self reference
    except Exception as e:
        pass
    
    
def test_get_children():
    n1 = Node('1asd', 'Parent')
    n2 = Node('aaaa', 'Child')
    n3 = Node('dood', 'Child of n2')
    
    n1.add_child(n2)
    n2.add_child(n3)
    assert n2 in n1.get_children()
    assert n3 not in n1.get_children()
    
    
def test_get_parents():
    n1 = Node('potato', 'Parent')
    n2 = Node('tomato', 'Child')
    n2.add_parent(n1)
    assert n2 in n1.get_children()
    
def test_save():
    n1 = Node('sandwhich', 'the one node')
    assert n1.save() == True
    

def test_load_all_nodes():
    n1 = Node('131', 'the one node')
    n2 = Node('random', 'The other Node')
    assert n1 in node_manager.load_all_nodes()  
    assert n2 in node_manager.load_all_nodes()  
   
    

def test_load_node_from_id():
    n1 = Node('xxo', 'the one node')
    n2 = Node('asdad', 'The other Node')
    """ Test loading one Node"""
    one_node = node_manager.load_node_from_id(n1.id)
    assert n1 == one_node
    assert n2 != one_node
    
    
def test_delete():
    n1 = Node('live', 'Parent')
    n2 = Node('well', 'Child')   
    
    delete_me = node_manager.Node(3, 'Delete Me')
    n1.add_child(delete_me)
    n2.add_parent(delete_me)
    
    # Check Deleting 
    assert delete_me.delete() == True

    assert delete_me not in node_manager.load_all_nodes()
    # Check if parent/child relationships are removed
    assert delete_me not in n1.get_children()
    assert delete_me not in n2.get_parents()
    # Ensure only the appropriate node is deleted
    assert n1 in node_manager.load_all_nodes()

def test_delete_node():
    n1 = Node('swagger', 'Parent')
    n2 = Node('swaggerlo', 'Child')   
    
    delete_me = Node('swaggeree', 'Delete Me')
    n1.add_child(delete_me)
    n2.add_parent(delete_me)
    
    # Check Deleting 
    assert node_manager.delete_node('swaggeree') == True

    assert delete_me not in node_manager.load_all_nodes()
    # Check if parent/child relationships are removed
    assert delete_me not in n1.get_children()
    assert delete_me not in n2.get_parents()
    # Ensure only the appropriate node is deleted
    assert n1 in node_manager.load_all_nodes()
    assert n2 in node_manager.load_all_nodes()

    


def test_get_upstream():
    a = Node('a', 'a')
    b = Node('b', 'b')
    c = Node('c', 'c')
    d = Node('d', 'd')
    e = Node('e', 'e')
    f = Node('f', 'f')

    
    a.add_child(b)
    b.add_child(c)
    c.add_child(d)
    d.add_child(e)
    b.add_child(f) #E is a child of an upstream element of D but not upstream of d,
    # it's on a different branch
    
    upstream = d.get_upstream([])
    for node in [a, b, c]:
        assert node in upstream # check logical upstream
        
    assert e not in upstream # E is a child of D
    assert d not in upstream # Ensure self is not in upstream
    assert f not in upstream # Ensure branching F is not included
    
    d.add_child(a) # Create a recursive situation
    upstream = d.get_upstream([]) # Recalculate the upstream data
    assert d not in d.get_upstream([]) # Avoid self referencing and perma looping
    
    # Re-check previous data
    assert e not in upstream # E is a child of D
    assert d not in upstream # Ensure self is not in upstream
    assert f not in upstream # Ensure branching F is not included
    
    # Create a different recursive situation
    c.add_child(a)
    upstream = d.get_upstream([])


def test_get_downstream():
    a = Node('a', 'a')
    b = Node('b', 'b')
    c = Node('c', 'c')
    d = Node('d', 'd')
    e = Node('e', 'e')
    f = Node('f', 'f')

    a.add_child(b)
    b.add_child(c)
    c.add_child(d)
    d.add_child(e)
    d.add_parent(f)  # F is not downstream of a, though it is a parent to a child of a
    
    downstream= a.get_downstream([])
    
    for node in [b, c, d, e]:
        assert node in downstream # Check logical downstream

    assert f not in downstream # F is not downstream of a but it is a parent to a child of a
    assert a not in downstream # Ensure self is not in downstream
    
    e.add_child(a) # Create a recursive situation
    downstream = a.get_downstream([])
    assert a not in downstream # Avoid self referencign and perma looping


    # Re check other data
    assert f not in downstream  # F is not downstream of a but it is a parent to a child of a
    assert a not in downstream # Ensure self is not in downstream
     
def test_search():
    sql.save_node('database.No Name', 'The Good')
    sql.save_node('database.Angel Eyes', 'The Bad')
    sql.save_node('database.Tuco', 'The Ugly')
    
    # Check Descriptions
    # All three should show up
    ans = node_manager.search_nodes('the')
    assert len(ans) == 3

    # Find only the good
    ans = node_manager.search_nodes('Good')
    assert len(ans) == 1
    assert ans[0].id == 'database.No Name'
    
    # All three should show up
    ans = node_manager.search_nodes('database')
    assert len(ans) == 3
    descriptions = ''
    for n in ans:
        descriptions = descriptions + '\n' +n.description
    
    assert 'Good' in descriptions
    assert 'Bad' in descriptions
    assert 'Ugly' in descriptions
