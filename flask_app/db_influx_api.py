# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import sys
import logging
import time
from datetime import datetime
import json

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/flask_app
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere

# import and get logger
logger_directory = os.path.join(projectpath, 'logger')
sys.path.append(logger_directory)
import logger_stdout
logger = logging.getLogger(__name__)

def add_measures_influx(influx_client, temp0, temp1, temp2, temp3, watt0, watt1, watt2, watt3):
    logging.info("Adding measure to influx")
    point = {
        "measurement": 'snapshot',
        "tags": {
            # identification de la sonde et du compteur
            "host": "raspberry",
            "region": "chaudiere"
        },
        "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fields": {
            "eau": temp0,
            "fume": temp1,
            "boitier": temp2,
            "primaire": watt2,
            "secondaire": watt0,
            "allumage": watt1,
            "alim": watt3
        }
    }
    points = []
    points.append(point)
    influx_client.write_points(points)
