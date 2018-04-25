"""
Reads current value from serial port (from Arduino Due)
Outputs current values (watt) to a temp file (/tmp/watt.tmp) 
the output buffer is formatted as:
2018/04/15 21:06:05;10;8;10
date (%Y/%m/%d %H:%M:%S) value1;value2;valueN

"""
import os, sys, argparse, string, datetime, time
import logging, logging.config
import serial
from serial.serialutil import SerialException
import logger_config

# Serial Config
PORT = '/dev/ttyACM0'
BAUDRATE = 9600
STOPBITS = serial.STOPBITS_ONE
BYTESIZE = serial.SEVENBITS

# Script Constants
TIMEOUT = 2*1000
WATT_SENSOR_SIZE = 3
DEFAULT_SENSOR_VALUE = -1

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/script
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                   # /home/pi/Dev
envname = os.path.basename(envpath)                      # Dev

# SET LOGGER
logger = logging.getLogger(__name__)

"""
Config for special watt buffer
"""

def checkCRC(values):
    sum = 0
    try:
        crc = int(values.pop())
        for value in values :
            sum += int(value)
        if (int(sum) == crc):
            return True
    except Exception as e:
        logger.warning("Invalid datas from serial port ({0})".format(e))
        return False
    return False
    
def read_serial_port(port):
    try:
        start = time.time()
        now = time.time()
        data = False
        data = port.readline()
        if not data : # if empty list, no data from serial port, return false
            logger.warning('no data from serial port')
            return False
        values = data.split(';')
        values.pop() #remove EOL \n\r
    except SerialException:
        logger.error('SerialException, closing port and EXIT', exc_info=True)
        port.close()
        sys.exit(0)
    except Exception as e:
        logger.warning("Invalid datas from serial port ({0})".format(e))
        return False
    else:
        #logger.debug(values)
        crc = checkCRC(values)
        logger.debug("port "+ str(PORT) +" "+ "values "+ str(values) +" CRC "+ str(crc))
        if crc == False:
            logger.warning("CRC Error")
            return (False)
        return (values)

"""
print to watt_buffer the values read from serial port
delete the N first value that are not relevant (first reading from arduino ADC)
"""
def api_get_watt_values():
    values = get_watt_values()
    if not values:
        logger.critical("get watt Fail, returning wrong value")
        watt0 = DEFAULT_SENSOR_VALUE
        watt1 = DEFAULT_SENSOR_VALUE
        watt2 = DEFAULT_SENSOR_VALUE
        values = []
        for n in range(0, WATT_SENSOR_SIZE):
            values.append(DEFAULT_SENSOR_VALUE)
    return (values)

def main():
    while True:
        values = get_watt_values()
        logger.info(values)

def get_watt_values():
    try:
        port = serial.Serial(port = PORT,baudrate = BAUDRATE, stopbits = STOPBITS, bytesize = BYTESIZE, timeout = 2)
        time.sleep(.1)
        port.flushInput()
        time.sleep(.1)
        checkedValues = read_serial_port(port)
        return checkedValues
        
    except SerialException:
        logger.error('Cant Open Port')
        return False
        sys.exit(0)
    except KeyboardInterrupt:
        logger.debug('KeyboardInterrupt')
        try:
            port.close()
            logger.debug('serial.close()')
            sys.exit(0)
        except SystemExit:
            logger.debug('SystemExit')
            os._exit(0)
#        time.sleep()
    
if __name__ == '__main__':
    # CALL MAIN
    main()