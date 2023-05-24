import os
import requests

from lag.common import get_dir_data, COMMITS, FILES, LAGRANGE_API_URL, get_config, STATUS_200_OK
from lag.config import get_api_token

#get hash of latest (most recent) commit
def get_latest_commit(data, cwd):
    latest_commit = None
    cwd_commits = data[cwd][COMMITS]

    for commit in cwd_commits:
        if latest_commit is None or cwd_commits[latest_commit]["CreatedAt"] < cwd_commits[commit]["CreatedAt"]:
            latest_commit = commit

    return latest_commit

def push(name, url_type):
    api_token = get_api_token()
    if api_token == None:
        print("Please set your api token with \"lag config --api-token <YOUR_TOKEN>\"")
        return

    cwd = os.getcwd()
    data = get_dir_data(cwd)

    latest_commit = get_latest_commit(data, cwd)

    if latest_commit == None:
        print("There currently are no commits to push")
        return

    files = data[cwd][COMMITS][latest_commit][FILES]

    files_data = []
    for filename in files:
        with open(filename, 'rb') as f:
            files_data.append(('file', (filename, f.read())))
    
    print(f"Uploading files to {url_type[:-1]}...")

    if url_type == "spaces":
        url_type = "spaces_task"

    if url_type == "datasets":
        url_type = "datasets_api"

    res = requests.put(
        LAGRANGE_API_URL + f"/{url_type}/" + name + "/files", 
        files=files_data,
        headers = {"Authorization" : "Bearer " + api_token}
        )

    if res.status_code != STATUS_200_OK:
        print(f"An error occured when pushing the files. Status code {res.status_code}")
    else:
        print(f"Push to {name} complete.")