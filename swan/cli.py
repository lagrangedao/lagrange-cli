import argparse
import os
import requests
import sys
import re


DATASET_PREFIX_URL = "https://lagrangedao.org/datasets"
STATUS_200_OK = 200
LAGRANG_API_URL = "https://api.lagrangedao.org"


def clone_dataset(dataset_name):
    res = requests.get(LAGRANG_API_URL + "/datasets/" + dataset_name)
    if(res.status_code != STATUS_200_OK):
        raise Exception("An error occured when trying to retrieve dataset")

    os.makedirs(dataset_name, exist_ok=True)

    for f in res.json()['data']['files']:
        filename = f['name'].split('/datasets/')[1]
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        print(filename)
        url = f['url']
        with open(filename, "wb") as file:
            content_res = requests.get(url)
            if(content_res.status_code == STATUS_200_OK):
                file.write(content_res.content)
            else:
                print(f"Error retrieving and/or writing {filename}")
            file.close()

def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(title="Commands", metavar='' )

    #Clone command
    clone_parer = subparser.add_parser("clone", help = "\"swan clone -h\" for additional info")
    clone_arg = clone_parer.add_argument('dataset_url', help="Dataset URL in the format of: https://lagrangedao.org/datasets/<dataset_name>")

    if len(sys.argv) <= 1:
        parser.print_help()
        exit(-1)

    args = parser.parse_args() 

    if args.dataset_url:
        url = args.dataset_url
        url_format = "https:\/\/lagrangedao\.org\/datasets\/\w+$"

        if not bool(re.match(url_format, url)):
            raise argparse.ArgumentError(clone_arg, "Dataset URL must be in the format of: https://lagrangedao.org/datasets/<dataset_name>")

        dataset_name = url.split(DATASET_PREFIX_URL)[1].replace('/', '')
        clone_dataset(dataset_name)
