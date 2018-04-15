import os, sys, argparse, string, datetime, time
import logging, logging.config
import serial
from serial.serialutil import SerialException
from get_temp import api_get_temp_values


currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/script
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                   # /home/pi/Dev
envname = os.path.basename(envpath)                      # Dev

logfile_base = os.path.join(currentpath, 'log')
tmpfile_base = os.path.join(currentpath, 'tmp')
tmpfile = os.path.join(tmpfile_base, 'watt.tmp')

# import Database API
chaudiereapp = os.path.join(projectpath, 'chaudiereapp')
sys.path.append(chaudiereapp)
from newapi import createChaudiere

"""
Get last line of wattbuffer
verify data is fresh
return values
"""
def get_last_watt():
    # Get last line of wattbuffer
    with open(tmpfile, 'rb') as buffer:
        for line in buffer:
            pass
        last = line
    # Remove \n with rstrip and Parse date
    values = line.rstrip().split(';')
    date_str = values.pop(0) #get first element = the date
    date_obj = datetime.datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S')
    delta = (datetime.datetime.now() - date_obj).seconds
    if delta < 3:
        values = map(int, values) #cast to Int all values
        return values
    else:
        logger.warning("no fresh value from Arduino")
        return [0,0,0]
            
def get_temp():
    return api_get_temp_values()

def main():
    while True:
        watts = get_last_watt()
        temps = get_temp()
        createChaudiere(datetime.datetime.now(), temps[0], temps[1], watts[0], watts[1], watts[2])
        time.sleep(.5)

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
                "format": "%(asctime)s | %(name)s | %(filename)s | %(levelname)s | %(funcName)s | %(message)s"
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
                "filename": os.path.join(logfile_base, 'get_temp_error.log'),
                "maxBytes": 5000,
                "backupCount": 1,
                "encoding": "utf8"
            }
        },

        "loggers": {
            __name__: {
                "level": "ERROR",
                "handlers": ["console"]
            }
        }
    })

    # CALL MAIN
    main()