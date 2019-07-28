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
DEFAULT_SENSOR_VALUE = None #if no sensor value is read then recorded value is DEFAULT_SENSOR_VALUE
MIN_VALUE = 4               #if sensor value < MIN_VALUE then recorded value is 0
MAX_FAIL_SERIAL = 5

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/script
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                   # /home/pi/Dev
envname = os.path.basename(envpath)                      # Dev

# import and get logger
logger_directory = os.path.join(projectpath, 'logger')
sys.path.append(logger_directory)
import logger_config
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
def power_off_serial_port():
    logger.debug('power_off_serial_port')
    try:
        command = 'sudo /home/pi/Dev/chaudiere/script/usb/uhubctl/uhubctl -p 2 -a 0'
        logger.debug('executing '+ command)
        os.system(command)
        time.sleep(2)

        command = 'sudo /home/pi/Dev/chaudiere/script/usb/uhubctl/uhubctl -p 2 -a 1'
        logger.debug('executing '+ command)
        os.system(command)
        time.sleep(6)
    except SerialException:
        logger.error('SerialException while executing cat /dev/ttyA*, ', exc_info=True)

"""
Execute cat command on serial ports with a timeout of 8 seconds
"""
def restart_serial_port():
    logger.info('restarting serial port')
    try:
        command = ' timeout 8 cat '+ prog_port()
        os.system(command)
        command = ' timeout 8 cat '+ native_port()
        os.system(command)
    except SerialException:
        logger.error('SerialException while executing command', exc_info=True)

"""
print to watt_buffer the values read from serial port
delete the N first value that are not relevant (first reading from arduino ADC)
"""
def api_get_watt_values():
    values = get_watt_values()
    if not values:
        logger.warning("get watt failed, returning default sensor value")
        values = []
        for n in range(0, WATT_SENSOR_SIZE):
            values.append(DEFAULT_SENSOR_VALUE)
    return (values)
 
def main():
    while True:
        values = get_watt_values()
        logger.info(values)

def close_port(port, caller):
    try:
        #logger.debug('Closing port '+ port.name)
        port.close()       
    except Exception as e:
        logger.error('Cant close Port : caller '+str(caller)+'({0})'.format(e))
    
def get_watt_values():
    try:
        checkedValues = read_serial_port()
        #convert values to int and to 0 if sensor value < MIN_VALUE
        if checkedValues:
            values = [0 if int(x)<MIN_VALUE else int(x) for x in checkedValues]
            #logger.debug(values)
            return values
        else:
            return False
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
        time.sleep(.1)
        fail_count = 0
        data = False
        while( (not data) and (fail_count < MAX_FAIL_SERIAL) ):
            fail_count += 1
            
            #open port
            try:
                port = serial.Serial(port = PORT,baudrate = BAUDRATE, stopbits = STOPBITS, bytesize = BYTESIZE, timeout = TIMEOUT)
            except serial.SerialException as e:
                logger.error('Exception : Could not open serial port {}: {}\n'.format(port.name, e))
                close_port(port, 1)
                return False
            
            #read data and close port
            data = port.readline()
            close_port(port, 2)
        #end of while

        #If no data is set restart serial port (for next call) and return false
        if (not data):
            logger.warning('No data from serial port')
            restart_serial_port()
            return False
        #else if some data to compute, check CRC
        else:
            values = data.split(';')
            values.pop() #remove EOL \n\r
            crc = checkCRC(values)
            if crc == True:
                logger.debug(str(PORT) +" "+ str(values) +" CRC "+ str(crc))
                return values
            else:
                logger.warning(str(PORT) +" "+ str(values) +" CRC "+ str(crc))
                return False
    
    except serial.SerialException as e:
        logger.error('Exception when reading port', exc_info=True)
        close_port(port, 4)
        return False
    except Exception as e:
        logger.error("General Exception 2 ({0})".format(e))
        return False

if __name__ == '__main__':
    # CALL MAIN
    main()