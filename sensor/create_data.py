import click
import os, sys, argparse, string, datetime, time
import logging, logging.config
import serial
from serial.serialutil import SerialException
from random import randint

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/script
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                   # /home/pi/Dev
envname = os.path.basename(envpath)                      # Dev

# import sensors API
from get_temp import api_get_temp_values
from get_watt import api_get_watt_values

# import Database API from flask_app
flask_app_directory = os.path.join(projectpath, 'flask_app')
sys.path.append(flask_app_directory)
from db_api import createSensorRecord

# import and get logger
logger_directory = os.path.join(projectpath, 'logger')
sys.path.append(logger_directory)
import logger_config
logger = logging.getLogger(__name__)

# Global variables
SLEEP_DELAY = 5

@click.group()
def main():
    pass

@click.option('--fake', is_flag=True, help='fake datas')
@main.command()
def main(fake):
    if fake:
        
        get_sensors_fake()
    else:
        get_sensors()
    

def get_watt():
    return api_get_watt_values()

def get_temp():
    return api_get_temp_values()

def get_sensors():
    while True:
        try:
            watts = get_watt()
            temps = get_temp()
            logger.info('createSensorRecord: watts '+str(watts)+' temps '+ str(temps))
            dt = datetime.datetime.now()
            createSensorRecord(dt, temps[0], temps[1], temps[2], watts[0], watts[1], watts[2], watts[3])
            time.sleep(SLEEP_DELAY)
        except IndexError:
            logger.error('IndexError ', exc_info=True)

def get_sensors_fake():
    while True:
        try:
            random_int = randint(-10, 10)
            dt = datetime.datetime.now()
            datas = [dt, 60+random_int, 70+random_int, None, 2000, 2000, 0, 0]
            logger.info('createSensorRecord: datas '+str(datas))
            createSensorRecord(*datas)
            time.sleep(SLEEP_DELAY)
        except IndexError:
            logger.error('IndexError ', exc_info=True)

if __name__ == '__main__':
    main()