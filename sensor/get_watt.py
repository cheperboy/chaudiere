"""
This script reads power through the wire of a 220v AC sine signal

This script can be called in console for debug purpose
If called by an external software (eg Chaudiere app), the entry point is api_get_watt_values()

Hardware interface
SCT-013-030-30A-1V-ac-current-sensor is connected to ADS1115
ADS1115 isconnected to Raspberry via i2C
ADS1115 has four analog inputs
analog input is biased to 3,3v/2 = 1.6v
With no power in AC this should give in theory 1600 mv read from ADC
In Practice, around 1635 to 1640 is read. So we consider that below 1650 (MIN_VALUE), the AC power is 0
"""

import ADS1115
import os, sys, argparse, string, datetime, time
import logging, logging.config
import glob


# Script Constants
WATT_SENSOR_SIZE = 4
DEFAULT_SENSOR_VALUE = None #if no sensor value is read then recorded value is DEFAULT_SENSOR_VALUE
MIN_VALUE = 1640               #if sensor value < MIN_VALUE then recorded value is 0

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
Return a list of four integer values read from ADC
"""
def api_get_watt_values():
    values = get_watt_values()
    if not values:
        logger.warning("get watt failed, returning default sensor value")
        values = []
        for n in range(0, WATT_SENSOR_SIZE):
            values.append(DEFAULT_SENSOR_VALUE)
    return (values)

# Replace value lower than MIN_VALUE to zero (int)
def get_watt_values():
    checkedValues = read_adc()    
    #convert values to int and to 0 if sensor value < MIN_VALUE
    if checkedValues:
        values = [0 if int(x)<MIN_VALUE else int(x) for x in checkedValues]
        #logger.debug(values)
        return values
    else:
        return False

# Read values (mV) from the four inputs of ADS1115
# Return a list of four values [ A0, A1, A2, A3]
# condidering that 220v AC signal is sine, multiples samples are read and the max is returned (approx equal to the max value of the sine signal)
def read_adc():
    try:
        # Initialize ADC converter
        ads = ADS1115.ADS1115()
    
    except IOError as e:
        logger.error(f'ADS1115 not available: {e}')
        return False
    
    except Exception as e:
        logger.error(f'Exception {e}', exc_info=True)
        # raise # print traceback / raise to higher level
        return False
    
    else:
        num_samples = 30
        channels    = [0, 1, 2, 3]
        max_voltage = [0, 0, 0, 0]
        for ch in channels:
            for x in range(0, num_samples):
                voltage = ads.readADCSingleEnded(channel=ch)
                max_voltage[ch] = max(voltage, max_voltage[ch])
        return max_voltage

def debug_read_channels():
    ads = ADS1115.ADS1115()
    num_samples = 30
    channels    = [0, 1, 2, 3]
    for ch in channels:
        max_voltage = 0
        for x in range(0, num_samples):
            voltage = ads.readADCSingleEnded(channel=ch)
            max_voltage = max(voltage, max_voltage)
        value = '{:4.0f}'.format(max_voltage)
        logger.info('channel '+ str(ch) + '\t'+str(value))

# For debug purpose, calling main() read values from ADC and print to console every 1 second
def main():
    while True:
        # values = read_adc()
        # values = ['{:4.0f}'.format(value) for value in values]
        # logger.info(values)
        
        values = get_watt_values()
        values = ['{:4.0f}'.format(value) for value in values]
        logger.info(values)
        
        #debug_read_channels()
        
        time.sleep(0.5) 
        
if __name__ == '__main__':
    main()