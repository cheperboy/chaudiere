import os
import logging.config

import yaml

config_file = 'logging.yaml'
default_level = logging.INFO
if os.path.exists(config_file):
    with open(config_file, 'rt') as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
else:
    logging.basicConfig(level=default_level)