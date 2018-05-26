""" App configuration."""
import os, sys
import json


# Detect ENV type from path
currentpath     = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/flask_app
projectpath     = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere
ENVPATH         = os.path.dirname(projectpath)               # /home/pi/Dev
ENVNAME         = os.path.basename(ENVPATH)                  # Dev

# email server
"""
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'chaudiere.mlv@gmail.com' #os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = '' #os.environ.get('MAIL_PASSWORD')
"""

#detect env from filesystem location (Proc/Dev)
if ENVNAME == 'Dev' :
    # Development configuration
    APP_NAME = 'Chaudiere Dev' 
    PORT = 5008
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    TEMPLATES_AUTO_RELOAD = True
    #APP_BASE_URL = 'http://montlevic.hd.free.fr:' + str(PORT) + '/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(ENVPATH + '/db/', 'app.db'))
    SQLALCHEMY_BINDS = {
        'chaudiere':         'sqlite:///' + os.path.join(ENVPATH + '/db/', 'chaudiere.db'),
        'chaudiere_minute':  'sqlite:///' + os.path.join(ENVPATH + '/db/', 'chaudiere_minute.db'),
        'chaudiere_hour':    'sqlite:///' + os.path.join(ENVPATH + '/db/', 'chaudiere_hour.db')
    } 
    # Users emails
    USERS = ['matthieujouve']
    USERS_EMAILS = list(map(lambda x: x+'@gmail.com', USERS))

elif ENVNAME == 'Prod':
    # Production configuration
    APP_NAME = 'Chaudiere'
    DEBUG=False
    PORT = 5007
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(ENVPATH + '/db/', 'app.db'))
    SQLALCHEMY_BINDS = {
        'chaudiere':         'sqlite:///' + os.path.join(ENVPATH + '/db/', 'chaudiere.db'),
        'chaudiere_minute':  'sqlite:///' + os.path.join(ENVPATH + '/db/', 'chaudiere_minute.db'),
        'chaudiere_hour':    'sqlite:///' + os.path.join(ENVPATH + '/db/', 'chaudiere_hour.db')
    }

    # Users emails are set in secret conf
    
elif ENVNAME == 'flask-dev' :
    # Windows Development configuration
    print 'db path '+os.path.join(ENVPATH + '\db\\', 'chaudiere.db')

    PORT = 5007
    APP_NAME += ' Win Dev'
    APP_BASE_URL = 'http://localhost:' + str(PORT) + '/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(
        os.path.join(ENVPATH + '\db\\', 'chaudiere.db'))

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(ENVPATH + '\db\\', 'app.db'))
    SQLALCHEMY_BINDS = {
        'chaudiere':         'sqlite:///' + os.path.join(ENVPATH + '\db\\', 'chaudiere.db'),
        'chaudiere_minute':  'sqlite:///' + os.path.join(ENVPATH + '\db\\', 'chaudiere_minute.db'),
        'chaudiere_hour':    'sqlite:///' + os.path.join(ENVPATH + '\db\\', 'chaudiere_hour.db')
    }
        
