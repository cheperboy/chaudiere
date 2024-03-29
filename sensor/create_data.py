import click
import os, sys, argparse, string, datetime, time
import logging, logging.config
import serial
from serial.serialutil import SerialException
from random import randint

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/sensor
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere

# import sensors API
from get_temp import api_get_temp_values
from get_watt import api_get_watt_values

# import Database API from flask_app
flask_app_directory = os.path.join(projectpath, 'flask_app')
sys.path.append(flask_app_directory)
from db_api import createSensorRecord
from db_influx_api import add_measures_influx

# import and get logger
logger_directory = os.path.join(projectpath, 'logger')
sys.path.append(logger_directory)
import logger_stdout
logger = logging.getLogger(__name__)

# Global variables
SLEEP_DELAY = 5


from influxdb import InfluxDBClient
# connexion a la base de données InfluxDB
influx_client = InfluxDBClient('localhost', 8086, username='influx', password='yVhlZYyZk3i/TXXmXMM')
DB_NAME = "chaudiere"
connected = False
while not connected:
    try:
        logging.info("Database %s exists?" % DB_NAME)
        if not {'name': DB_NAME} in influx_client.get_list_database():
            logging.info("Database %s creation.." % DB_NAME)
            influx_client.create_database(DB_NAME)
            logging.info("Database %s created!" % DB_NAME)
        influx_client.switch_database(DB_NAME)
        logging.info("Connected to %s!" % DB_NAME)
    except Exception as e:
        logging.info('InfluxDB is not reachable. Waiting 5 seconds to retry.')
        time.sleep(5)
    else:
        connected = True



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
            logger.info('watts '+str(watts)+' temps '+ str(temps))
            dt = datetime.datetime.now()
            createSensorRecord(dt, temps[0], temps[1], temps[2], None, watts[0], watts[1], watts[2], watts[3])
            add_measures_influx(influx_client, temps[0], temps[1], temps[2], None, watts[0], watts[1], watts[2], watts[3])
            time.sleep(SLEEP_DELAY)
        except IndexError:
            logger.error('IndexError ', exc_info=True)

def get_sensors_fake():
    while True:
        try:
            random_int = randint(-10, 10)
            small_random_int = randint(-3, 3)
            dt = datetime.datetime.now()
            datas = [dt, 60+random_int, 70+random_int, 20+small_random_int, None, 2000, 2000, 0, 0]
            logger.info('datas '+str(datas))
            createSensorRecord(*datas)
            time.sleep(SLEEP_DELAY)
        except IndexError:
            logger.error('IndexError ', exc_info=True)

if __name__ == '__main__':
    logger.info('starting processus')
    main()