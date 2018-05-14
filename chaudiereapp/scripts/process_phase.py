'''
Summary:
python script used to store average values (Minutes, Hour, ...) of Teleino SQLA Database.
supposed to be run every 10 minutes by cron

CLI Usage :
workon venv
python teleinfo_archive.py --archive_hour

CRON Config :
python teleinfo_archive.py --archive_hour

Description
Database Model and usefull models methods are imported from teleinfoapp (app.models and app.models_util)
Le fait d'appeler l'option --archive_hour provoque d'abord l'appel de archive_minute

'''


import os, sys, argparse
from datetime import datetime, timedelta
import logging, logging.config

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/chaudiereapp/script
chaudiereapp = os.path.dirname(currentpath)              # /home/pi/Dev/chaudiere/chaudiereapp
projectpath = os.path.dirname(chaudiereapp)              # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                   # /home/pi/Dev
envname = os.path.basename(envpath)                      # Dev

# import ../app/ 
app_path = os.path.join(chaudiereapp, 'app')
sys.path.append(chaudiereapp)
from app import db
from app.models import ChaudiereMinute
from app.constantes import *
from app import create_app
app = create_app().app_context().push()

# import ../../script/logger_config to get logger
chaudierescript = os.path.join(projectpath, 'script')
sys.path.append(chaudierescript)
import logger_config

# SET LOGGER
logger = logging.getLogger(__name__)

def find_last_phase():
    logger.info('find_last_phase()')
    if ChaudiereMinute.last(ChaudiereMinute) == None:
        logger.debug('return None')
        return None
    # if new db:
    try_first = ChaudiereMinute.first(ChaudiereMinute)
    if try_first is not None and try_first.phase is None :
        logger.debug('returning first entry')
        return try_first.dt
    # else search for lat processed entry 
    dt = ChaudiereMinute.last(ChaudiereMinute).dt
    phase = None
    while (phase is None):
        logger.info(str(dt))
        dt = dt - timedelta(minutes=1)
        entry = ChaudiereMinute.get_by_datetime(ChaudiereMinute, dt)
        if entry is not None:
            phase = ChaudiereMinute.get_by_datetime(ChaudiereMinute, dt).phase
    logger.info('date : '+str(dt))
    return dt
        
def find_date_end(date):
    last_ch_minute_date = ChaudiereMinute.last(ChaudiereMinute).dt
    entry = ChaudiereMinute.get_by_datetime(ChaudiereMinute, date)
    while ((entry is None) and (date < last_ch_minute_date)):
        date = date + timedelta(minutes=1)
        entry = ChaudiereMinute.get_by_datetime(ChaudiereMinute, date)
    print ('ChaudiereMinute.dt end:'+ str(entry.dt))
    return entry.dt
        
#run every 15 min
def process_phase(mode='normal', hours=None, date=None):
    logger.info('process_phase()')
    
    # defini date de debut et de fin 
    if mode is 'normal':
        # begin = (date du dernier record de la base Archive) + 1 minute
        # end = (maintenant) - 1 minute        
        # if ChaudiereMinute is empty then we start with the first Chaudiere record (oldest)
        begin = find_last_phase()
        # we finish with the last Chaudiere record (replace second to zero to avoid incomplete current minute)
        end = ChaudiereMinute.last(ChaudiereMinute).dt
    elif mode is 'rework_from_now':
        #negin is last existing ChaudiereMinute - N hours
        dt = ChaudiereMinute.last(ChaudiereMinute).dt 
        begin = dt - timedelta(hours=hours)
        # we finish with the last Chaudiere record (replace second to zero to avoid incomplete current minute)
        end = ChaudiereMinute.last(ChaudiereMinute).dt
    elif mode is 'rework_from_date':
        end = find_date_end(date)
        print ('ChaudiereMinute.dt end:'+ str(end))
        begin = end - timedelta(hours=hours)
    else:
        logger.error('wrong arguments')
        return
    if begin is None:
        logger.info('No records')
        return
    logger.info('Entries to process ' + str(begin) + ' -> ' + str(end))
    
    if ((begin + timedelta(minutes=1)) > end):
        logger.info('Waiting more records')
    # while some old Logs to Archive
    while ((begin + timedelta(minutes=1)) <= end):
        entry = ChaudiereMinute.get_by_datetime(ChaudiereMinute, begin) 
        if entry is None:
            #shall be deleted, now done in archive_minute
            logger.error('create missing ChaudiereMinute entry')
            ChaudiereMinute.create(ChaudiereMinute, begin, None, None, None, None, None, None, None, None, None)
        entry = ChaudiereMinute.get_by_datetime(ChaudiereMinute, begin)
        update_phase_allumage(entry)
        begin = begin + timedelta(minutes=1)

