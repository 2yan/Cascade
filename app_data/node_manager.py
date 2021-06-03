#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 23 18:28:09 2021

@author: ryan
"""
import sql



class Node: 
    def __init__(self, index, description, _save_on_create= True ):
        index = str(index)
        index = index.replace(' ', '_')
        for letter in index.lower():
            assert letter in ".-'?,abcdefghijklmnopqrstuvwxyz_1234567890$"
        if index.strip().strip() == '':
            raise ValueError("Index Can Not be Blank")
            
        self.id = str(index)
        
        self.description = str(description)
        if _save_on_create:
            self.save()
        return 
    
    def add_child(self, other_node):
        sql.save_connection(self.id, other_node.id)
        return True
    
    def add_parent(self, other_node):
        sql.save_connection(other_node.id, self.id)
        return True
    
    
    def get_children(self):
        child_ids = sql.get_children(self.id)
        children = []
        for index in child_ids:
            children.append(load_node_from_id(index))
        return children
    
    def get_parents(self):
        parent_ids = sql.get_parents(self.id)
        parents = []
        for index in parent_ids:
            parents.append(load_node_from_id(index))
        return parents
         
    
    def __eq__(self, obj):
        try:
            return self.id == obj.id
        except AttributeError:
            return False
    
    def __hash__(self):
        return hash(self.id)
    
    def __repr__(self):
        return f'<{self.id} : {self.description}>'
    
    def save(self):
        sql.save_node(self.id, self.description)
        return True
        
    def delete(self):
        sql.delete_node(self.id)
        return True
    
    def get_upstream(self, ignore_nodes = False):
        if ignore_nodes == False:
            raise ValueError('MUST CALL THIS FUNCTION AS FOLLOWS get_upstream([])')
        
        
        ignore_nodes.append(self)
            
        result = []
        parents = self.get_parents()
        for parent in parents:
            if parent not in ignore_nodes:
                result.append(parent)
                others = parent.get_upstream(ignore_nodes)
                result.extend(others)
            
        return result
    
    
    def get_downstream(self, ignore_nodes = False):
        if ignore_nodes == False:
            raise ValueError('MUST CALL THIS FUNCTION AS FOLLOWS get_downstream([])')
        
        ignore_nodes.append(self)
            
        result = []
        children = self.get_children()
        
        for child in children:
            if child not in ignore_nodes:
                result.append(child)
                others = child.get_downstream(ignore_nodes)
                result.extend(others)
            
        return result
    

def delete_connection(parent_node, child_node):
    sql.delete_connection(parent_node.id, child_node.id)
    return 

def delete_node(index):
    sql.delete_node(index)
    return True 

def search_nodes(text):
    node_data = sql.search_nodes(text)
    nodes = []
    for n in node_data:
        
        nodes.append(Node(n[0], n[1]))
    return nodes

def load_node_from_id(index):
    data = sql.load_nodes(index)
    n = Node(index, data[0][1])
    return n


def load_all_nodes():
    data = sql.load_nodes()
    nodes = []
    for row in data:
        n = Node(row[0], row[1], _save_on_create=False)
        nodes.append(n)
    return nodes
