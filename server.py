import os
from flask import Flask, render_template, request, redirect, flash, url_for, session, send_from_directory
from werkzeug.utils import secure_filename

server = Flask(__name__)

server.secret_key = os.urandom(24)
devices = []

@server.route("/")
def index():
    if 'device' not in session:
        session['device'] = os.urandom(10).hex()
        session['joined'] = True

    if session['device'] not in devices:
        devices.append(session['device'])
    
    session_id = f"Session ID: {session['device']}"

    return render_template('index.html', session_id=session_id, devices=devices)

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