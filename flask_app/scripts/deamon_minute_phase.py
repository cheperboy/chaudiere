#!/usr/bin/env python

"""
## Summary

language: Python 3 
script: deamon_minute_phase.py
Suposed to be deamonized by supervisord
Call archive_minute and process_phase then sleep two minute

## supervisor call :

    /home/pi/Envs/dev/bin/python /home/pi/Dev/chaudiere/flask_app/scripts/deamon_minute_phase.py

"""

import sys
import os
import click
import logging
from time import sleep

from archive_minute import process_archive_minute
from process_phase import process_phase

currentpath = os.path.abspath(os.path.dirname(__file__))    # /home/pi/Dev/chaudiere/flaskapp/scripts
flaskapp = os.path.dirname(currentpath)                     # /home/pi/Dev/chaudiere/flaskapp
projectpath = os.path.dirname(flaskapp)                     # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                      # /home/pi/Dev
envname = os.path.basename(envpath)                         # Dev

app_path = os.path.join(flaskapp, 'app')
sys.path.append(flaskapp)
from app import db
from app.models import Chaudiere, ChaudiereMinute
from app import create_app
app = create_app().app_context().push()

###############################################################################
# Configure logger
###############################################################################
logger_directory = os.path.join(projectpath, 'logger')
sys.path.append(logger_directory)
import logger_stdout
logger = logging.getLogger(__name__)


# Script Constants
DEAMON_SLEEP = 60 # do nothing during 1 minutes

@click.command()
@click.option('-d', '--debug',          type=click.BOOL,        help='print debug info')
#########################################
def main_function(debug):
#########################################
    """ Call archive_minute and process_phase then sleep two minute
    """
    try:
        while (True):
            logger.info('starting task')
            process_archive_minute(mode='normal')
            process_phase(mode='normal')
            logger.info('task done. sleeping {0}s.'.format(DEAMON_SLEEP))
            sleep(DEAMON_SLEEP)
    except KeyboardInterrupt as e:
        logger.warning(f'Stopped by system, Stopping process')
    finally:
        logger.warning(f'Stop process')
        
if __name__ == '__main__':
    logger.info('starting processus')
    main_function()
