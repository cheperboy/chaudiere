# -*- coding: ISO-8859-1 -*-
from __future__ import absolute_import

import os, click, sys, time
from random import randint
from datetime import datetime, timedelta

from flask.cli import FlaskGroup

from app import create_app, db
from app.models import Chaudiere, ChaudiereMinute, AdminConfig
from app.models.users import User

import config

import send_email_sms

import getpass#, bcrypt
from werkzeug.security import generate_password_hash

def create_my_app(info):
    from app import create_app
    return create_app()

@click.group(cls=FlaskGroup, create_app=create_my_app)
def cli():
    """This is a management script for the application."""

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

@cli.command()
def list_admin_config():
    for item in AdminConfig.all(AdminConfig):
        print("id {}\ntemp_chaudiere_failure {}".format(item.id, item.temp_chaudiere_failure))

if __name__ == '__main__':
    cli()