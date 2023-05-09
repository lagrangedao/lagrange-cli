from concurrent.futures import ProcessPoolExecutor
import os
import requests

STATUS_200_OK = 200
LAGRANGE_API_URL = "https://api.lagrangedao.org"

# Download and write files 
def download_and_write_files(files_lst, url_type):
    for f in files_lst:
        filename = f['name'].split(f"/{url_type}/")[1]

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

# Clone provided dataset / space / model
def clone(name, url_type):
    res = requests.get(LAGRANGE_API_URL + f"/{url_type}/" + name)
    if(res.status_code != STATUS_200_OK):
        raise Exception(f"An error occured when trying to retrieve dataset. Status code: {res.status_code}.")

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