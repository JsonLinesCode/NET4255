from flask import Flask
from datetime import datetime
import socket

app = Flask(__name__)

@app.route("/")
def index():
    now = datetime.now()
    hostname = socket.gethostname()
    return f"""
    <html>
    <head><title>Flask App 1</title></head>
    <body>
        <h1>Net4255 Challenge 4</h1>
        <h2>Josselin ROBERT</h2>
        <h3>Version V2</h3>
        <p>Current Date: {now}</p>
        <p>Hostname: {hostname}</p>
        <p>Type: <b>Without a Database</b></p>
    </body>
    </html>
    """
