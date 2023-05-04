from concurrent.futures import ProcessPoolExecutor
import os
import requests

STATUS_200_OK = 200
LAGRANGE_API_URL = "https://api.lagrangedao.org"

# Download and write files 
def download_and_write_files(files_lst):
    for f in files_lst:
        filename = f['name'].split('/datasets/')[1]

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

# Clone provided dataset
def clone_dataset(dataset_name):
    res = requests.get(LAGRANGE_API_URL + "/datasets/" + dataset_name)
    if(res.status_code != STATUS_200_OK):
        raise Exception("An error occured when trying to retrieve dataset")

    os.makedirs(dataset_name, exist_ok=True)

    #initialize concurrency structures
    files_lst = res.json()['data']['files']
    n_workers = 8
    chunksize = round(len(files_lst) / n_workers)
    futures = []

    #Concurrently batch process the files
    try:
        with ProcessPoolExecutor(n_workers) as exe:
            for i in range(0, len(files_lst), chunksize):
                files = files_lst[i:(i + chunksize)]
                futures.append(exe.submit(download_and_write_files, files))
    except KeyboardInterrupt:
        for f in futures:
            f.cancel()