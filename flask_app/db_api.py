# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import sys
import logging
from datetime import datetime, timedelta

from app import create_app, db
from app.models import Chaudiere

from app import create_app
app = create_app().app_context().push()

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/flask_app
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere

# import and get logger
logger_directory = os.path.join(projectpath, 'logger')
sys.path.append(logger_directory)
import logger_stdout
logger = logging.getLogger(__name__)

def createSensorRecord(timestamp, temp0, temp1, temp2, temp3, watt0, watt1, watt2, watt3):
    try:
        entry = Chaudiere(timestamp, temp0, temp1, temp2, temp3, watt0, watt1, watt2, watt3, None, None, None)
        db.session.add(entry)
        db.session.commit()
    except Exception as e:
        logger.error("generic Error" + str(e.message))
        return False
    else:
        return True
