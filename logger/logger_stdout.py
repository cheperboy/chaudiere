import logging.config

CONFIG_PY = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "save": {
            "format": "%(asctime)s | %(filename)s | %(levelname)s | %(funcName)s | %(message)s"
        },
        "default": {
            "format": "%(filename)s | %(levelname)s | %(funcName)s | %(message)s"
        },
    },

#handler level overrides the logger level
    "handlers": {
        "info": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        },
        "error": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
            "formatter": "default",
            "stream": "ext://sys.stderr"
        },
    },

# root logger level is always set to the lower level => the root logger sends all stream. 
# then the stream will be filtered be the handler level

    "root": {
        "level": "DEBUG",
        "handlers": ["info", "error"]
    },
}

logging.config.dictConfig(CONFIG_PY)
