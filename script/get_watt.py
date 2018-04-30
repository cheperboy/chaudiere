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
import glob
from find_port import native_port, prog_port

#PORT = '/dev/ttyAMA0'  # Native USB
#PORT = '/dev/ttyACM2'   # Programming port

# Serial Config
BAUDRATE = 9600
STOPBITS = serial.STOPBITS_ONE
BYTESIZE = serial.SEVENBITS
PORT = native_port()
TIMEOUT = 10

# Script Constants
WATT_SENSOR_SIZE = 4
DEFAULT_SENSOR_VALUE = -1
MAX_FAIL_SERIAL = 4

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

"""
resssources:
https://raspberrypi.stackexchange.com/questions/5407/how-can-i-cut-power-coming-out-of-the-pis-usb-ports?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
https://github.com/mvp/uhubctl

procedure:
power off usb : sudo uhubctl -p 2 -a 0
delay
power on usb : sudo uhubctl -p 2 -a 1
delay
cat Prog port
"""
def restart_serial_port():
    logger.debug('restart_serial_port')
    try:
        command = 'sudo /home/pi/Dev/chaudiere/script/usb/uhubctl/uhubctl -p 2 -a 0'
        logger.debug('executing '+ command)
        os.system(command)
        time.sleep(2)

        command = 'sudo /home/pi/Dev/chaudiere/script/usb/uhubctl/uhubctl -p 2 -a 1'
        logger.debug('executing '+ command)
        os.system(command)
        time.sleep(6)
        """
        command = 'stty -F '+ prog_port() +' min 1 time 3'        
        logger.debug('executing '+ command)
        os.system(command)
        command = 'cat '+ prog_port() +'> temp.txt'
        logger.debug('executing '+ command)
        os.system(command)
        time.sleep(0.5)
        """
    except SerialException:
        logger.error('SerialException while executing cat /dev/ttyA*, ', exc_info=True)

"""
print to watt_buffer the values read from serial port
delete the N first value that are not relevant (first reading from arduino ADC)
"""
def api_get_watt_values():
    values = get_watt_values()
    if not values:
        logger.critical("get watt Fail, returning wrong value")
        values = []
        for n in range(0, WATT_SENSOR_SIZE):
            values.append(DEFAULT_SENSOR_VALUE)
    return (values)

def main():
    while True:
        values = get_watt_values()
        logger.info(values)

        
def open_port():
    try:
        port = serial.Serial(port = PORT,baudrate = BAUDRATE, stopbits = STOPBITS, bytesize = BYTESIZE, timeout = TIMEOUT)
        return port
        
    except SerialException:
        logger.error('Cant Open Port')
        port.close()
        return False
    
def close_port(port, caller):
    try:
        logger.info('Closing port '+ port.name)
        port.close()       
    except Exception as e:
        logger.error('Cant close Port : caller '+str(caller)+'({0})'.format(e))
    
def get_watt_values():
    try:
        checkedValues = read_serial_port()
        return checkedValues
        
    except Exception as e:
        logger.warning("General Exception 1 ({0})".format(e))
        return False
    except KeyboardInterrupt:
        logger.debug('Keyboard Interrupt')
        try:
            sys.exit(0)
        except SystemExit:
            logger.debug('SystemExit')
            os._exit(0)

def read_serial_port():
    try:
        port = serial.Serial(port = PORT,baudrate = BAUDRATE, stopbits = STOPBITS, bytesize = BYTESIZE, timeout = TIMEOUT)
    except serial.SerialException as e:
        logger.error('Exception : Could not open serial port {}: {}\n'.format(port.name, e))
        close_port(port, 1)
        return False
    try:
        time.sleep(.1)
        data = False
        data = port.readline()
        logger.debug('raw data : '+str(data))
        close_port(port, 2)
        if (not data): # if empty list, no data from serial port, return false
            logger.warning('No data from serial port')
            close_port(port, 3)
            return False
        values = data.split(';')
        values.pop() #remove EOL \n\r
    
    except serial.SerialException as e:
        logger.error('Exception when reading port', exc_info=True)
        close_port(port, 4)
        return False
    except Exception as e:
        logger.warning("General Exception 2 ({0})".format(e))
        return False
    else:
        #logger.debug(values)
        crc = checkCRC(values)
        logger.debug("port "+ str(PORT) +" "+ "values "+ str(values) +" CRC "+ str(crc))
        if crc == False:
            logger.warning("CRC Error")
            return (False)
        return (values)

if __name__ == '__main__':
    # CALL MAIN
    main()