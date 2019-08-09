# -*- coding: ISO-8859-1 -*-
from __future__ import absolute_import

import os, click, sys, time
from random import randint
from datetime import datetime, timedelta

from flask.cli import FlaskGroup

from app import create_app, db
from app.models import Chaudiere, ChaudiereMinute
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

#############
# Manage Database #
#############

@cli.command()
@click.option('--delete_users_db', prompt='delete also users db (y/n) ?')
@click.option('--delete_admin_config_db', prompt='delete also admin_config db (y/n) ?')
def create_db(delete_users_db, delete_admin_config_db):
    """Recreate the db tables."""
    all_db_except_users_and_config = ['chaudiere', 'chaudiere_minute', 'admin_config']
    db.drop_all(all_db_except_users_and_config)
    db.create_all(all_db_except_users_and_config)
    if delete_users_db == 'y':
        db.drop_all('users')
        db.create_all('users')
    if delete_admin_config_db == 'y':
        db.drop_all('admin_config')
        db.create_all('admin_config')
    # db.session.commit()

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

#############
# Test Mail #
#############
@cli.command()
@click.option('--email', prompt='send to which email ?')
def test_mail(email):
    """ Send an Email """
    send_email_sms.Send_Mail_Test([email])

#############
# Test SMS #
#############
@cli.command()
def test_sms():
    """ Send an SMS """
    send_email_sms.Send_SMS_Test('33688649102')

###########
# Manage Users #
###########
@cli.command()
def list_users():
    """ List admin users """
    for user in User.all(User):
        print (user.id, user.name, user.email)
    
@click.option('--name')
@cli.command()
def delete_user(name):
    """ delete_user --name toto """
    user = User.get_by_name(User, name)
    db.session.delete(user)
    db.session.commit()
    
@cli.command()
def create_user():
    """ Create an admin user """
    print ("List of existing users :")
    for user in User.all(User):
        print (user.id, user.name, user.email)
    print ()
    print ("New user")
    print ('Enter name: ')
    name = input()
    print ('Enter email: ')
    email = input()
    password = getpass.getpass()
    assert password == getpass.getpass('Password (again):')

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    
    print ('User added.')

if __name__ == '__main__':
    cli()