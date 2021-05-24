#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 23 18:28:09 2021

@author: ryan
"""
import sql


nodes = []

class Node: 
    def __init__(self, index, description):
        self.id = str(index)
        self.description = str(description)
        
        index
        self.children = set()
        self.parents = set()
        nodes.append(self)
        return 
    
    def add_child(self, other_node):
        self.children.add(other_node)
        other_node.parents.add(self)
        self.save()
        other_node.save()
        return 
    
    def add_parent(self, other_node):
        # THis needs to be implemented
        return 
    
    def __eq__(self, obj):
        return self.id == obj.id
    
    def __hash__(self):
        return hash(self.id)
    
    def __repr__(self):
        return f'<{self.id} : {self.description}>'
    
    def save(self):
        sql.save_node(self.id, self.description)
        
        
        




def load_all_nodes():
    data = sql.load_node_data()
    nodes = []
    for index, vals in data.iterrows():
        description = vals['description']
        n = Node(index, description)
        nodes.append(n)
    return nodes
