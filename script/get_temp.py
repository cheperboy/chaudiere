#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, argparse, string, datetime, time
import logging
import glob
import logger_config

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/script
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                   # /home/pi/Dev
envname = os.path.basename(envpath)                      # Dev

logfile_base = os.path.join(currentpath, 'log')
#logfile_base = currentpath

# Sensor Config
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'

# Constant
DEFAULT_SENSOR_VALUE = -1

# SET LOGGER
logger = logging.getLogger(__name__)

"""
Read sensor buffer in /sys/bus/w1/devices/28xxxx[N]/w1_slave
    28xxxx : sensor base name
    [N] iter on all sensors that match base name
    w1_slave : sensor buffer (temp & CRC)
"""
def get_raw_sensor_buffer(sensor):
    device_folder = glob.glob(base_dir + '28*')[sensor]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    w1_slave = f.readlines()
    f.close()
    return w1_slave

"""
Parse temperature value from sensor buffer and returns
"""
def get_temp_value(sensor):
    lines = get_raw_sensor_buffer(sensor)
    # if CRC Fail, read again (if fail too much, stop)
    fail_count = 0
    max_fail = 10
    while lines[0].strip()[-3:] != 'YES':
        fail_count += 1
        if fail_count > max_fail:
            logger.warning("CRC Fail many times for sensor "+str(sensor))
            return False
        else:
            time.sleep(0.2)
            lines = get_raw_sensor_buffer(sensor)
    equals_pos = lines[1].find('t=')
    # if CRC is ok and temp value exist
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

"""
External API : returns list of sensor values
if get a wrong value, set it to default value -1
"""
def api_get_temp_values():
    temp0 = get_temp_value(0)
    temp1 = get_temp_value(1)
    if not temp0:
        logger.critical("temp0 Fail, returning wrong value")
        temp0 = DEFAULT_SENSOR_VALUE
    if not temp1:
        logger.critical("temp1 Fail, returning wrong value")
        temp1 = DEFAULT_SENSOR_VALUE
    return( [temp0, temp1] )

def main():
    while True:
        temp0 = get_temp_value(0)
        temp1 = get_temp_value(1)
        if not temp0:
            logger.critical("temp0 Fail")
        if not temp1:
            logger.critical("temp1 Fail")
        logger.info(str("%.1f" % temp0)+" "+str("%.1f" % temp1))
        time.sleep(1)

if __name__ == '__main__':             
    # CALL MAIN
    main()