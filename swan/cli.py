import argparse
import sys
import re

from swan.clone import clone_dataset
from swan.add import add_files, remove_files
from swan.commit import commit
from swan.push import push
from swan.config import set_api_token

DATASET_PREFIX_URL = "https://lagrangedao.org/datasets"
CLONE_CMD = "clone"
ADD_CMD = "add"
COMMIT_CMD = "commit"
PUSH_CMD = "push"
CFG_CMD = "config"
RM_CMD = "remove"

def dataset_from_url(url, arg):
    url_format = "https:\/\/lagrangedao\.org\/datasets\/\w+$" #regex pattern url must follow

    if not bool(re.match(url_format, url)):
        raise argparse.ArgumentError(arg, "Dataset URL must be in the format of: https://lagrangedao.org/datasets/<dataset_name>")

    dataset_name = url.split(DATASET_PREFIX_URL)[1].replace('/', '')
    return dataset_name

def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(title="Commands", metavar='', dest="selected_cmd", required=True)

    #clone command
    clone_parer = subparser.add_parser(CLONE_CMD, help = f"Clone a lagrange dataset into the current directory. \"swan {CLONE_CMD} -h\" for additional info.")
    clone_arg = clone_parer.add_argument('dataset_url', help="Dataset URL in the format of: https://lagrangedao.org/datasets/<dataset_name>")
    
    #add command
    add_parer = subparser.add_parser(ADD_CMD, help = f"Add files to be comitted. \"swan {ADD_CMD} -h\" for additional info")
    add_arg = add_parer.add_argument("files", nargs="+",  help="One or more files to be added. The file paths should be relative to current working directory.")

    #commit command
    commit_parer = subparser.add_parser(COMMIT_CMD, help = f"Commit added files. \"swan {COMMIT_CMD} -h\" for additional info")
    commit_arg = commit_parer.add_argument("-m",  help="Commit message", required=True)

    #push command
    push_parser = subparser.add_parser(PUSH_CMD, help = f"Push comitted files to designated dataset. \"swan {PUSH_CMD} -h\" for additional info")
    push_arg = push_parser.add_argument('dataset_url', help="Dataset URL in the format of: https://lagrangedao.org/datasets/<dataset_name>")

    #config command
    cfg_parser = subparser.add_parser(CFG_CMD, help = f"Edit config. \"swan {CFG_CMD} -h\" for additional info")
    api_token_arg = cfg_parser.add_argument('--api-token', help="API token needed for permissions to upload to dataset.")

    #remove command
    remove_parser = subparser.add_parser(RM_CMD, help = f"Remove added files. \"swan {RM_CMD} -h\" for additional info")
    remove_arg = remove_parser.add_argument("files", nargs="+",  help="Files to be removed. The file paths should be relative to current working directory.")

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(-1)

    args = parser.parse_args() 
    cmd = args.selected_cmd

    if cmd == CLONE_CMD:
        url = args.dataset_url
        url_format = "https:\/\/lagrangedao\.org\/datasets\/\w+$"

        if not bool(re.match(url_format, url)):
            raise argparse.ArgumentError(clone_arg, "Dataset URL must be in the format of: https://lagrangedao.org/datasets/<dataset_name>")

        dataset_name = url.split(DATASET_PREFIX_URL)[1].replace('/', '')
        clone_dataset(dataset_name)
    elif cmd == ADD_CMD:
        add_files(args.files)
    elif cmd == COMMIT_CMD:
        commit(args.m)
    elif cmd == PUSH_CMD:
        dataset_name = dataset_from_url(args.dataset_url, push_arg)
        push(dataset_name)
    elif cmd == CFG_CMD:
        if args.api_token:
            set_api_token(args.api_token)
    elif cmd == RM_CMD:
        remove_files(args.files)
        

if __name__ == "__main__":
    main()