# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import sys
import logging
import time
from datetime import datetime
import json
from influxdb import InfluxDBClient

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/flask_app
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere

# import and get logger
logger_directory = os.path.join(projectpath, 'logger')
sys.path.append(logger_directory)
import logger_stdout
logger = logging.getLogger(__name__)

# connexion a la base de données InfluxDB
client = InfluxDBClient('localhost', 8086, username='admin', password='password')
DB_NAME = "chaudiere"
connected = False
while not connected:
    try:
        logging.info("Database %s exists?" % DB_NAME)
        if not {'name': DB_NAME} in client.get_list_database():
            logging.info("Database %s creation.." % DB_NAME)
            client.create_database(DB_NAME)
            logging.info("Database %s created!" % DB_NAME)
        client.switch_database(DB_NAME)
        logging.info("Connected to %s!" % DB_NAME)
    except Exception as e:
        logging.info('InfluxDB is not reachable. Waiting 5 seconds to retry.')
        time.sleep(5)
    else:
        connected = True


def add_measures_influx(timestamp, temp0, temp1, temp2, temp3, watt0, watt1, watt2, watt3):
    logging.info("Adding measure to influx %s" % timestamp)
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
    client.write_points(points)
