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

# Script Constants
TIMEOUT = 10
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

def read_serial_port(port):
    try:
        fail_count = 0
        data = False
        while( (not data) and (fail_count < MAX_FAIL_SERIAL)):
            if port.isOpen():
                data = port.readline()
            else:
                logger.debug('port not opened')
            fail_count += 1
            if (not data):
                restart_serial_port()
        if (not data): # if empty list, no data from serial port, return false
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
        values = []
        for n in range(0,  ):
            values.append(DEFAULT_SENSOR_VALUE)
    return (values)

def main():
    while True:
        values = get_watt_values()
        logger.info(values)

        
def open_port():
    try:
        port = serial.Serial(port = PORT,baudrate = BAUDRATE, stopbits = STOPBITS, bytesize = BYTESIZE, timeout = 2)
        return port
        
    except SerialException:
        logger.error('Cant Open Port')
        port.close()
        return False
    
def get_watt_values():
    try:
        port = open_port()
        time.sleep(.1)
        port.flushInput()
        time.sleep(.1)
        checkedValues = read_serial_port(port)
        port.close()
        return checkedValues
        
    except SerialException:
        logger.error('Cant Open Port')
        port.close()
        return False
    except KeyboardInterrupt:
        logger.debug('KeyboardInterrupt')
        try:
            port.close()
            logger.debug('serial.close()')
            sys.exit(0)
        except SystemExit:
            port.close()
            logger.debug('SystemExit')
            os._exit(0)
#        time.sleep()
    
if __name__ == '__main__':
    # CALL MAIN
    main()