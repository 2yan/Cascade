

from flask import Flask
import flask as f



app = Flask(__name__)

@app.route('/')
def hello_world():
    return f.render_template('home.html') 







if __name__ == "__main__":
        app.run(debug = True)