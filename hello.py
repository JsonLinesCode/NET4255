from flask import Flask, request
import os
import socket
from datetime import datetime
import pymongo 
import urllib.parse
app = Flask(__name__)


NAME = "Josselin ROBERT"
PROJECT_NAME = "Ma boite de chocolats"
APP_VERSION = "2.0"
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://root:example@mongo:888")
mongo_client = pymongo.MongoClient(MONGO_URI)

VISITS_DB = "mydb"
VISITS_COLLECTION = "ips"

def build_from_tag_list(tags):
    final_page=""
    for tag in tags:
        final_page+="\n"+tag

    return "<!DOCTYPE html>\n<html><head><title>"+PROJECT_NAME+"</title></head><body>" + final_page + "</body></html>"

def add_visit_record():
    db = mongo_client[VISITS_DB]
    collection = db[VISITS_COLLECTION]
    new_record = {
        "ip": request.remote_addr,
        "date": datetime.now()
    }
    collection.insert_one(new_record)


## Add the latest visits
def show_latest_visits(limit_count):
    add_visit_record()
    db = mongo_client[VISITS_DB]
    collection = db[VISITS_COLLECTION]
    visits = collection.find().sort("date", -1).limit(limit_count)
    visit_tags = []
    for visit in visits:
        ip = visit.get("ip", "unknown")
        when = visit.get("date", "")
        visit_tags.append("<p>Visitor " + ip + " at " + str(when) + "</p>")
    return build_from_tag_list(visit_tags)


def construct_page():
    name_tag="<h3><u>My name is</u>: "+NAME+"</h3>"
    project_name_tag="<h3><u>My project name is </u>: "+PROJECT_NAME+"</h3>"
    app_version_tag="<h3><u>My app version is </u>: "+APP_VERSION+"</h3>"
    host_name_tag="<h3><u>My host name is:</u> " + urllib.parse.urlparse(request.host_url).netloc
    current_date="<h3><u>Current date is:</u> " + datetime.today().strftime('%d-%m-%Y')+"</h3>"
    latest_visits=show_latest_visits(10)

    return build_from_tag_list([name_tag, project_name_tag, app_version_tag, host_name_tag, current_date, latest_visits])


@app.route("/")
def hello_world():
    return construct_page()