import os, sys, argparse, string, datetime
import logging, logging.config
import serial
from serial.serialutil import SerialException

PORT = '/dev/ttyACM0'
BAUDRATE = 9600
STOPBITS = serial.STOPBITS_ONE
BYTESIZE = serial.SEVENBITS

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere
#projectpath = os.path.dirname(currentpath)               # /home/pi/Dev
envpath = os.path.dirname(currentpath)                   # /home/pi/Dev
envname = os.path.basename(envpath)                      # Dev

#logfile_base = os.path.join(currentpath, 'log')
logfile_base = currentpath
'''
api = projectpath + '/teleinfoapp/'
sys.path.append(api)
from api import createti
'''
'''
logging.critical(os.path.basename(__file__))
logging.error("ERROR")
logging.warning("WARNING")
logging.info("INFO")
logging.debug("DEBUG")
'''

def main():
    logger.info('Start')
    try:
        logger.info('before port open')
        port = serial.Serial(port = PORT,baudrate = BAUDRATE, stopbits = STOPBITS, bytesize = BYTESIZE)
        logger.info('after port open')
    except SerialException:
        logger.info('Cant Open Port')
        sys.exit(0)
    logger.debug('before try read port')
    try:
        while True:
            teleinfo = readPort(port)
            print(teleinfo)
            """
            createti(
                      datetime.datetime.now(), 
                      teleinfo['base'],
                      teleinfo['papp'],
                      teleinfo['iinst1'],
                      teleinfo['iinst2'],
                      teleinfo['iinst3']
                    )
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

def checkCRC(values):
    sum = 0
    crc = values.pop()
    for value in values :
        sum += int(value)
    if (int(sum) == int(crc)) :
        return True
    return False
    
def readPort(port):
    logger.debug('readSerial()')
    teleinfo = dict([('papp', -1), ('base', -1), ('iinst1', -1), ('iinst2', -1), ('iinst3', -1), ('valid', -1)])
    reading = True #End of frame found / all datas are set
    count_valid = 0
    while (reading == True):
        try:
            data = port.readline()
        except SerialException:
            logger.error('SerialException, closing port and EXIT', exc_info=True)
            port.close()
            sys.exit(0)
        values = data.split(';')
        values.pop() #remove EOL \n\r
        """        
        if (string.find(data, 'PAPP ') != -1):
            if (data[5:10].isdigit() == True):
                teleinfo['papp'] = int(data[5:10])
                count_valid += 1
        """
    logger.info(values)
    crc = checkCRC(values)
    if crc == False:
        logger.error("CRC ERROR")
        logger.info(values)
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
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s | %(name)s | %(filename)s | %(funcName)s | %(levelname)s | %(message)s"
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
                "filename": os.path.join(logfile_base, 'info.log'),
                "maxBytes": 1000,
                "backupCount": 1,
                "encoding": "utf8"
            },

            "error_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": os.path.join(logfile_base, 'error.log'),
                "maxBytes": 1000,
                "backupCount": 1,
                "encoding": "utf8"
            }
        },

        "loggers": {
            "my_module": {
                "level": "ERROR",
                "handlers": ["console"],
                "propagate": "no"
            }
        },

        "root": {
            "level": "INFO",
            "handlers": ["console", "info_file_handler", "error_file_handler"]
        }
    })

    # CALL MAIN
    main()