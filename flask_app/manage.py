# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os, click
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
        print 'Done'
    else:
        print 'Aborted. Env is '+config.ENVNAME

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
    me = Chaudiere(datetime.now())
    db.session.add(me)
    db.session.commit()
    print me

"""Get last data Entry."""
"""
@cli.command()
def test(): 
    entry = ChaudiereMinute.last(ChaudiereMinute)
    print entry
    prec = entry.prec()
    print prec
    precs = entry.precs(2)
    print precs
    print entry.precs_condition_at_least_one(2, 'prec.watt2 > 0') 
"""
if __name__ == '__main__':
    cli()