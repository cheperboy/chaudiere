# -*- coding: ISO-8859-1 -*-
"""
# script process_phase.py

## Summary

This script determines the `phase` value of ChaudiereMinute entries.
This script is supposed to be run every 1 or 2 minutes by cron

## CLI Usage :

Idem archive_minute.py

## CRON Config :

    1-59/2 * * * * /home/pi/Envs/dev/bin/python /home/pi/Dev/chaudiere/chaudiereapp/scripts/process_phase.py

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
import send_email_sms
from progress_bar import print_bar
from app import db
from app.models import ChaudiereMinute, timedelta_in_minute
from app.constantes import *
from app import create_app
app = create_app().app_context().push()

# import and get logger
logger_directory = os.path.join(projectpath, 'logger')
sys.path.append(logger_directory)
import logger_config
logger = logging.getLogger(__name__)

# import TEMP_CHAUDIERE_FAILURE from AdminConfig database
from app.models.admin_config import AdminConfig
admin_config = AdminConfig.first(AdminConfig)
if admin_config is not None:
    TEMP_CHAUDIERE_FAILURE = admin_config.temp_chaudiere_failure
else:
    logger.error("Could not fetch AdminConfig.temp_chaudiere_failure")

def temperature_variation(entry, periode):
    """
    retourne la variation de température (+/- Float) sur la période (minutes)
    retourne None si pas d'information
    si la période est incomplete (info capteurs absente), calcule avec une valeur plus récente
    """
    try:
        first_dt = entry.dt - timedelta(minutes=periode)
        dt = first_dt
        last_dt = entry.dt
        minute = 0
        old_entry = None
        # retourne la plus ancienne entry existante dans la période
        while old_entry is None and dt < last_dt:
            dt = first_dt + timedelta(minutes=minute)
            old_entry = ChaudiereMinute.get_by_datetime(ChaudiereMinute, dt)
            minute += 1
        
        old_temp = old_entry.get(TEMP_CHAUDIERE)
        temp = entry.get(TEMP_CHAUDIERE)
        return temp - old_temp
    except Exception as e:
        logger.warning("temperature variation failed ({0})".format(e))
        return None

def find_last_phase():
    """
    Return last processed ChaudiereMinute entry.dt or None
    """
    # if no ChaudiereMinute entry exists, return None
    if ChaudiereMinute.last(ChaudiereMinute) == None:
        return None
    
    # if some ChaudiereMinute entry exists but phase is None 
    # (first call of this script since db creation) :
    # return first ChaudiereMinute dt
    try_first = ChaudiereMinute.first(ChaudiereMinute)
    if try_first is not None and try_first.phase is None :
        logger.debug('returning first entry')
        return try_first.dt
    
    # else search for lat processed entry 
    dt = ChaudiereMinute.last(ChaudiereMinute).dt
    phase = None
    while (phase is None):
        dt = dt - timedelta(minutes=1)
        entry = ChaudiereMinute.get_by_datetime(ChaudiereMinute, dt)
        if entry is not None:
            phase = ChaudiereMinute.get_by_datetime(ChaudiereMinute, dt).phase
    logger.debug('last phase found is at : '+str(dt))
    return dt
        
def find_date_end(date):
    """
    return the datetime of an existing Chaudiere entry close to the given *date* parameter
    """
    last_ch_minute_date = ChaudiereMinute.last(ChaudiereMinute).dt
    entry = ChaudiereMinute.get_by_datetime(ChaudiereMinute, date)
    while ((entry is None) and (date < last_ch_minute_date)):
        date = date + timedelta(minutes=1)
        entry = ChaudiereMinute.get_by_datetime(ChaudiereMinute, date)
    logger.debug('found ChaudiereMinute at (dt end):'+ str(entry.dt))
    return entry.dt
        
def process_phase(mode='normal', hours=None, date=None):
    """ 
    Détermine la date de début (begin) et de fin (end) des minutes à traiter en fonction du `mode`
    """
    disable_alert = False
    if mode is 'normal':
        begin = find_last_phase() # begin = last processed ChaudiereMinute entry.dt
        end = ChaudiereMinute.last(ChaudiereMinute).dt # end = last existing ChaudiereMinute entry.dt
    elif mode is 'rework_from_now':
        disable_alert = True
        end = ChaudiereMinute.last(ChaudiereMinute).dt
        begin = end - timedelta(hours=hours)
    elif mode is 'rework_from_date':
        disable_alert = True
        end = find_date_end(date)
        begin = end - timedelta(hours=hours)
    else:
        logger.error('wrong arguments')
        return
    if begin is None:
        logger.info('No records')
        return
    
    if ((begin + timedelta(minutes=1)) >= end):
        logger.info('Strating from '+str(begin)+' ...Waiting more records')
    else:
        logger.info('processing phase From ' + str(begin) + ' To ' + str(end))

    # Progress bar Init (for console mode)
    bar_items = timedelta_in_minute(begin, end)
    bar_item = 0
    
    # while some entries to process
    while ((begin + timedelta(minutes=1)) <= end):
        entry = ChaudiereMinute.get_by_datetime(ChaudiereMinute, begin) 
        # entry should not be missing, test just in case and create missing entry
        if entry is None:
            logger.warning('create missing ChaudiereMinute entry (should not be the case')
            ChaudiereMinute.create(ChaudiereMinute, begin, None, None, None, None, None, None, None, None, None, None)
        entry = ChaudiereMinute.get_by_datetime(ChaudiereMinute, begin)
        
        # Progress bar Print (for console mode)
        bar_item += 1
        # print_bar(bar_item, bar_items, prefix=str(entry.dt))
        
        update_phase(entry)
        update_change(entry)
        process_alerts(entry, disable_alert)
        begin = begin + timedelta(minutes=1)
        


def update_phase(entry):
    """
    Met à jour le champ phase en fonction des valeur ventilateur, température, allumeur
    """
    # Si des informations capteurs sont disponibles
    if entry.get(ALLUMAGE) is not None and\
        entry.get(VENT_PRIMAIRE) is not None and\
        entry.get(TEMP_CHAUDIERE) is not None:

            # détecter l'allumage (allumeur > 0)
            if (entry.get(ALLUMAGE) > 0):
                entry.phase = PHASE_ALLUMAGE
                db.session.commit()

            # Détecter la combustion (ventilateur > 0 et allumeur == 0)
            elif entry.get(VENT_PRIMAIRE) > 0:
                entry.phase = PHASE_COMBUSTION
                db.session.commit()

            # Détecter le maintien de feu (vent == 0 et allumeur == 0)
            elif entry.get(VENT_PRIMAIRE) == 0:
                entry.phase = PHASE_MAINTIEN
                db.session.commit()

            # Détecter l'arrêt (condition température basse : temp_chaudiere < TEMP_CHAUDIERE_FAILURE) 
            # malgré la condition température basse, 
            # - si allumeur en marche => ALLUMAGE
            # - si ventilateur en marche et allumeur à été en marche [depuis moins de 20 minutes] => COMBUSTION
            # - si ventilateur en marche et température augmente [10 min] => COMBUSTION
            # - cas non nominal : si ventilateur en marche et température diminue pendant + de 30 minutes => BOURRAGE
            if entry.get(TEMP_CHAUDIERE) < TEMP_CHAUDIERE_FAILURE:
                # Si allumeur en marche => ALLUMAGE
                if entry.get(ALLUMAGE) > 0:
                    entry.phase = PHASE_ALLUMAGE
                    db.session.commit()
            
                # Si ventilateur en marche et allumeur à été en marche [depuis moins de 20 minutes] => COMBUSTION
                elif entry.get(VENT_PRIMAIRE) > 0:
                    condition_precs_was_allumage = '((prec is not None) and (prec.phase == '+str(PHASE_ALLUMAGE)+' ))'
                    if entry.at_least_one_prec_verify_condition(20, condition_precs_was_allumage):
                        entry.phase = PHASE_SURVEILLANCE
                        db.session.commit()
                    
                    # Si ventilateur en marche et température augmente [10 min] => COMBUSTION
                    delta_temp = temperature_variation(entry, 10)
                    if delta_temp is not None and delta_temp > 0.2:
                        entry.phase = PHASE_SURVEILLANCE
                        db.session.commit()

                    # Cas non nominal : si ventilateur en marche et température diminue pendant + de 30 minutes => BOURRAGE
                    delta_temp = temperature_variation(entry, 30)
                    if delta_temp is not None and delta_temp < 1.0:
                        entry.phase = PHASE_RISQUE_BOURAGE
                        db.session.commit()
                        
                # Dans tout les autres cas (par défaut) => ARRET
                else:
                    entry.phase = PHASE_ARRET
                    db.session.commit()
                    
    # cas par défaut, aucune information des capteurs disponible, phase est UNDEFINED
    else:
        entry.phase = PHASE_UNDEFINED
        db.session.commit()

def update_change(entry):
    """
    Met a jour le champ "chaudiere.change" si phase courante est différent de phase prec
    """
    #condition_prec_has_same_phase = '((prec is not None) and (prec.phase == '+str(entry.get(PHASE))+' or prec.phase == PHASE_UNDEFINED ))'
    if entry.prec() is not None and entry.prec().phase != entry.phase:
        entry.change = True
    else:
        entry.change = False
    db.session.commit()

def process_alerts(entry, disable_alert):
    """
    Envoi une alerte (mail, sms) si phase courante est ALERT et si change est True
    et si aucun des precs n'etaient deja en ALERT (cette condition permet de la gestion de la séquence
    ALERT -> UNDEFINED -> ALERT (change == True)
    Si une alerte est envoyee, alors le champ entry.event vaut "Alert mail/sms"
    """
    condition_precs_was_not_alert = '((prec is not None) and (prec.phase != '+str(PHASE_ARRET)+' ))'
    if entry.change is True and\
      entry.phase == PHASE_ARRET and\
      entry.all_prec_verify_condition(10, condition_precs_was_not_alert):
        if disable_alert is False:
            if envname == 'Prod':
                logger.info('Sending email/sms alert for entry :'+str(entry.dt))
                send_email_sms.Send_Mail_Chaudiere_Alert(entry.dt)
                send_email_sms.Send_SMS_Chaudiere_Alert(entry.dt)
            else:
                logger.info('Not Sending email/sms alert (not Prod env) for entry :'+str(entry.dt))
        else:
            logger.info('Not Sending email/sms alert (already sent previously) for entry :'+str(entry.dt))
        entry.event = EVENT_ALERT
        db.session.commit()

def test_alerts():
    logger.debug('test_alerts()')
    entry = ChaudiereMinute.last(ChaudiereMinute)
    send_email_sms.Send_Mail_Chaudiere_Alert(entry.dt)
    send_email_sms.Send_SMS_Chaudiere_Alert(entry.dt)


  
if __name__ == '__main__':
    
    # PARSE ARGS 
    parser = argparse.ArgumentParser(description = "process phase calculation", epilog = "" )
    #group = parser.add_mutually_exclusive_group()
    
    parser.add_argument('--test_alerts',            action='store_true',  default=False, dest='test_alerts',        help='test email and sms alerts')
    parser.add_argument('--rework_from_now',        action='store_true',  default=False, dest='rework_from_now',    help='rework N hours from now')
    parser.add_argument('--rework_from_date',       action='store_true',  default=False, dest='rework_from_date',   help='rework N hours from given END date')
    parser.add_argument('--hours',                  type=int,             default=None,                             help='number of hour to rework')
    parser.add_argument('--date',                                         default=None,                             help='end date to rework YYYY/MM/DD/HH')
    args = parser.parse_args()
    print (args)
    if args.test_alerts:
        print('sending test alerts')
        test_alerts()
    elif args.rework_from_now:
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
        print (date)
        try:
            ts_end = datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), 0, 0)
            print (ts_end)
            print (str(ts_end))
        except IndexError:
            print('Argument error : --date must be YYYY/MM/DD/HH')
            exit()
        print('mode=rework_from_date date='+str(ts_end)+' hours='+str(args.hours))
        process_phase(mode='rework_from_date', date=ts_end, hours=args.hours)
    else:
        print('mode=normal')
        process_phase(mode='normal')
