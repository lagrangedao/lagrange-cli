from concurrent.futures import ProcessPoolExecutor
import os
import requests
import json
from lag.common import LAGRANGE_API_URL, STATUS_200_OK, PREFIX_URL, download_and_write_files, create_new_workspace

# Clone provided dataset / space / model
def clone(name, wallet_address, url_type):
    res = requests.get(f"{LAGRANGE_API_URL}/{url_type}/{wallet_address}/{name}")
    if(res.status_code != STATUS_200_OK):
        raise Exception(f"An error occured when trying to clone code. Status code: {res.status_code}.")

    origin_url = f"{PREFIX_URL}{url_type}/{wallet_address}/{name}"
    print(f"Cloning {name} into current directory...")
    create_new_workspace(os.path.join(os.getcwd(), name), origin_url)
    os.makedirs(name, exist_ok=True)

    #initialize concurrency structures
    files_lst = res.json()['data']['files']
    n_workers = 8
    chunksize = max(round(len(files_lst) / n_workers), 1)
    futures = []

    #Concurrently batch process the files
    try:
        with ProcessPoolExecutor(n_workers) as exe:
            for i in range(0, len(files_lst), chunksize):
                files = files_lst[i:(i + chunksize)]
                futures.append(exe.submit(download_and_write_files, files, url_type))
    except KeyboardInterrupt:
        for f in futures:
            f.cancel()
