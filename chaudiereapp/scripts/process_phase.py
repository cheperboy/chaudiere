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
from app import create_app
app = create_app().app_context().push()

PHASE_UNDEFINED  = 0
PHASE_COMBUSTION = 6
PHASE_ALLUMAGE   = 7
PHASE_MAINTIEN   = 8
PHASE_ARRET      = 9

# import ../../script/logger_config to get logger
chaudierescript = os.path.join(projectpath, 'script')
sys.path.append(chaudierescript)
import logger_config

# SET LOGGER
logger = logging.getLogger(__name__)

def find_last_phase():
    #for debug purpose
    #return ChaudiereMinute.first(ChaudiereMinute).timestamp

    logger.info('find_last_phase()')
    if ChaudiereMinute.last(ChaudiereMinute) == None:
        logger.debug('return None')
        return None
    timestamp = ChaudiereMinute.last(ChaudiereMinute).timestamp 
    phase = None
    while (phase is None):
        logger.info(str(timestamp))
        timestamp = timestamp - timedelta(minutes=1)
        entry = ChaudiereMinute.get_by_date(ChaudiereMinute, timestamp)
        if entry is not None:
            phase = ChaudiereMinute.get_by_date(ChaudiereMinute, timestamp).phase
    logger.info('timestamp : '+str(timestamp))
    return timestamp
        

#run every 15 min
def process_phase():
    logger.info('process_phase()')
    # defini date de debut et de fin 
    # begin = (date du dernier record de la base Archive) + 1 minute
    # end = (maintenant) - 1 minute
    
    # if ChaudiereMinute is empty then we start with the first Chaudiere record (oldest)
    begin = find_last_phase()
    if begin is None:
        logger.info('No records')
        return
    
    # we finish with the last Chaudiere record (replace second to zero to avoid incomplete current minute)
    end = ChaudiereMinute.last(ChaudiereMinute).timestamp
    logger.info('Entries to process ' + str(begin) + ' -> ' + str(end))
    
    if ((begin + timedelta(minutes=1)) > end):
        logger.info('Waiting more records')
    # while some old Logs to Archive
    while ((begin + timedelta(minutes=1)) <= end):
        entry = ChaudiereMinute.get_by_timestamp(ChaudiereMinute, begin) 
        if entry is None:
            #shall be deleted, now done in archive_minute
            logger.error('create missing ChaudiereMinute entry')
            ChaudiereMinute.create(ChaudiereMinute, timestamp, None, None, None, None, None, None, None, None, None)
        entry = ChaudiereMinute.get_by_timestamp(ChaudiereMinute, begin) 
        logger.info('update_phase_allumage(entry, begin)' +str(entry)+' '+ str(begin))
        update_phase_allumage(entry, begin)
        begin = begin + timedelta(minutes=1)

#ASC : plus ancient 
#DESC : plus recent
'''
recupere dans la base Logs l'ensenmble des objets dont la date est comprise entre 
begin et (begin + 1 minute)
Calcule des moyennes et enregistre
'''
def update_phase_allumage(entry, timestamp):
    """ Process Allumage"""
    if entry.watt1 is not None: #watt allumage
        if entry.watt1 > 0:
            entry.phase = PHASE_ALLUMAGE
            db.session.commit()
            logger.debug(str(entry.watt1)+' '+ str(entry.timestamp) +' Phase Allumage')
    """
    si vent > 0 and prec(4) was > 0 => COMBUSTION

    gestion debut du process (pas dhistorique donc jamais de combustion)
    si vent > 0 and pas dhistorique (prec(4) was None) => COMBUSTION

    si vent = 0 and prec(4) was combustion => MAINTIEN  
    """

    """ Process Combustion or Maintien"""
    if (entry.watt2 is not None):
        if entry.watt2 > 0: #watt vent primaire

            """ Process Maintien"""
            """si vent > 0 and prec(4) was > 0 => COMBUSTION"""
            condition = 'prec.watt2 > 0'
            if entry.at_least_one_prec_verify_condition(5, condition):
                entry.phase = PHASE_COMBUSTION
                db.session.commit()
                logger.debug(str(entry.timestamp) +' vent > 0 and prec(4) was > 0 => COMBUSTION')

            """si vent > 0 and pas d'historique (prec(4) was None) => COMBUSTION"""
            condition = '((prec is None) or (prec.watt2 is None))'
            if entry.at_least_one_prec_verify_condition(5, condition):
                entry.phase = PHASE_COMBUSTION
                db.session.commit()
                logger.debug(str(entry.timestamp) +' si vent > 0 and pas dhistorique (prec(4) was None) => COMBUSTION')
            
        if entry.watt2 == 0: #watt vent primaire
            """si prec(4) was combustion and vent = 0 => MAINTIEN"""
            condition = '((prec is not None) and (prec.phase is 6))'
            if entry.at_least_one_prec_verify_condition(5, condition):
                entry.phase = PHASE_MAINTIEN
                db.session.commit()
                logger.debug(str(entry.timestamp) +' si vent = 0 and prec(4) was combustion => MAINTIEN')
            
    #else:
    if (entry.phase is None):
        entry.phase = PHASE_UNDEFINED
        db.session.commit()
        logger.debug(str(entry.timestamp) +' PHASE_UNDEFINED')
    
    
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
    process_phase()
    """
    if args.minute:
        process_archive_minute()
    """