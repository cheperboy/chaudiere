# -*- coding: ISO-8859-1 -*-
import os, sys
from subprocess import call             # to execute a shell command
from threading import Thread            # to launch an async thread
import datetime
from flask_mail import Message
from app import mail, create_app
from util import pretty_date
import logging, logging.config

from flask import current_app as app
import nexmo

# import and get logger
flaskapp = os.path.abspath(os.path.dirname(__file__))   # /home/pi/Dev/chaudiere/flaskapp
projectpath = os.path.dirname(flaskapp)                 # /home/pi/Dev/chaudiere
logger_directory = os.path.join(projectpath, 'logger')
sys.path.append(logger_directory)
import logger_config
logger = logging.getLogger(__name__)

# Create app instance
app = create_app()

# Create Nexmo instance
sms_gateway = nexmo.Client(key=app.config['NEXMO_API_KEY'], secret=app.config['NEXMO_API_SECRET'])

def send_async_sms(app, sender, recipient, body):
    """ Call nexmo library to send sms """
    with app.app_context():
        sms = {
            'from': sender,
            'to': recipient,
            'text': body
        }
        logger.debug('Sending SMS')
        logger.debug(str(sms))
        sms_gateway.send_message(sms)

def send_sms(sender, recipients, body):
    """ Start N Threads for the N recipients 
    Each Thread will call the function send_async_sms"""
    for recipient in recipients:
        thr = Thread(target=send_async_sms, args=[app, sender, recipient, body])
        thr.start()

def Send_SMS_Chaudiere_Alert(dt):
    """ To be called by ext package
    Prepare an sms to Alert all recipients """
    date        = pretty_date(dt)
    body        = '''Alerte Temperature basse atteinte. le ''' + date
    sender      = 'Chaudiere Montlevic'
    recipients  = app.config['USERS_PHONES']
    send_sms(sender, recipients, body)
        
def Send_SMS_Test(recipient):
    """ For testing purpose only
    send a sms to one recipient """
    recipients = []
    recipients.append(recipient)
    date    = datetime.datetime.now()
    body    = "Test SMS {0}".format(date)
    sender  = 'Chaudiere Montlevic'
    send_sms(sender, recipients, body)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

def Send_Mail_Chaudiere_Alert(dt):
    date = pretty_date(dt)
    subject   = '''Alerte Arret Chaudiere le {0}'''.format(date)
    html_body = '''
    Température basse atteinte (T<65°) <br>
    historique des 12 dernières heures : http://montlevic.hd.free.fr:5007/charts/now/12
    '''
    body = '''
    Température basse atteinte (T<65°)
    http://montlevic.hd.free.fr:5007/charts/now/6
    '''
    sender      = app.config['MAIL_USERNAME']
    recipients  = app.config['USERS_EMAILS']
    send_email(subject, sender, recipients, body, html_body)

def Send_Mail_Test(recipients):
    date = datetime.datetime.now()
    subject     = "Chaudiere Test Mail {0}".format(date)
    html_body   = subject
    body        = subject
    sender      = app.config['MAIL_USERNAME']
    send_email(subject, sender, recipients, body, html_body)
