# -*- coding: ISO-8859-1 -*-

import os, click, sys, time
from random import randint
from datetime import datetime, timedelta

import getpass
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import Chaudiere, ChaudiereMinute
from app.models.users import User
import config
import send_email_sms

@click.group()
def manager():
    pass

@click.group()
def database(): pass
manager.add_command(database)

@click.group()
def users(): pass
manager.add_command(users)

@click.group()
def test(): pass
manager.add_command(test)

@click.group() 
def fakedata(): pass
manager.add_command(fakedata)

############
# Database #
############
@database.command()
def init_all():
    """Recreate All the db tables."""
    db.drop_all()
    db.create_all()

@database.command()
@click.option('--delete_users_db', prompt='delete also users db (y/n) ?')
@click.option('--delete_admin_config_db', prompt='delete also admin_config db (y/n) ?')
def init(delete_users_db, delete_admin_config_db):
    """Recreate the db tables except the one specified with cli option"""
    all_db_except_users_and_config = ['chaudiere', 'chaudiere_minute']
    db.drop_all(all_db_except_users_and_config)
    db.create_all(all_db_except_users_and_config)
    if delete_users_db == 'y':
        db.drop_all('users')
        db.create_all('users')
    if delete_admin_config_db == 'y':
        db.drop_all('admin_config')
        db.create_all('admin_config')
    # db.session.commit()

@click.argument('database')
@database.command()
def rotate(database):
    """ Rotate database 'Chaudiere' or 'ChaudiereMinute' """
    if database not in ['Chaudiere', 'ChaudiereMinute']:
        print("database not in ['Chaudiere', 'ChaudiereMinute']. Return.")
        return()
        
    # import chaudiere_(minute)_db_rotate_days from AdminConfig database
    from app.models.admin_config import AdminConfig
    admin_config = AdminConfig.first(AdminConfig)
    if admin_config is not None:
        if database == 'Chaudiere':
            timedelta_config = admin_config.chaudiere_db_rotate_hours
        elif database == 'ChaudiereMinute':
            timedelta_config = admin_config.chaudiere_minute_db_rotate_days
    else:
        logger.error("Could not fetch AdminConfig.chaudiere_(minute)_db_rotate_days")
    
    # Retrieve entries betwenn now and passed date (number of days defined by AdminConfig parameter)
    # delete the selected entries
    Model = eval(database)
    dt_end = datetime.now() - timedelta(days=timedelta_config)
    # dt_end = datetime.now() - timedelta(minutes=timedelta_config)
    entries = Model.get_older_than(Model, dt_end)
    for e in entries:
        db.session.delete(e)
    print("deleting "+ str(len(entries)) +" entries")
    db.session.commit()
        
@click.argument('database')
@click.option('-c', '--count', is_flag=True, help='just count the number of entries')
@database.command()
def list_all(database, count):
    """ List all entries of a db (or just count them) 
    list_all ChaudiereMinute [--count]
    """
    Model = eval(database)
    # entries = Model.all(Model).order_by(id, desc)
    entries = db.session.query(Model).order_by(Model.id.asc()).all()
    if count:
        print (len(entries))
    else:
        for e in entries:
            print (e)
        
@click.argument('database')
@database.command()
def first(database):
    """ List first entry of a db
    """
    Model = eval(database)
    e = db.session.query(Model).order_by(Model.id.asc()).first()
    print (e)
        
@click.argument('database')
@database.command()
def last(database):
    """ List first entry of a db
    """
    Model = eval(database)
    e = db.session.query(Model).order_by(Model.id.desc()).first()
    print (e)
        
@database.command()
def copy_prod_to_dev():
    """ copy chaudiere.db & chaudiere_minute.db from prod to dev """
    if config.ENVNAME == 'Dev' :
        # db.drop_all()
        # db.create_all()
        # db.session.commit()
        os.system("sudo rm -f /home/pi/Dev/db/chaudiere_minute.db")
        os.system("cp /home/pi/Prod/db/chaudiere_minute.db /home/pi/Dev/db/")
        os.system("sudo rm -f /home/pi/Dev/db/chaudiere.db")
        os.system("cp /home/pi/Prod/db/chaudiere.db /home/pi/Dev/db/")
        print ('Done')
    else:
        print ('Aborted. Env is '+config.ENVNAME)

###########
# Manage Users #
###########
@users.command()
def list():
    """ List admin users """
    for user in User.all(User):
        print (user.id, user.name, user.email)
    
@click.option('--name')
@users.command()
def delete(name):
    """user delete --name toto """
    user = User.get_by_name(User, name)
    db.session.delete(user)
    db.session.commit()
    
@users.command()
def create():
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

###################
# Test Mail & SMS #
###################
@test.command()
@click.option('--email', prompt='send to which email ?')
def mail(email):
    """ Send an Email """
    send_email_sms.Send_Mail_Test([email])

@test.command()
def sms():
    """ Send an SMS """
    send_email_sms.Send_SMS_Test('33688649102')

#####################
# Create fake datas #
#####################
@click.argument('minutes')
@fakedata.command()
def chaudiereminute(minutes):
    """Creates fake ChaudiereMinute entries every minute from now to a past date defined by a number of minutes from now (given by argument)    
    """
    now = datetime.now()
    for x in range(0, int(minutes)):
        dt = now - timedelta(minutes=x)
        rec = ChaudiereMinute(dt, 70, 0, 0, 0, 0, 0, 0, None, None, None)
        db.session.add(rec)
        print (rec)
    db.session.commit()

@click.argument('seconds')
@fakedata.command()
def chaudiere(seconds):
    """Creates fake Chaudiere entries every 20 second from now to a past date defined by a number of second from now (given by argument)    
    """
    now = datetime.now()
    for x in range(0, int(seconds), 20):
        dt = now - timedelta(seconds=x)
        rec = Chaudiere(dt, 70, 0, 0, 0, 0, 0, 0, None, None, None)
        db.session.add(rec)
        print (rec)
    db.session.commit()


    
if __name__ == '__main__':
    app= create_app()
    with app.app_context():
        manager()
  