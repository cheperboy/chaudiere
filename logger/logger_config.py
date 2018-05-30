import os
import logging.config
import yaml

#CONFIG_TYPE = "YAML"
CONFIG_TYPE = "PY"

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/logger
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                   # /home/pi/Dev
envname = os.path.basename(envpath)                      # Dev

logfile_base = os.path.join(envpath, 'log')
error_logfile_name = os.path.join(logfile_base, 'simple_log.log')
debug_logfile_name = os.path.join(logfile_base, 'full_log.log')

CONFIG_PY = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s | %(filename)s | %(levelname)s | %(funcName)s | %(message)s"
        },
        "simple": {
            "format": "%(filename)s | %(levelname)s | %(message)s"
        }
    },

#handler level overrides the logger level
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },

        "error_log": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "default",
            "filename": error_logfile_name,
            "maxBytes": 1000000,
            "backupCount": 10,
            "encoding": "utf8"
        },
        "debug_log": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filename": debug_logfile_name,
            "maxBytes": 1000000,
            "backupCount": 10,
            "encoding": "utf8"
        },
    },

# logger level is always set to the lower level => the logger sends all stream. 
# then the stream will be filtered be the handler level

    "root": {
        "level": "DEBUG",
        "handlers": ["console", "error_log", "debug_log"]
    },
}

if CONFIG_TYPE == "YAML":
    config_file = 'logging.yaml'
    default_level = logging.INFO
    if os.path.exists(config_file):
        with open(config_file, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
    
if CONFIG_TYPE == "PY":
    logging.config.dictConfig(CONFIG_PY)

# Example of config.yaml:
"""
version: 1
disable_existing_loggers: False
formatters:
  simple:
    format: "%(asctime)s | %(name)s | %(filename)s | %(levelname)s | %(funcName)s | %(message)s"

#handler level overrides the logger level
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: simple
    stream: ext://sys.stdout

  file_handler:
    class: logging.handlers.RotatingFileHandler
    level: INFO
    formatter: simple
    filename: log/logger.log
    maxBytes: 1000000
    backupCount: 1
    encoding: utf8

# logger level is overriden by the handler level
# logger propagate: if yes, root logger records also this logger datas
loggers:
  create_data:
    level: DEBUG
    handlers: [console, file_handler]
    propagate: no

  get_temp:
    level: DEBUG
    handlers: [console, file_handler]
    propagate: no

  get_watt:
    level: DEBUG
    handlers: [console, file_handler]
    propagate: no

root:
    level: DEBUG
    handlers: [console, file_handler]

#CRITICAL
#ERROR
#WARNING
#INFO
#DEBUG
"""