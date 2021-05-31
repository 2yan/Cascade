

from flask import Flask
import flask as f
from . import objects 


app = Flask(__name__)

@app.route('/')
def hello_world():
    return f.render_template('home.html') 

def load_json(json_data):
    # Currently saves data on create
    # Will overwrite data if the node already exists

    nodes = json_data.get('nodes', [])
    links = json_data.get('links', [])
    
    try:
    
        # Load all the nodes first
        for node in nodes:
            iden = node['id']
            description = node.get('description', "")
            n = objects.Node(iden, description)
            n.save()
    
        # Load all the links next
        for link in links:
            source_node = objects.load_node_from_id(link['source'])
            target_node = objects.load_node_from_id(link['target'])
    
            source_node.add_child(target_node)
    
        return f.Response(str({'status':'good'}), status=200, mimetype='application/json')

    except Exception as e:

        text = str(e)
        error_json = {'status':'Bad Request', 
         'Error Code': text}
        
        return f.Response(str(error_json), status = 400, mimetype= 'application/json')
        


if __name__ == "__main__":
        app.run(debug = True)
