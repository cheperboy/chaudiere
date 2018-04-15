import os, sys, argparse, string, datetime, time
import logging, logging.config
import serial

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/script
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                   # /home/pi/Dev
envname = os.path.basename(envpath)                      # Dev

logfile_base = os.path.join(currentpath, 'log')
tmpfile_base = os.path.join(currentpath, 'tmp')
tmpfile = os.path.join(tmpfile_base, 'watt.tmp')


if __name__ == '__main__':

    while True:
        with open(tmpfile, 'rb') as buffer:
            for line in buffer:
                pass
            last = line
            print line
            time.sleep(.4)



        
        