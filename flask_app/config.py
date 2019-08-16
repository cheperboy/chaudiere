""" App configuration."""
import os, sys
import json
import socket # needed to get ip address


# Detect ENV type from path
FLASKPATH     = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/flask_app
PROJECTPATH     = os.path.dirname(FLASKPATH)               # /home/pi/Dev/chaudiere
ENVPATH         = os.path.dirname(PROJECTPATH)             # /home/pi/Dev
ENVNAME         = os.path.basename(ENVPATH)                # Dev

#Common conf
SQLALCHEMY_TRACK_MODIFICATIONS = False

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'chaudiere.montlevic@gmail.com'
# MAIL_PASSWORD is set in secret congig

#Debug toolbar option
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Detect env from filesystem location (Prod/Dev)
if ENVNAME == 'Dev' :
    os.environ['FLASK_ENV'] = 'development'
    # Development configuration
    ENV = 'development'
    APP_NAME = 'Chaudiere Dev' 
    PORT = 5008
    DEBUG = True
    WTF_CSRF_ENABLED = False
    TEMPLATES_AUTO_RELOAD = True
    # url = socket.gethostbyname(socket.gethostname())
    url = "chaudiere.local"
    URL = 'http://'+ str(url) +':'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(ENVPATH + '/db/', 'app.db'))
    SQLALCHEMY_BINDS = {
        'admin_config': 'sqlite:///' + os.path.join(ENVPATH + '/db/', 'admin_config.db'),
        'users':            'sqlite:///' + os.path.join(ENVPATH + '/db/', 'users.db'),
        'chaudiere':      'sqlite:///' + os.path.join(ENVPATH + '/db/', 'chaudiere.db'),
        'chaudiere_minute':   'sqlite:///' + os.path.join(ENVPATH + '/db/', 'chaudiere_minute.db'),
        'chaudiere_hour':     'sqlite:///' + os.path.join(ENVPATH + '/db/', 'chaudiere_hour.db')
    } 
    # Users emails
    USERS = ['matthieujouve']

elif ENVNAME == 'Prod':
    # Production configuration
    FLASK_ENV='production'
    ENV = 'production'
    APP_NAME = 'Chaudiere'
    DEBUG = False
    PORT = 5007
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(ENVPATH + '/db/', 'app.db'))
    SQLALCHEMY_BINDS = {
        'admin_config': 'sqlite:///' + os.path.join(ENVPATH + '/db/', 'admin_config.db'),
        'users':            'sqlite:///' + os.path.join(ENVPATH + '/db/', 'users.db'),
        'chaudiere':         'sqlite:///' + os.path.join(ENVPATH + '/db/', 'chaudiere.db'),
        'chaudiere_minute':  'sqlite:///' + os.path.join(ENVPATH + '/db/', 'chaudiere_minute.db'),
        'chaudiere_hour':    'sqlite:///' + os.path.join(ENVPATH + '/db/', 'chaudiere_hour.db')
    }

    # Users emails are set in secret conf
    
elif ENVNAME == 'flask-dev' :
    # Windows Development configuration
    ENV: 'development'
    FLASK_ENV='development'
    print ('db path '+os.path.join(ENVPATH + '\db\\', 'chaudiere.db'))

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
        
