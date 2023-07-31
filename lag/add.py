import os
import json
from datetime import datetime

from lag.common import DATA_FILE, ADDED, LAST_UPDATED, get_dir_data


def add_files(files):

    if len(files) == 1 and files[0] == '.':
        files = []
        for path, _, files2 in os.walk('.'):
            for name in files2:
                raw_filepath = os.path.join(path, name);
                filepath = raw_filepath.split(f".{os.sep}")[1]
                files.append(filepath)

    else:
        nonfiles = []
        for f in files:
            if not os.path.isfile(f):
                nonfiles.append(f)

        if len(nonfiles) > 0:
            print(f"Attempted to add invalid files: {nonfiles}")
            return

    cwd = os.getcwd();
    data = get_dir_data(cwd)

    # If cwd isn't initialized, get_dir_data prints error and returns None
    if data is None:
        return

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

    # If cwd isn't initialized, get_dir_data prints error and returns None
    if data is None:
        return

    added_files = data[cwd][ADDED]
    new_added_files = added_files
    for file in files:
        if file in new_added_files:
            new_added_files.remove(file)
        else:
            print(f"{file} is not added.")

    data[cwd][ADDED] = new_added_files
    data[cwd][LAST_UPDATED] = str(datetime.now())

    json.dump(data, open(DATA_FILE, "w"))
            