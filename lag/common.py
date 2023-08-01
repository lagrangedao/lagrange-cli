import os
import json
import requests
import re
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
CFG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
ADDED = "Added"
COMMITS = "Commits"
COMITTED = "Committed"
LAST_UPDATED = "Updated"
COMMIT_MSG = "CommitMessage"
STATUS_200_OK = 200
LAGRANGE_API_URL = "https://api.lagrangedao.org"
FILES = "Files"
STATUS_200_OK = 200
PREFIX_URL = "https://lagrangedao.org/"
ORIGIN_URL = "Origin"
URL_PATTERN =  "https:\/\/lagrangedao\.org\/(datasets|spaces|models)\/\w+\/\w+(-\w+)*$" #regex pattern url must follow

#Precondition: url follows URL_PATTERN
def data_from_url(url):
    return url.split(PREFIX_URL + url_type(url))[1].split("/")[1:3]

#Precondition: url follows URL_PATTERN
def url_type(url):
    match = re.match(URL_PATTERN, url)
    return match.group(1)

def create_new_workspace(root, origin_url):
    f = open(DATA_FILE, "r")
    data = json.load(f)

    data[root] = {}
    data[root][ORIGIN_URL] = origin_url
    data[root][ADDED] = []
    data[root][COMMITS] = {}
    data[root][LAST_UPDATED] = str(datetime.now())

    json.dump(data, open(DATA_FILE, "w"))
    f.close()

def get_dir_data(cwd):
    data_file = open(DATA_FILE, "r")
    data = json.load(data_file)

    if cwd not in data:
        print(f"Please clone a Lagrange dataset/model/space to initialize this repository.")
        return None
    
    data_file.close()

    return data

def get_config():
    cfg_file = open(CFG_FILE, "r");
    cfg = json.load(cfg_file)

    cfg_file.close()
    return cfg

# Download and write files 
def download_and_write_files(files_lst, url_type, include_prefix = True):
    for f in files_lst:
        filename = f['name'].split(f"/{url_type}/")[1]
        if not include_prefix:
            parts = filename.split("/")
            filename = "/".join(parts[1:])

        if len(os.path.dirname(filename)) > 1:
            os.makedirs(os.path.dirname(filename), exist_ok=True)

        print(f"Downloading: {filename}")
        url = f['url']
        with open(filename, "wb") as file:
            content_res = requests.get(url)
            if(content_res.status_code == STATUS_200_OK):
                file.write(content_res.content)
            else:
                print(f"Error retrieving and/or writing {filename}")
            file.close()
