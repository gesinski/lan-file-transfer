from flask import Flask
from flask import render_template

server = Flask(__name__)

@server.route("/")
def index(name=None):
    return render_template('index.html', person=name)
