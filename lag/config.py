import json

from lag.common import get_config, CFG_FILE

API_TOKEN = "api_token"

def set_api_token(token):
    cfg = get_config()
    cfg[API_TOKEN] = token

    json.dump(cfg, open(CFG_FILE, "w"))

def get_api_token():
    cfg = get_config()
    return cfg[API_TOKEN]