import os, sys, argparse, string, datetime, time
import logging, logging.config
import serial
from serial.serialutil import SerialException

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/script
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                   # /home/pi/Dev
envname = os.path.basename(envpath)                      # Dev

# import sensors API
from get_temp import api_get_temp_values
from get_watt import api_get_watt_values

# import Database API
chaudiereapp = os.path.join(projectpath, 'chaudiereapp')
sys.path.append(chaudiereapp)
from db_api import createSensorRecord

# SET LOGGER
import logger_config
logger = logging.getLogger(__name__)

# Global variables
count_serial_port_fail = 0

"""
if serial port fail
the following command in console reopen the port and resolves the problem
ls /dev/tty
"""
def get_watt():
    return api_get_watt_values()

def get_temp():
    return api_get_temp_values()

def main():
    while True:
        watts = get_watt()
        temps = get_temp()
        dt = datetime.datetime.now()
        ret = createSensorRecord(dt, temps[0], temps[1], temps[2], watts[0], watts[1], watts[2], watts[3])
        if ret:
            logger.debug(ret)
            logger.info(str(dt)+" createSensorRecord : Ok")
        else:
            logger.warning("createSensorRecord : Fail")
        time.sleep(2)

if __name__ == '__main__':
    # CALL MAIN
    main()