

import sqlite3
import itertools

database_name = 'database.db'


def do_sql(query, args = ()):
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    cur.execute(query, args)
    con.commit()
    con.close()

def read_sql(query, args = ()):
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    cur.execute(query, args)

    rows = cur.fetchall()
    return rows
    
def create_database():
    query = """
    CREATE TABLE IF NOT EXISTS Node
    (
	id TEXT PRIMARY KEY UNIQUE,
   	description TEXT NOT NULL
    ) 
    """
    
    do_sql(query)
    
    query = """
    CREATE TABLE IF NOT EXISTS Connection
    (
    parent_id TEXT NOT NULL,
    child_id TEXT NOT NULL,
    PRIMARY KEY (parent_id, child_id)
    ) ;
    
    """
    do_sql(query)
    
    

def save_node(index, description):
    query = """
    REPLACE INTO Node (id, description)
    VALUES(
    ?, ?
    
    );
    """
    do_sql(query, (index, description))
    return True


def load_nodes(specific_node = False):
    query = """
    select * from Node 
    """
    if specific_node:
        query = query + 'where id = ?'
        data = read_sql(query, specific_node)
        return data
    
    data = read_sql(query )
    return data
    
def save_connection(parent_id, child_id):
    if parent_id == child_id:
       raise ValueError("""
                        Parent and Child ids can not be the same in this data model
                        
                        """  ) 
    query = """
    REPLACE INTO Connection (parent_id, child_id)
    VALUES(
    ?, ?
    );
    """
    
    do_sql(query, (parent_id, child_id))
    return True
    


    
def get_children(parent_id):
    query = """Select child_id from Connection
    where parent_id = ?
    """
    data = read_sql(query, str(parent_id))
    children = itertools.chain.from_iterable(data)
    return set(children)
    
    
def get_parents(child_id):
    query = """Select parent_id from Connection
    where child_id= ?
    """
    data = read_sql(query, str(child_id))
    parent_ids = itertools.chain.from_iterable(data)
    return set(parent_ids)
    
def delete_node(index):
    index = str(index)
    #DELETES THE NODE ITSELF
    query = """
    DELETE FROM Node
    WHERE id = ?;
    """
    do_sql(query, index)
    
    query = """
    DELETE FROM Connection
    where child_id == ?
    or parent_id == ?"""
    do_sql(query, (index, index))
    
    return 

def search_nodes(text):
    text = '%' + text + '%'
    text = text.lower()
    
    query = """
    select * from Node 
    where id like ?
    or description like ?
    """
    data = read_sql(query, (str(text), str(text)))
    return data
    