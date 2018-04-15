#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, argparse, string, datetime, time
import logging, logging.config
import glob
import time

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/script
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                   # /home/pi/Dev
envname = os.path.basename(envpath)                      # Dev

#logfile_base = os.path.join(currentpath, 'log')
logfile_base = currentpath

# import Database API
chaudiereapp = os.path.join(projectpath, 'chaudiereapp')
print chaudiereapp
sys.path.append(chaudiereapp)
from newapi import createChaudiere

def get_last_watt():
    return 0

def get_temp():
    return 0

def main():
    while True:
        get_temp()
        get_last_watt()
#        createChaudiere()

if __name__ == '__main__':
    
    # PARSE ARGS
    parser = argparse.ArgumentParser(description = "Rpi gets info from Uno serial", epilog = "" )
    parser.add_argument("-v",
                          "--verbose",
                          help="increase output verbosity",
                          action="store_true")
    args = parser.parse_args()

    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.CRITICAL
    
    # SET LOGGER
    logger = logging.getLogger(__name__)
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s | %(name)s | %(filename)s | %(levelname)s | %(funcName)s | %(message)s"
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": loglevel,
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },

            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": os.path.join(logfile_base, __file__+'_info.log'),
                "maxBytes": 5000,
                "backupCount": 0,
                "encoding": "utf8"
            },

            "error_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": os.path.join(logfile_base, 'get_temp_error.log'),
                "maxBytes": 5000,
                "backupCount": 0,
                "encoding": "utf8"
            }
        },

        "loggers": {
            "my_module": {
                "level": "ERROR",
                "handlers": ["console"],
                "propagate": "no"
            }
        },

        "root": {
            "level": "INFO",
            "handlers": ["console", "info_file_handler", "error_file_handler"]
        }
    })

    # CALL MAIN
    main()