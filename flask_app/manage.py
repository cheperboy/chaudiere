# -*- coding: ISO-8859-1 -*-


from __future__ import absolute_import

import os, click, sys, time
from random import randint
from datetime import datetime, timedelta

from flask.cli import FlaskGroup

from app import create_app, db
from app.models import Chaudiere, ChaudiereMinute
import config

import send_email_sms

def create_my_app(info):
    from app import create_app
    return create_app()

@click.group(cls=FlaskGroup, create_app=create_my_app)
def cli():
    """This is a management script for the application."""

@cli.command()
def create_db():
    """Recreate the db tables."""
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def update_data():
    """ copy_prod_db_to_dev """
    if config.ENVNAME == 'Dev' :
        db.drop_all()
        db.create_all()
        db.session.commit()
        os.system("sudo rm -f /home/pi/Dev/db/chaudiere_minute.db")
        os.system("sudo rm -f /home/pi/Dev/db/chaudiere.db")
        os.system("cp /home/pi/Prod/db/chaudiere.db /home/pi/Dev/db/")
        os.system("cp /home/pi/Prod/db/chaudiere_minute.db /home/pi/Dev/db/")
        print ('Done')
    else:
        print ('Aborted. Env is '+config.ENVNAME)

@cli.command()
def test_mail():
    """ Send an Email """
    send_email_sms.Send_Mail_Test(['chaudiere.montlevic@gmail.com'])

@cli.command()
def test_sms():
    """ Send an SMS """
    send_email_sms.Send_SMS_Test('33688649102')

    
@cli.command()
def create_data():
    """Creates a data Entry."""
    for x in range(0, 100):
        me = Chaudiere(datetime.now(), x, 0, 0, 0, 0, 0, 0, None, None, None)
        db.session.add(me)
        db.session.commit()
        print (me)

"""Get Events."""

@cli.command()
def test(): 
    entries = ChaudiereMinute.all(ChaudiereMinute)
    out     = []
    total = len(entries)
    percent     = float(0)
    percent_old = float(0)
    iter        = float(0)
    for entry in entries:
        iter += 1
        percent = 100*(iter/total)
        #print ('iter : ' + str(iter/total))
        percent = int(percent)
        if percent != percent_old:
            percent_old = percent
            sys.stdout.write("\033[F")
            print (str(percent) + ' %')
        if entry.event is not None:
            out.append(entry)
    for entry in out:
        print (str(entry.dt) + ' ' + str(entry.event))
    print ('end')
 
 
# Supposed to be run every minute by cron to insert datas every minute in ChaudiereMinute database
@cli.command()
def insert_test_data_every_minute():
    dt = datetime.now().replace(second=0, microsecond=0)
    temp = dt.minute
    watt = 1
    # Save to db
    ChaudiereMinute.create(ChaudiereMinute, dt, temp, temp, temp, watt, watt, watt, watt, None, None, None)

@cli.command()
def print_last_entry():
    print(ChaudiereMinute.last(ChaudiereMinute))

if __name__ == '__main__':
    cli()