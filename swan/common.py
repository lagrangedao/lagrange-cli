import os
import json
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

def create_new_workspace(root):
    f = open(DATA_FILE, "r")
    data = json.load(f)

    data[root] = {}
    data[root][ADDED] = []
    data[root][COMMITS] = {}
    data[root][LAST_UPDATED] = str(datetime.now())

    json.dump(data, open(DATA_FILE, "w"))
    f.close()

def get_dir_data(cwd):
    data_file = open(DATA_FILE, "r")
    data = json.load(data_file)

    if cwd not in data:
        create_new_workspace(cwd)
        data_file = open(DATA_FILE, "r")
        data = json.load(data_file)
    
    data_file.close()

    return data

def get_config():
    cfg_file = open(CFG_FILE, "r");
    cfg = json.load(cfg_file)

    cfg_file.close()
    return cfg
