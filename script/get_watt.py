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

PORT = '/dev/ttyACM0'
BAUDRATE = 9600
STOPBITS = serial.STOPBITS_ONE
BYTESIZE = serial.SEVENBITS

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/script
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                   # /home/pi/Dev
envname = os.path.basename(envpath)                      # Dev

logfile_base = os.path.join(currentpath, 'log')
tmpfile_base = os.path.join(currentpath, 'tmp')
#logfile_base = currentpath

# import Database API
chaudiereapp = os.path.join(projectpath, 'chaudiereapp')
print chaudiereapp
sys.path.append(chaudiereapp)
from newapi import createWattbuffer

def main():
    try:
        port = serial.Serial(port = PORT,baudrate = BAUDRATE, stopbits = STOPBITS, bytesize = BYTESIZE)
        time.sleep(.1)
        port.flushInput()
        time.sleep(.1)
    except SerialException:
        logger.info('Cant Open Port')
        sys.exit(0)
    logger.info('Port open')
    
    # Delete X firsts records (not relevant)
    for i in range(6):
        checkedValues = parseLine(port)
    while True:
        try:
            checkedValues = parseLine(port)
            # Format output and write to special logger
            logger_output_content = ""
            for value in checkedValues:
                logger_output_content += ";" + str(value)
            logger_output.info(logger_output_content)
            """createWattbuffer(
                    datetime.datetime.utcnow(),
                    checkedValues[0],
                    checkedValues[1],
                    checkedValues[2])
            """
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

def checkCRC(values):
    sum = 0
    try:
        crc = int(values.pop())
        for value in values :
            sum += int(value)
        if (int(sum) == crc):
            return True
    except Exception as e:
        logger.error("Invalid datas from serial port ({0})".format(e))
        return False
    return False
    
def parseLine(port):
    try:
        data = port.readline()
    except SerialException:
        logger.error(data)
        logger.error('SerialException, closing port and EXIT', exc_info=True)
        port.close()
        sys.exit(0)
    try:
        values = data.split(';')
        values.pop() #remove EOL \n\r
    except Exception as e:
        logger.error("Invalid datas from serial port ({0})".format(e))
        return False
    else:
        logger.info(values)
        crc = checkCRC(values)
        if crc == False:
            logger.error("CRC ERROR")
            logger.error(values)
            return (False)
        return (values)
    
if __name__ == '__main__':
    
    # PARSE ARGS
    parser = argparse.ArgumentParser(description = "Rpi gets info from Uno serial", epilog = "" )
    parser.add_argument("-v",
                          "--verbose",
                          help="increase output verbosity",
                          action="store_true")
    args = parser.parse_args()

    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.CRITICAL
    
    # SET LOGGER
    logger = logging.getLogger(__name__)
    logger_output = logging.getLogger("output")
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s | %(name)s | %(filename)s | %(levelname)s | %(funcName)s | %(message)s"
            },
            "output": {
                "format": "%(asctime)s%(message)s",
                "datefmt": "%Y/%m/%d %H:%M:%S",
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": loglevel,
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },

            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": os.path.join(logfile_base, __file__+'_info.log'),
                "maxBytes": 5000,
                "backupCount": 1,
                "encoding": "utf8"
            },

            "error_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": os.path.join(logfile_base, __file__+'_error.log'),
                "maxBytes": 5000,
                "backupCount": 1,
                "encoding": "utf8"
            },
            
            "output_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "output",
                "filename": os.path.join(tmpfile_base, 'watt.tmp'),
                "maxBytes": 200,
                "backupCount": 1,
                "encoding": "utf8"
            }
        },

        "loggers": {
            __name__: {
                "level": "INFO",
                "handlers": ["console", "info_file_handler", "error_file_handler"]
            },
            "output": {
                "level": "INFO",
                "handlers": ["output_file_handler"]
            }
        },
    })

    
    # CALL MAIN
    main()