from flask import Flask
from datetime import datetime
from pymongo import MongoClient
import socket
import os

app = Flask(__name__)

# Connect to MongoDB
# Host is 'mongo' as defined in docker-compose
    
mongo_url = os.environ.get('MONGO_URL', 'mongodb://mongo:27017/')
client = MongoClient(mongo_url)
db = client['net4255_db']
collection = db['access_logs']

@app.route("/")
def index():
    now = datetime.now()
    hostname = socket.gethostname()
    
    # Insert current access record
    record = {
        'date': now,
        'hostname': hostname,
        'message': 'Access from Flask App 2'
    }
    collection.insert_one(record)
    
    # Retrieve last 10 records
    last_records = list(collection.find().sort('_id', -1).limit(10))
    
    records_html = "<ul>"
    for r in last_records:
        records_html += f"<li>{r.get('date')} - {r.get('hostname')}</li>"
    records_html += "</ul>"

    return f"""
    <html>
    <head><title>Flask App 2</title></head>
    <body>
        <h1>Net4255 Challenge 4</h1>
        <h2>Josselin ROBERT</h2>
        <h3>Version V2</h3>
        <p>Current Date: {now}</p>
        <p>Hostname: {hostname}</p>
        <p>Type: <b>With Database (MongoDB)</b></p>
        <hr>
        <h4>Last 10 DB Records:</h4>
        {records_html}
    </body>
    </html>
    """
