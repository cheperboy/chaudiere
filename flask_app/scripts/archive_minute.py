#!python
# -*- coding: utf-8 -*-

"""
markdown readme
# script archive_minute.py

## Summary
`Chaudiere` database records the sensors every 3 seconds
This script is used to store average values (one per Minute) of `Chaudiere` database into  `ChaudiereMinute` database .
This script is supposed to be run every 1 or 2 minutes by cron

## CLI Usage

### Normal mode

    python archive_minute.py
    
search for last ChaudiereMinute entry.
start from this entry to create a ChaudiereMinute entry per minute, logging average values of Chaudiere

### rework_from_now mode

    python archive_minute.py --rework_from_now --hours N
    
rework N hours from current datetime

### rework_from_date

    python archive_minute.py --rework_from_date  --hours N --date YYYY/MM/DD/HH

### CRON Config

Run every odd minutes

    */2 * * * * /home/pi/Envs/dev/bin/python /home/pi/Dev/chaudiere/chaudiereapp/scripts/archive_minute.py

## ToDo

Rework modes shall delete existing entries before creating new ones
"""

import os, sys, argparse
from datetime import datetime, timedelta
import logging, logging.config

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/chaudiereapp/script
chaudiereapp = os.path.dirname(currentpath)              # /home/pi/Dev/chaudiere/chaudiereapp
projectpath = os.path.dirname(chaudiereapp)              # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                   # /home/pi/Dev
envname = os.path.basename(envpath)                      # Dev

app_path = os.path.join(chaudiereapp, 'app')
sys.path.append(chaudiereapp)
from app import db
from app.models import Chaudiere, ChaudiereMinute
from app import create_app
app = create_app().app_context().push()

# import and get logger
logger_directory = os.path.join(projectpath, 'logger')
sys.path.append(logger_directory)
import logger_stdout
logger = logging.getLogger(__name__)

def find_datetime_end(date):
    """
    return the datetime of an existing Chaudiere entry close to the given *date* parameter
    """
    last_chaudiere_date = Chaudiere.last(Chaudiere).dt
    entry = Chaudiere.get_by_approx_date(Chaudiere, date)
    while ((entry is None) and (date < last_chaudiere_date)):
        date = date + timedelta(minutes=1)
        entry = Chaudiere.get_by_approx_date(Chaudiere, date)
    logger.debug('Chaudiere.dt end:'+ str(entry.dt))
    return entry.dt


def process_archive_minute(mode='normal', hours=None, date=None): 
    """ Defini date de debut et de fin 
    begin = (date du dernier record de la base Archive) + 1 minute
    end = (maintenant) - 1 minute
    Appelle la fonction record_minute() autant de fois que nécessaire
    """
    if mode is 'normal':
        # if ChaudiereMinute is empty then we start with the first Chaudiere record (oldest)
        if ChaudiereMinute.last(ChaudiereMinute) == None:
            logger.debug('ChaudiereMinute.last(ChaudiereMinute) == None:')
            begin = Chaudiere.first(Chaudiere).dt

        # else ChaudiereMinute is NOT empty then we start with the last ChaudiereMinute record (newest)
        else:
            logger.debug('ChaudiereMinute.last(ChaudiereMinute) != None:')
            begin = (ChaudiereMinute.last(ChaudiereMinute).dt + timedelta(minutes=1))

        # we finish with the last Chaudiere record (replace second to zero to avoid incomplete current minute)
        end = Chaudiere.last(Chaudiere).dt
    elif mode is 'rework_from_now':
        #begin is last existing Chaudiere - N hours
        dt = Chaudiere.last(Chaudiere).dt 
        begin = dt - timedelta(hours=hours)
        # we finish with the last Chaudiere record (replace second to zero to avoid incomplete current minute)
        end = Chaudiere.last(Chaudiere).dt
    elif mode is 'rework_from_date':
        end = find_datetime_end(date)
        begin = end - timedelta(hours=hours)
    else:
        logger.error('wrong arguments')
        return
    if begin is None:
        logger.info('No records')
        return
    
    begin = begin.replace(second=0, microsecond=0)
    end = end.replace(second=0, microsecond=0)
    
    if ((begin + timedelta(minutes=1)) > end):
        logger.info('Starting From '+ str(begin) + ' ...Waiting more records')
    else:
        logger.info('Archiving From '+ str(begin) +' To ' + str(end))

    # while some old Logs to Archive, call function record_minute()
    while ((begin + timedelta(minutes=1)) <= end):
        record_minute(begin)
        begin = begin + timedelta(minutes=1)

