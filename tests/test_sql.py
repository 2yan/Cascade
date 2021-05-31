

import os
import sys
sys.path.append(os.path.abspath('./app_data'))

import sql
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
    

def test_create_database():
    # See if databases are created
    assert len(sql.read_sql('select * from Node')) == 0
    assert len(sql.read_sql('select * from Connection')) == 0 
    
    
def test_save_node():
    # Checking saving operation
    assert sql.save_node(1, 'test') == True
    
def test_load_node_data():
    
    sql.save_node(1, 'test_1')
    sql.save_node(2, 'test_2')
    data = sql.load_nodes()
    # Should only have 2 nodes
    assert(len(data) == 2)
    
    data = dict(data)
    # Check Node data
    assert data['1'] == 'test_1'
    assert data['2'] == 'test_2'
    
    sql.save_node(1, 'test_updated') # Test updating of data
    
    data = sql.load_nodes()
    # Should still only have 2 nodes
    assert(len(data) == 2)
    
    data = dict(data)
    assert data['1'] == 'test_updated'
    assert data['2'] == 'test_2' # This should not change

def test_save_connection():
    # Check if saving connection works
    assert sql.save_connection(1, 2) == True
    # No self referencing
    try:
        sql.save_connection(1,1)
        assert True == False # Should not allow saving a self connection
    except Exception as e:
        pass
    
    
def test_get_children():
    sql.save_connection(1, 2)
    children = sql.get_children(1)
    assert '2' in children # Check results of saving connections
    assert '1' not in children # Only correct children are returned
    
def test_get_parents():
    sql.save_connection(1, 2)
    parents = sql.get_parents(2)
    assert '1' in parents 
    assert '2' not in parents
    
def test_delete_node():
    sql.save_node(1, 'parent_node')
    sql.save_node(2, 'delete_me_child_node')
    sql.save_node(3, 'other_child_node')
    
    sql.save_connection(1, 2) # 2 is a child of 1
    sql.save_connection(1, 3) # 3 is a child of 1
    
    sql.delete_node('2')
    nodes = sql.load_nodes()
    nodes = dict(nodes)
    assert '2' not in nodes.keys()
    assert '1' in nodes.keys()
    
    # See if child relationship is deleted
    assert '2' not in sql.get_children(1)
        
    # See if other child is NOT deleted
    assert '3' in sql.get_children(1)
    
    

def test_search():
    sql.save_node('database.No Name', 'The Good')
    sql.save_node('database.Angel Eyes', 'The Bad')
    sql.save_node('database.Tuco', 'The Ugly')
    
    # Check Descriptions
    # All three should show up
    ans = sql.search_nodes('the')
    assert len(ans) == 3
    ans = dict(ans)
    assert 'database.No Name' in ans.keys()
    
    ans = dict(sql.search_nodes('ugly'))
    # Only the Ugly
    assert 'database.Tuco'in ans.keys()
    
    # Not the Bad
    assert 'database.Angel Eyes' not in ans.keys()
    
    
    
    
    
    
    
