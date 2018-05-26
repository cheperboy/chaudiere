# -*- coding: utf-8 -*-
from threading import Thread
import datetime
from flask_mail import Message
from app import mail, create_app
from util import pretty_date
from flask import current_app as app
#from config import USERS_EMAILS, MAIL_USERNAME

app = create_app()

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

"""
msg = Message('test 3', sender=MAIL_USERNAME, recipients=USERS_EMAILS)
body = 'Alert'
html = '<b>Alert</b>'
send_email('test 4', 'chaudiere.montlevic@gmail.com', ['matthieujouve@gmail.com'], body, html)
"""

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
