import os, sys, argparse, string, datetime, time
import logging, logging.config
import serial
from serial.serialutil import SerialException

import logger_config
from get_temp import api_get_temp_values
from get_watt import api_get_watt_values

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/script
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                   # /home/pi/Dev
envname = os.path.basename(envpath)                      # Dev

logfile_base = os.path.join(currentpath, 'log')

# import Database API
chaudiereapp = os.path.join(projectpath, 'chaudiereapp')
sys.path.append(chaudiereapp)
from db_api import createSensorRecord

# SET LOGGER
logger = logging.getLogger(__name__)
"""
logger.critical("critical")
logger.error("error")
logger.warning("warning")
logger.info("info")
logger.debug("debug")
"""


"""
Get last line of wattbuffer
verify data is fresh
return values
"""
def get_last_watt():
    return api_get_watt_values()

def get_temp():
    return api_get_temp_values()

def main():
    while True:
        watts = get_last_watt()
        temps = get_temp()
        if createSensorRecord(datetime.datetime.now(), temps[0], temps[1], watts[0], watts[1], watts[2]):
            logger.info("createSensorRecord : Ok")
        else:
            logger.warning("createSensorRecord : Fail")
        time.sleep(2)

if __name__ == '__main__':
    # CALL MAIN
    main()