#ASC : plus ancient 
#DESC : plus recent
def record_minute(begin):
    """
    Recupere dans la base Logs l'ensemble des objets dont la date est comprise entre 
    les dates begin et (begin + 1 minute)
    Calcule des moyennes et enregistre dans une entry ChaudiereMinute
    """
    logger.debug('Minute '+ str(begin))    
    end = begin + timedelta(minutes=1)
    temp0 = 0.0
    temp1 = 0.0
    temp2 = 0.0
    watt1 = 0
    watt2 = 0
    watt3 = 0
    # get logs
    logs = Chaudiere.get_between_date(Chaudiere, begin, end)
    nb_logs = len(logs)
    logger.info('minute ' + str(begin)+' logs :'+str(nb_logs))
    if nb_logs > 0:
        for log in logs:
            if (log.temp0 is not None): temp0 += float(log.temp0)
            if (log.temp1 is not None): temp1 += float(log.temp1)
            if (log.temp2 is not None): temp2 += float(log.temp2)
            if (log.watt1 is not None): watt1 += int(log.watt1)
            if (log.watt2 is not None): watt2 += int(log.watt2)
            if (log.watt3 is not None): watt3 += int(log.watt3)
        # calcule des moyennes sur les series
        temp0 = temp0 / nb_logs
        temp1 = temp1 / nb_logs
        temp2 = temp2 / nb_logs
        watt1 = watt1 / nb_logs
        watt2 = watt2 / nb_logs
        watt3 = watt3 / nb_logs
        # Save to db
        ChaudiereMinute.create(ChaudiereMinute, begin, temp0, temp1, temp2, None, None, watt1, watt2, watt3, None, None, None)
    # else if no log to process, we still create an entry with None fields
    else:
        ChaudiereMinute.create(ChaudiereMinute, begin, None, None, None, None, None, None, None, None, None, None, None)

if __name__ == '__main__':
    
    # PARSE ARGS
    parser = argparse.ArgumentParser(description = "Archive Chaudiere in Minute and Hour db", epilog = "" )
    parser.add_argument('--rework_from_now',        action='store_true',  default=False, dest='rework_from_now',  help='rework N hours from now')
    parser.add_argument('--rework_from_date',       action='store_true',  default=False, dest='rework_from_date',  help='rework N hours from given END date')
    parser.add_argument('--hours',                  type=int,             default=None,   help='number of hour to rework')
    parser.add_argument('--date',                                         default=None,   help='end date to rework YYYY/MM/DD/HH')
    args = parser.parse_args()
    #print(args)
    if args.rework_from_now:
        if not args.hours: 
            print('Argument error : --hours must be set')
            exit()
        print('mode=rework_from_now '+str(args.hours))
        process_archive_minute(mode='rework_from_now', hours=args.hours)
    elif args.rework_from_date:
        if not args.hours: 
            print('Argument error : --hours must be set')
            exit()
        if not args.date: 
            print('Argument error : --date must be set')
            exit()

        date = args.date.split('/')
        print (date)
        try:
            dt_end = datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), 0, 0)
        except IndexError:
            print('Argument error : --date must be YYYY/MM/DD/HH')
            exit()
        print('mode=rework_from_date date='+str(dt_end)+' hours='+str(args.hours))
        process_archive_minute(mode='rework_from_date', date=dt_end, hours=args.hours)
    else:
        print('mode=normal')
        process_archive_minute(mode='normal')
            