from functools import lru_cache

import json
import os

# Load config only once
@lru_cache()
def get():
    config_name = os.getenv('CMPT371_ANALYTICS_BACKEND_CONF', 'dev.json')
    with open('config/' + config_name, 'r') as config_file:
        return json.load(config_file)
