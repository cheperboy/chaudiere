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

PORT = '/dev/ttyACM0'
BAUDRATE = 9600
STOPBITS = serial.STOPBITS_ONE
BYTESIZE = serial.SEVENBITS

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/script
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                   # /home/pi/Dev
envname = os.path.basename(envpath)                      # Dev

logfile_base = os.path.join(currentpath, 'log')
watt_buffer_dir = os.path.join(currentpath, 'tmp')
watt_buffer_file = os.path.join(watt_buffer_dir, 'watt.tmp')

# SET LOGGER
logger = logging.getLogger(__name__)

"""
Config for special watt buffer
"""
def config_watt_buffer_logger():
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "output": {
                "format": "%(asctime)s%(message)s",
                "datefmt": "%Y/%m/%d %H:%M:%S",
            }
        },
        "handlers": {
            "watt_buffer": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "output",
                "filename": watt_buffer_file,
                "maxBytes": 200,
                "backupCount": 1,
                "encoding": "utf8"
            }
        },
        "loggers": {
            "watt_buffer": {
                "level": "INFO",
                "handlers": ["watt_buffer"],
                "propagate": "no"                
            }
        },
    })

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
        data = port.readline()
    except SerialException:
        logger.error('SerialException, closing port and EXIT', exc_info=True)
        port.close()
        sys.exit(0)
    try:
        values = data.split(';')
        values.pop() #remove EOL \n\r
    except Exception as e:
        logger.warning("Invalid datas from serial port ({0})".format(e))
        return False
    else:
        logger.debug(values)
        crc = checkCRC(values)
        if crc == False:
            logger.warning("CRC Error")
            return (False)
        return (values)

"""
print to watt_buffer the values read from serial port
delete the N first value that are not relevant (first reading from arduino ADC)

"""
def main():
    watt_buffer = logging.getLogger("watt_buffer")
    config_watt_buffer_logger()
    try:
        port = serial.Serial(port = PORT,baudrate = BAUDRATE, stopbits = STOPBITS, bytesize = BYTESIZE)
        time.sleep(.1)
        port.flushInput()
        time.sleep(.1)
    except SerialException:
        logger.error('Cant Open Port')
        sys.exit(0)
    
    # Delete N firsts records (not relevant)
    for i in range(8):
        checkedValues = read_serial_port(port)
    while True:
        try:
            checkedValues = read_serial_port(port)
            
            # Format output and write to special watt_buffer logger
            logger_output_content = ""
            for value in checkedValues:
                logger_output_content += ";" + str(value)
            watt_buffer.info(logger_output_content)

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