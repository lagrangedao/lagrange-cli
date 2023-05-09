import argparse
import sys
import re

from swan.clone import clone
from swan.add import add_files, remove_files
from swan.commit import commit
from swan.push import push
from swan.config import set_api_token

PREFIX_URL = "https://lagrangedao.org/"
CLONE_CMD = "clone"
ADD_CMD = "add"
COMMIT_CMD = "commit"
PUSH_CMD = "push"
CFG_CMD = "config"
RM_CMD = "remove"
URL_HELP = "URL must be in the format of: https://lagrangedao.org/<datasets or spaces or models>/<name>"
URL_PATTERN =  "https:\/\/lagrangedao\.org\/(datasets|spaces|models)\/\w+(-\w+)*$" #regex pattern url must follow


#Precondition: url follows URL_PATTERN
def name_from_url(url):
    return url.split(PREFIX_URL + url_type(url))[1].replace('/', '')

#Precondition: url follows URL_PATTERN
def url_type(url):
    match = re.match(URL_PATTERN, url)
    return match.group(1)

def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(title="Commands", metavar='', dest="selected_cmd", required=True)

    #clone command
    clone_parer = subparser.add_parser(CLONE_CMD, help = f"Clone a lagrange dataset or space or model into the current directory. \"swan {CLONE_CMD} -h\" for additional info.")
    clone_arg = clone_parer.add_argument('url', help=URL_HELP)
    
    #add command
    add_parer = subparser.add_parser(ADD_CMD, help = f"Add files to be comitted. \"swan {ADD_CMD} -h\" for additional info")
    add_arg = add_parer.add_argument("files", nargs="+", 
        help="""
        One or more files to be added. The file paths should be relative to current 
        working directory. \"swan add .\" to add all files in current directory
        and all subdirectories.
        """)

    #commit command
    commit_parer = subparser.add_parser(COMMIT_CMD, help = f"Commit added files. \"swan {COMMIT_CMD} -h\" for additional info")
    commit_arg = commit_parer.add_argument("-m",  help="Commit message", required=True)

    #push command
    push_parser = subparser.add_parser(PUSH_CMD, help = f"Push comitted files to designated dataset/space/model. \"swan {PUSH_CMD} -h\" for additional info")
    push_arg = push_parser.add_argument('url', help=URL_HELP)

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
        if not bool(re.match(URL_PATTERN, args.url)):
            raise argparse.ArgumentError(clone_arg, URL_HELP)

        name = name_from_url(args.url)
        urlType = url_type(args.url)
        clone(name, urlType)
    elif cmd == ADD_CMD:
        add_files(args.files)
    elif cmd == COMMIT_CMD:
        commit(args.m)
    elif cmd == PUSH_CMD:
        if not bool(re.match(URL_PATTERN, args.url)):
            raise argparse.ArgumentError(clone_arg, URL_HELP)

        name = name_from_url(args.url)
        urlType = url_type(args.url)
        push(name, urlType)
    elif cmd == CFG_CMD:
        if args.api_token:
            set_api_token(args.api_token)
    elif cmd == RM_CMD:
        remove_files(args.files)
        

if __name__ == "__main__":
    main()