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
from app.models import Chaudiere, ChaudiereMinute
from app import create_app
app = create_app().app_context().push()


# import ../../script/logger_config to get logger
chaudierescript = os.path.join(projectpath, 'script')
sys.path.append(chaudierescript)
import logger_config

# SET LOGGER
logger = logging.getLogger(__name__)

#run every 15 min
def process_archive_minute():
    # defini date de debut et de fin 
    # begin = (date du dernier record de la base Archive) + 1 minute
    # end = (maintenant) - 1 minute
    
    # if ChaudiereMinute is empty then we start with the first Chaudiere record (oldest)
    if ChaudiereMinute.last(ChaudiereMinute) == None:
        begin = Chaudiere.first(Chaudiere).timestamp.replace(second=0, microsecond=0) 
        #begin = Chaudiere.last(Chaudiere).timestamp - timedelta(hours=6) 

    # else ChaudiereMinute is NOT empty then we start with the last ChaudiereMinute record (newest)
    else:
        begin = (ChaudiereMinute.last(ChaudiereMinute).timestamp + timedelta(minutes=1)).replace(second=0, microsecond=0)
    
    # we finish with the last Chaudiere record (replace second to zero to avoid incomplete current minute)
    end = (Chaudiere.last(Chaudiere).timestamp).replace(second=0, microsecond=0)
    logger.info('Minute to archive ' + str(begin) + ' -> ' + str(end))
    
    if ((begin + timedelta(minutes=1)) > end):
        logger.info('Waiting more records')
    # while some old Logs to Archive
    while ((begin + timedelta(minutes=1)) <= end):
        record_minute(begin)
        begin = begin + timedelta(minutes=1)

#ASC : plus ancient 
#DESC : plus recent
'''
recupere dans la base Logs l'ensenmble des objets dont la date est comprise entre 
begin et (begin + 1 minute)
Calcule des moyennes et enregistre
'''
def record_minute(begin):
    logger.debug('record minute')
    #fake begin/end
#    begin = datetime.now() - timedelta(minutes=3)
    
    end = begin + timedelta(minutes=1)
    logger.info('Archiving minute ' + str(begin) + ' -> ' + str(end))
    #print('minute ' + str(begin) + ' -> ' + str(end))
    temp0 = 0.0
    temp1 = 0.0
    watt1 = 0
    watt2 = 0
    watt3 = 0
    # get logs
    logs = Chaudiere.get_between_date(Chaudiere, begin, end)
    nb_logs = len(logs)
    logger.debug('nb_logs=' + str(nb_logs))
    if nb_logs > 0:
        for log in logs:
            if (log.temp0 is not None): temp0 += float(log.temp0)
            if (log.temp1 is not None): temp1 += float(log.temp1)
            if (log.watt1 is not None): watt1 += int(log.watt1)
            if (log.watt2 is not None): watt2 += int(log.watt2)
            if (log.watt3 is not None): watt3 += int(log.watt3)
        # calcule des moyennes sur les series
        temp0 = temp0 / nb_logs
        temp1 = temp1 / nb_logs
        watt1 = watt1 / nb_logs
        watt2 = watt2 / nb_logs
        watt3 = watt3 / nb_logs
        # Save to db
        ret = ChaudiereMinute.create(ChaudiereMinute, begin, temp0, temp1, None, None, watt1, watt2, watt3, None, None)
        logger.debug('ret = ' + str(ret))
    else:
        ret = ChaudiereMinute.create(ChaudiereMinute, begin, None, None, None, None, None, None, None, None, None)

if __name__ == '__main__':
    
    # PARSE ARGS
    parser = argparse.ArgumentParser(description = "Archive Chaudiere in Minute and Hour db", epilog = "" )
    parser.add_argument("-v",
                          "--verbose",
                          help="increase output verbosity",
                          action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--minute", action="store_true")
    args = parser.parse_args()
    logger.info('START (last Chaudiere recrod = ' + str(Chaudiere.last(Chaudiere).timestamp))
    if args.minute:
        process_archive_minute()
    