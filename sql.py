

import sqlite3
import pandas as pd

database_name = 'database.db'


def do_sql(query):
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    con.close()

def read_sql(query):
    data = pd.read_sql(query, con  = sqlite3.connect(database_name))
    return data
    
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
    query = f"""
    REPLACE INTO Node (id, description)
    VALUES(
    '{index}', '{description}'
    
    );
    """
    do_sql(query)
    return True


def load_node_data(specific_node = False):
    query = """
    select * from Node 
    """
    if specific_node:
        query = query + f'where id = {specific_node}'
    
    data = read_sql(query)
    data = data.set_index('id')
    return data
    
def save_connection(parent_id, child_id):
    query = f"""
    REPLACE INTO Connection (parent_id, child_id)
    VALUES(
    '{parent_id}', '{child_id}'
    );
    """
    
    do_sql(query)
    return True
    
    
def get_children(parent_id):
    query = f"""Select child_id from Connection
    where parent_id = '{parent_id}'
    """
    data = read_sql(query)
    return set()
    
    
def get_parents(child_id):
    query = f"""Select parent_id from Connection
    where child_id= '{child_id}'
    """
    data = read_sql(query)
    return set()
    
    