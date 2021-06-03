

from flask import Flask
import flask as f
import node_manager 
import sql
import json

sql.create_database()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return f.render_template('home.html') 


@app.route('/upload', methods = ['POST'])
def upload():
    message = False
    progress = False
    
    if 'file' not in f.request.files:
        message = "Please Choose a File"
        progress = '0'
    else:
        file = f.request.files['file']
        if file.filename == '':
            message = "File Not Selected"
            progress = "0"
        else:
            data = file.read()
            failed = False
            try:
                json_data =  json.loads(data)
                
            except Exception as E:
                message = 'Failed! Due to Malformed JSON data.'
                progress = "0"
                failed = True
                

            if not(failed):
                uploaded = load_json(json_data)
                progress = str(uploaded)
                message = file.filename + ' has been uploaded'
    
    
    html = """
    <label class="form-label mr-1 form-text text-muted" for="customFile">
    """ + message + """
                <progress class="ml-2" id='progress' value='""" + progress + """' max='100'></progress>
                </label>
                <input type="file" name="file" class="form-control" id="customFile" />
                <input type="submit" value="Submit" class="btn btn-info">
            
            
            
            <script>
                htmx.on('#form', 'htmx:xhr:progress', function(evt) {
                  htmx.find('#progress').setAttribute('value', evt.detail.loaded/evt.detail.total * 100)
                });
            </script>
    
    """
    
    
    return html


def load_json(json_data):
    # Currently saves data on create
    # Will overwrite data if the node already exists

    nodes = json_data.get('nodes', [])
    links = json_data.get('links', [])
    total = len(nodes) + len(links)
    i = 0
    
    try:
        
        # Load all the nodes first
        for node in nodes:
            iden = node['id']
            description = node.get('description', "")
            n = node_manager.Node(iden, description)
            n.save()
            i = i + 1
    
        # Load all the links next
        for link in links:
            source_node = node_manager.load_node_from_id(link['source'])
            target_node = node_manager.load_node_from_id(link['target'])
    
            source_node.add_child(target_node)
            i = i + 1
    
        return 100

    except Exception as e:        
        return int((i/total) * 100)
        
@app.route('/search', methods = ['POST'])
def search():
    search_text = f.request.form.get('search_text', "")
    nodes = node_manager.search_nodes(search_text)

    if len(nodes) == 0:
        return '<text class="text-muted"> No Tables found </text>'
    for node in nodes:
        node.html_class = ""
        if node.id.lower() == search_text.lower():
            node.html_class = " table-primary "
    
    return f.render_template('list.html', nodes = nodes)

@app.route('/add_node', methods = ['Post'])
def add_node():

    name = f.request.form['name']
    name = name.strip()
    description = f.request.form.get('description', '')

    n = node_manager.Node(name, description)
    n.save()
    return 'Data Added'

@app.route('/delete_node', methods = ['POST'])
def delete_node():
    
    index = f.request.form['index']
    index = str(index)
    
    node_manager.delete_node(index)
    return {'status': 'good'}
    

@app.route('/get_relationship_page', methods = ['GET'])
def get_relationship_page():
        
    index = f.request.args.get('index')
    n = node_manager.load_node_from_id(index)

    return f.render_template('relationship_page.html', node = n)





@app.route('/get_relationships', methods = ['GET'])
def get_relationships():
        
    index = f.request.args.get('index')
    kind = f.request.args.get('kind')
    
    n = node_manager.load_node_from_id(index)
    
    assert kind in ['parents', 'children']
    if kind  == 'parents':
        relationships= n.get_parents()
        
    if kind == 'children':
        relationships = n.get_children()

    return f.render_template('relationship_results.html', node = n ,kind = kind, relationships = relationships)

@app.route('/search_unrelated', methods = ['POST'])
def search_unrelated():
    index = f.request.form.get('index')
    kind = f.request.form.get('kind')
    search_text = f.request.form.get('search_text', "")
    n = node_manager.load_node_from_id(index)

    
    found_nodes = node_manager.search_nodes(search_text)
    
    if kind  == 'parents':
        relationships= n.get_parents()
        
    if kind == 'children':
        relationships = n.get_children()
        
    final_nodes = []
    
    for node in found_nodes:
        if node not in relationships:
            if node != n:
                final_nodes.append(node)
    
    return f.render_template('unrelated_nodes.html', nodes = final_nodes)

@app.route('/add_relationship', methods = ['POST'])
def add_relationship():
    source_node_id = f.request.form['source_node_id']
    target_node_id = f.request.form['target_node_id']
    kind = f.request.form['kind']
    app.logger.info(kind)
    source_node = node_manager.load_node_from_id(source_node_id)
    target_node = node_manager.load_node_from_id(target_node_id)
    
    assert kind in ['children', 'parents']
    if kind == 'children':
        source_node.add_child(target_node)
        
    if kind == 'parents':
        source_node.add_parent(target_node)
        
    return  {'status': 'good'}
    
@app.route('/remove_relationship', methods = ['POST'])
def remove_relationship():
    source_node_id = f.request.form['source_node_id']
    target_node_id = f.request.form['target_node_id']
    kind = f.request.form['kind']
    app.logger.info(kind)
    source_node = node_manager.load_node_from_id(source_node_id)
    target_node = node_manager.load_node_from_id(target_node_id)
    
    assert kind in ['children', 'parents']
    if kind == 'children':
        node_manager.delete_connection(source_node,target_node )
        
    if kind == 'parents':
        node_manager.delete_connection(target_node, source_node)
        
    return  {'status': 'good'}


@app.route('/show_all_related', methods = ['GET'])
def show_all_related():
    """ 
    Only Returns non-direct parents and non direct children
    """
    index = f.request.args.get('index')
    kind = f.request.args.get('kind')
    
    app.logger.info('|' + index + '| - ' + kind)
    
    assert kind in ['parents', 'children']
    n = node_manager.load_node_from_id(index)
    
    if kind == 'parents':
        direct_parents = n.get_parents()
        all_parents = n.get_upstream([])
        result = []
        for node in all_parents:
            if node not in direct_parents:
                result.append(node)
        
    if kind == 'children':
        direct_children = n.get_children()
        app.logger.info(direct_children)
        all_children= n.get_downstream([])
        app.logger.info(all_children)
        result = []
        for node in all_children:
            if node not in direct_children:
                result.append(node)
    
    for x in result:
        app.logger.info(x)
        
    node_count = len(result)
    return f.render_template('indirectly_related_nodes.html', nodes = result, kind = kind, node_count = node_count)
    
    

@app.route('/get_help')
def get_help():
    
    return f.render_template('Help.html')

if __name__ == "__main__":
        app.run(debug = True)
