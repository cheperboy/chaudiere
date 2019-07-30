#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, argparse, string, datetime, time
import logging
import glob

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/script
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                   # /home/pi/Dev
envname = os.path.basename(envpath)                      # Dev

# import and get logger
logger_directory = os.path.join(projectpath, 'logger')
sys.path.append(logger_directory)
import logger_config
logger = logging.getLogger(__name__)

# Sensor Config
# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'

# SENSOR CONFIG
SENSOR_TEMP_0 = '28-00000a69bebf'
SENSOR_TEMP_1 = '28-800000282141'

# Constant
DEFAULT_SENSOR_VALUE = -1

# Retrive sensor by index or name
BY_NAME = 1
BY_INDEX = 2

def get_raw_sensor_buffer(sensor, retrive_method):
    """
    Read sensor buffer in /sys/bus/w1/devices/28xxxx[N]/w1_slave
        28xxxx : sensor base name
        [N] iter on all sensors that match base name
        w1_slave : sensor buffer (temp & CRC)
    28-8000002817f6
    28-80000028212d
    28-800000281fef

    """
    try:
        if retrive_method == BY_INDEX:
            device_folder = glob.glob(base_dir + '28*')[sensor]
        elif retrive_method == BY_NAME:
            device_folder = base_dir + sensor
        else:
            logger.error("retrive_method not defined")
            return ''
        #logger.debug(device_folder)
        device_file = device_folder + '/w1_slave'
        #logger.debug("reading sensor "+str(sensor) + " " + str(device_file))
        f = open(device_file, 'r')
        w1_slave = f.readlines()
        f.close()
    except Exception as e:
        logger.error("Invalid datas from OneWire ({0})".format(e))
        return ''
    return w1_slave

def get_temp_value(sensor, retrive_method):
    """
    Parse temperature value from sensor buffer and returns
    """
    try:
        sensor_buffer = get_raw_sensor_buffer(sensor, retrive_method)
        # if CRC Fail, read again (if fail too much, stop)
        fail_count = 0
        max_fail = 10
        if sensor_buffer == '':
            return False
        
        while sensor_buffer == '' or sensor_buffer[0].strip()[-3:] != 'YES':
            fail_count += 1
            if fail_count > max_fail:
                logger.warning("CRC Fail many times for sensor "+str(sensor))
                return False
            else:
                time.sleep(0.2)
                sensor_buffer = get_raw_sensor_buffer(sensor, retrive_method)
        equals_pos = sensor_buffer[1].find('t=')
        # if CRC is ok and temp value exist
        if equals_pos != -1:
            temp_string = sensor_buffer[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            #logger.debug("value "+str(temp_c))
            return temp_c
    except Exception as e:
        logger.error("Invalid datas from serial port ({0})".format(e))
        return -1

def api_get_temp_values():
    """
    External API : returns list of sensor values
    if get a wrong value, set it to default value -1
    """
    temp0 = get_temp_value(SENSOR_TEMP_0, BY_NAME)
    temp1 = get_temp_value(SENSOR_TEMP_1, BY_NAME)
    temp2 = DEFAULT_SENSOR_VALUE
    if not temp0:
        logger.critical("temp0 Fail, returning wrong value")
        temp0 = DEFAULT_SENSOR_VALUE
    if not temp1:
        logger.critical("temp1 Fail, returning wrong value")
        temp1 = DEFAULT_SENSOR_VALUE
    if not temp2:
        logger.critical("temp2 Fail, returning wrong value")
        temp2 = DEFAULT_SENSOR_VALUE
    logger.debug(str("%.3f" % temp0)+" "+str("%.3f" % temp1)+" "+str("%.3f" % temp2))
    return( [temp0, temp1, temp2] )

def main():
    while True:
        """
        temp0 = get_temp_value(0, BY_INDEX)
        temp1 = get_temp_value(1, BY_INDEX)
        temp2 = get_temp_value(2, BY_INDEX)
        """
        temp0 = get_temp_value(SENSOR_TEMP_0, BY_NAME)
        temp1 = get_temp_value(SENSOR_TEMP_1, BY_NAME)
        temp2 = DEFAULT_SENSOR_VALUE
        if not temp0:
            logger.critical("temp0 Fail")
        if not temp1:
            logger.critical("temp1 Fail")
        if not temp2:
            logger.critical("temp2 Fail")
        logger.info(str("%.1f" % temp0)+" "+str("%.1f" % temp1)+" "+str("%.1f" % temp2))
        time.sleep(1)

if __name__ == '__main__':             
    # CALL MAIN
    main()