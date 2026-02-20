import os
from flask import Flask, render_template, request, redirect, flash, url_for, session, send_from_directory, jsonify
from werkzeug.utils import secure_filename

server = Flask(__name__)

server.secret_key = os.urandom(24)

UPLOAD_DIR = os.path.join(server.root_path, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

devices = []
pending_files = {}

@server.route("/")
def index():
    if 'device' not in session:
        session['device'] = os.urandom(10).hex()
        session['joined'] = True

    if session['device'] not in devices:
        devices.append(session['device'])
    
    device_index = devices.index(session['device'])
    device_info = f"You are on device number: {devices.index(session['device'])}"

    pending_files.setdefault(device_index, [])

    enum_devices = list(enumerate(devices))
    return render_template('index.html', device_index=device_index, device_num=device_info, devices=enum_devices)

@server.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify(error="no file"), 400
        
        file = request.files['file']
        receiver_device = int(request.form.get('devices'))

        if file.filename == '':
            return jsonify(error="empty filename"), 400
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_DIR, filename))

        pending_files.setdefault(receiver_device, []).append(filename)

        return jsonify(ok=True)

@server.route("/inbox")
def inbox():
    if "device" not in session:
        return jsonify([])
    
    device_index = devices.index(session["device"])
    files = pending_files.get(device_index, [])
    return jsonify([{"name": f, "sender": device_index} for f in files])

@server.route("/download/<int:receiver>/<filename>")
def download(receiver, filename):
    if "device" not in session:
        return redirect(url_for("index"))

    device_index = devices.index(session["device"])

    if device_index != receiver:
        return redirect(url_for("index"))

    if filename not in pending_files.get(receiver, []):
        return redirect(url_for("index"))

    pending_files[receiver].remove(filename)

    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)