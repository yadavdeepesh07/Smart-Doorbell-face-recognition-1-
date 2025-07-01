import json
import os
from dotenv import load_dotenv

load_dotenv()

CONFIG_FILE = "config.json"

def get_env(key, default=None):
    return os.getenv(key, default)

def read_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def update_config(key, value):
    config = read_config()
    config[key] = value
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def get_config(key, default=None):
    return read_config().get(key, default)
