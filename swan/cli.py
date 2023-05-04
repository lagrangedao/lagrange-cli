import argparse
import sys
import re

from swan.clone import clone_dataset

DATASET_PREFIX_URL = "https://lagrangedao.org/datasets"

def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(title="Commands", metavar='')

    #Clone command
    clone_parer = subparser.add_parser("clone", help = "\"swan clone -h\" for additional info")
    clone_arg = clone_parer.add_argument('dataset_url', help="Dataset URL in the format of: https://lagrangedao.org/datasets/<dataset_name>")

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(-1)

    args = parser.parse_args() 

    if args.dataset_url:
        url = args.dataset_url
        url_format = "https:\/\/lagrangedao\.org\/datasets\/\w+$"

        if not bool(re.match(url_format, url)):
            raise argparse.ArgumentError(clone_arg, "Dataset URL must be in the format of: https://lagrangedao.org/datasets/<dataset_name>")

        dataset_name = url.split(DATASET_PREFIX_URL)[1].replace('/', '')
        clone_dataset(dataset_name)
