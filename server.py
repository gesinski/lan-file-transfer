import os
from flask import Flask, render_template, request, redirect, flash, url_for, session, send_from_directory
from flask_session import Session
from werkzeug.utils import secure_filename
from datetime import timedelta

server = Flask(__name__)

server.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
server.config["SESSION_TYPE"] = "filesystem" 
Session(server)

@server.route("/")
def index():
    return render_template('index.html')

@server.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(server.root_path, 'uploads', filename))
        return redirect(url_for('upload_file', name=filename))

@server.route("/download")
def download():
    filename = "count"
    file_path = os.path.join(server.root_path, 'uploads')

    return send_from_directory(file_path, filename, as_attachment=True)