#ASC : plus ancient 
#DESC : plus recent
'''
recupere dans la base Logs l'ensenmble des objets dont la date est comprise entre 
begin et (begin + 1 minute)
Calcule des moyennes et enregistre
'''
"""
ALGO 2
Si vent = 0 => MAintien
Si vent > 0 => combustion
"""

def update_phase_allumage(entry):
    if entry.watt1 is not None and\
       entry.watt2 is not None and\
       entry.temp0 is not None:
        """ Process Allumage"""
        if entry.watt1 > 0: #watt allumage
            entry.phase = PHASE_ALLUMAGE
            db.session.commit()
            print(str(entry.dt)+' watt1 :'+str(entry.watt1)+' '+ PhaseName[PHASE_ALLUMAGE])

        elif entry.watt2 > 0: #watt vent primaire
            """Si vent > 0 => combustion"""
            entry.phase = PHASE_COMBUSTION
            db.session.commit()
            print(str(entry.dt)+' watt2 :'+str(entry.watt2)+' '+ PhaseName[PHASE_COMBUSTION])

        elif entry.watt2 == 0: #watt vent primaire
            """si vent == 0 => MAINTIEN"""
            entry.phase = PHASE_MAINTIEN
            db.session.commit()
            print(str(entry.dt)+' watt2 :'+str(entry.watt2)+' '+ PhaseName[PHASE_MAINTIEN])

        if entry.temp0 < 40: #temp is too low
            """si temp_chaudiere < 40 => ARRET"""
            entry.phase = PHASE_ARRET
            db.session.commit()
            print(str(entry.dt)+' temp0 :'+str(entry.temp0)+' '+ PhaseName[PHASE_ARRET])
    
    else: #(entry.phase is None)
        entry.phase = PHASE_UNDEFINED
        db.session.commit()
        print(str(entry.dt) +' '+PhaseName[PHASE_UNDEFINED])

    
if __name__ == '__main__':
    
    # PARSE ARGS 
    parser = argparse.ArgumentParser(description = "process phase calculation", epilog = "" )
    #group = parser.add_mutually_exclusive_group()
    
    parser.add_argument('--rework_from_now',        action='store_true',  default=False, dest='rework_from_now',  help='rework N hours from now')
    parser.add_argument('--rework_from_date',       action='store_true',  default=False, dest='rework_from_date',  help='rework N hours from given END date')
    parser.add_argument('--hours',                  type=int,             default=None,   help='number of hour to rework')
    parser.add_argument('--date',                                         default=None,   help='end date to rework YYYY/MM/DD/HH')
    args = parser.parse_args()
    print(args)
    if args.rework_from_now:
        if not args.hours: 
            print('Argument error : --hours must be set')
            exit()
        print('mode=rework_from_now '+str(args.hours))
        process_phase(mode='rework_from_now', hours=args.hours)
    elif args.rework_from_date:
        #python process_phase.py --rework_from_date --hours 10 --date 2018/05/9/10
        if not args.hours: 
            print('Argument error : --hours must be set')
            exit()
        if not args.date: 
            print('Argument error : --date must be set')
            exit()

        date = args.date.split('/')
        print date
        try:
            ts_end = datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), 0, 0)
            print ts_end
            print str(ts_end)
        except IndexError:
            print('Argument error : --date must be YYYY/MM/DD/HH')
            exit()
        print('mode=rework_from_date date='+str(ts_end)+' hours='+str(args.hours))
        process_phase(mode='rework_from_date', date=ts_end, hours=args.hours)
    else:
        print('mode=normal')
        process_phase(mode='normal')
