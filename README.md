# LFT – Local Area Network File Transfer

## Overview

LFT (Local Area Network File Transfer) is a lightweight web-based application designed to transfer files between devices connected to the same local area network (LAN).

The project consists of:
- a **Python backend** built with Flask,
- a **frontend** implemented using Vanilla JavaScript, HTML, and CSS.

The application does not require any external services, user accounts, or internet access. All communication takes place entirely within the local network.

---

## How It Works

1. Each device that opens the website is assigned a **temporary device ID** stored in the session.
2. All connected devices are visible in a shared device list.
3. A user can select a target device and upload a file.
4. The uploaded file is stored on the server and assigned to the selected recipient.
5. The receiving device periodically checks its inbox and is notified when a file is available for download.
6. Files can only be downloaded by the intended recipient device.

This mechanism allows simple, fast, and controlled file transfers inside a LAN environment.

---

## Features

- Automatic device identification using sessions
- Live list of connected devices
- File upload to a specific target device
- Inbox system for received files
- Secure download access limited to the intended recipient
- No database required (in-memory storage)
- Works on desktop and mobile browsers
- No external dependencies beyond Python packages

---

# Installation

To avoid installing dependencies globally, it is recommended to use a Python virtual environment.

### 1. Create and activate a virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install required dependencies

```
pip install -r requirements.txt
```

---

## Usage

### Run the server

```
flask --app server run --host=0.0.0.0 --port=5000
```

### Access the application

From any device connected to the same local network, open a browser and navigate to:

```
http://<SERVER_IP>:5000
```

Example:

```
http://192.168.1.10:5000
```

## Network Requirements

- All devices must be connected to the same LAN
- The server device firewall must allow incoming connections on port 5000
- No port forwarding is required for local usage

## Limitations

- Device list and inbox data are stored in memory
- Restarting the server clears all state
- Not intended for large files or production use
- No encryption (LAN-only assumption)

## License

This project is provided for educational and personal use.
You are free to modify and extend it as needed.