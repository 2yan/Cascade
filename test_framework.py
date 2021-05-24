import objects
from objects import Node
import sql
import numpy as np

original_db_name = ''

def use_test_db():
    # Temporarily use a test db
    global original_db_name
    original_db_name = sql.database_name
    sql.database_name = 'test_database.db'


def return_db_name():
    # Cleanup database to original 
    sql.database_name = original_db_name
    
    
def test_nodes():
    use_test_db()
    
    """
    Test Node creation
    """
    n = Node(1,'Nodes must have a description & ID')
    
    assert n.id == '1'
    assert n.description == 'Nodes must have a description & ID'
    
    
    """
    Test parent and child operations
    """
    
    n2 = Node(2, 'I am a child of Node 1')
    n.add_child(n2)    
    assert n2 in n.children
    assert n in n2.parents
    
    """ Test Saving"""
    n.save()
    assert n in objects.load_all_nodes()
    
    return_db_name()
    
    
    
    
def test_sql():
    #Ensure the database name is set correctly
    assert sql.database_name == 'database.db'
    use_test_db()
    
    sql.create_database()
    
    """ Check to see if saving Nodes works"""
    n = Node(np.random.randint(0, 10000), 'This should create a node and save it')
    assert sql.save_node(n.id, n.description) == True
    
    """ Check if Loading Nodes Works"""
    node_data = sql.load_node_data()
    assert n.id in node_data.index
    
    """ Check to see if saving connections works"""
    assert sql.save_connection("1", "2") == True
    assert "1" in sql.get_parents("2")
    assert "2" in sql.get_children("1")
    
    return_db_name()
    
    