from concurrent.futures import ProcessPoolExecutor
import os
import requests
from lag.common import ORIGIN_URL, STATUS_200_OK, download_and_write_files, get_dir_data, data_from_url, url_type, LAGRANGE_API_URL

# Clone provided dataset / space / model
def pull():
    cwd = os.getcwd()
    data = get_dir_data(cwd)
    if data is None:
        return

    wallet_address, name = data_from_url(data[cwd][ORIGIN_URL])
    urlType = url_type(data[cwd][ORIGIN_URL])
    
    print(f"{LAGRANGE_API_URL}/{urlType}/{wallet_address}/{name}")
    res = requests.get(f"{LAGRANGE_API_URL}/{urlType}/{wallet_address}/{name}")
    if(res.status_code != STATUS_200_OK):
        raise Exception(f"An error occured when trying to pull code. Status code: {res.status_code}.")

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
                futures.append(exe.submit(download_and_write_files, files, urlType, False))
    except KeyboardInterrupt:
        for f in futures:
            f.cancel()
