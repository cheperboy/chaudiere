""" App configuration."""
import os

# Detect ENV type from path
currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/chaudiereapp
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                   # /home/pi/Dev
ENVNAME = os.path.basename(envpath)                      # Dev
# print 'ENVNAME : '+ENVNAME

# Base configuration
APP_NAME = "Chaudiere"
SECRET_KEY = os.getenv('SECRET_KEY', default='lkdsjfiozefkdv23168761JGDZYGU')
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'chaudiere.montlevic@gmail.com' #os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = 'Montlevic36' #os.environ.get('MAIL_PASSWORD')

#detect env from filesystem location (Proc/Dev)
if ENVNAME == 'Dev' :
    # Development configuration
    DEBUG=False
    TEMPLATES_AUTO_RELOAD = True
    APP_NAME += ' Dev' 
    PORT = 5008
    APP_BASE_URL = 'http://montlevic.hd.free.fr:' + str(PORT) + '/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(envpath + '/db/', 'app.db'))
    SQLALCHEMY_BINDS = {
        'chaudiere':         'sqlite:///' + os.path.join(envpath + '/db/', 'chaudiere.db'),
        'chaudiere_minute':  'sqlite:///' + os.path.join(envpath + '/db/', 'chaudiere_minute.db'),
        'chaudiere_hour':    'sqlite:///' + os.path.join(envpath + '/db/', 'chaudiere_hour.db')
    }
    # Users emails
    USERS = ['matthieujouve']
    USERS_EMAILS = list(map(lambda x: x+'@gmail.com', USERS))

    
elif ENVNAME == 'Prod':
    # Production configuration
    DEBUG=False
    PORT = 5007
    APP_BASE_URL = 'http://montlevic.hd.free.fr:' + str(PORT) + '/'
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(envpath + '/db/', 'app.db'))
    SQLALCHEMY_BINDS = {
        'chaudiere':         'sqlite:///' + os.path.join(envpath + '/db/', 'chaudiere.db'),
        'chaudiere_minute':  'sqlite:///' + os.path.join(envpath + '/db/', 'chaudiere_minute.db'),
        'chaudiere_hour':    'sqlite:///' + os.path.join(envpath + '/db/', 'chaudiere_hour.db')
    }
    WTF_CSRF_ENABLED = True

    # Users emails
    USERS = ['matthieujouve', 'thierryjouve', 'elisabethjouve', 'acjouve']
    USERS_EMAILS = list(map(lambda x: x+'@gmail.com', USERS))
    
elif ENVNAME == 'flask-dev' :
    # Windows Development configuration
    print 'db path '+os.path.join(envpath + '\db\\', 'chaudiere.db')

    PORT = 5007
    APP_NAME += ' Win Dev'
    APP_BASE_URL = 'http://localhost:' + str(PORT) + '/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(
        os.path.join(envpath + '\db\\', 'chaudiere.db'))

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(envpath + '\db\\', 'app.db'))
    SQLALCHEMY_BINDS = {
        'chaudiere':         'sqlite:///' + os.path.join(envpath + '\db\\', 'chaudiere.db'),
        'chaudiere_minute':  'sqlite:///' + os.path.join(envpath + '\db\\', 'chaudiere_minute.db'),
        'chaudiere_hour':    'sqlite:///' + os.path.join(envpath + '\db\\', 'chaudiere_hour.db')
    }
    

else:
    """Undefined configuration."""
    APP_NAME += ' /!\\'
    
