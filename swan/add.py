import os
import json
from datetime import datetime

from swan.common import DATA_FILE, ADDED, LAST_UPDATED, get_dir_data


def add_files(files):

    nonfiles = []
    for f in files:
        if not os.path.isfile(f):
            nonfiles.append(f)

    if len(nonfiles) > 0:
        print(f"Attempted to add invalid files: {nonfiles}")
        return

    cwd = os.getcwd();
    data = get_dir_data(cwd)
    
    data[cwd][ADDED] = list(set(data[cwd][ADDED] + files))
    data[cwd][LAST_UPDATED] = str(datetime.now())

    json.dump(data, open(DATA_FILE, "w"))


def remove_files(files):
    nonfiles = []
    for f in files:
        if not os.path.isfile(f):
            nonfiles.append(f)

    if len(nonfiles) > 0:
        print(f"Attempted to remove invalid/nonexistant files: {nonfiles}")
        return

    cwd = os.getcwd();
    data = get_dir_data(cwd)

    added_files = data[cwd][ADDED]

    for file in files:
        added_files.remove(file)

    data[cwd][ADDED] = added_files
    data[cwd][LAST_UPDATED] = str(datetime.now())

    json.dump(data, open(DATA_FILE, "w"))
            