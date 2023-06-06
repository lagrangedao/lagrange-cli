from lag.common import DATA_FILE, COMMITS, COMMIT_MSG, ADDED, LAST_UPDATED, get_dir_data
import os
import hashlib
import json
from datetime import datetime


def hash_files(filepaths):
    hash_value = hashlib.sha256()

    for filepath in filepaths:
        with open(filepath, 'rb') as f:
            contents = f.read()
            hash_value.update(contents)

    return hash_value.hexdigest()


def commit(commit_msg):
    cwd = os.getcwd();
    data = get_dir_data(cwd)
    if data is None:
        return


    added_files = data[cwd][ADDED]

    if len(added_files) == 0:
        print("The current working directory has no added files to commit. \"lag add -h\" for more info. ")
        return

    # If windows file path, change to linux file path
    if os.sep == "\\":
        added_files =  list(map( lambda f : f.replace("\\", "/"), added_files))

    hash = hash_files(added_files)

    #create new commit
    commit = {
        "Files": added_files,
        COMMIT_MSG : commit_msg,
        "CreatedAt": str(datetime.now())
    }
    data[cwd][COMMITS][hash] = commit

    data[cwd][ADDED] = []
    data[cwd][LAST_UPDATED] = str(datetime.now())

    json.dump(data, open(DATA_FILE, "w"))
    