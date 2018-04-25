import os

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Dev/chaudiere/chaudiereapp
projectpath = os.path.dirname(currentpath)               # /home/pi/Dev/chaudiere
envpath = os.path.dirname(projectpath)                   # /home/pi/Dev
envname = os.path.basename(envpath)                      # Dev
"""
print 'currentpath '+currentpath
print 'projectpath '+projectpath
print 'envpath '+envpath
print 'ENVNAME '+envname
"""
print 'ENVNAME : '+envname

"""Base configuration."""
APP_NAME = "Chaudiere"
SECRET_KEY = os.getenv('SECRET_KEY', default='my_secret')
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False
PORT = 5007


#detect env from filesystem location (Proc/Dev)
if envname == 'Dev' :
    """Development configuration."""
    APP_NAME += ' Dev' 
    APP_BASE_URL = 'http://192.168.0.70:' + str(PORT) + '/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(projectpath + '/db/', 'app.db'))
    SQLALCHEMY_BINDS = {
        'chaudiere':         'sqlite:///' + os.path.join(projectpath + '/db/', 'chaudiere.db'),
        'chaudiere_minute':  'sqlite:///' + os.path.join(projectpath + '/db/', 'chaudiere_minute.db'),
        'chaudiere_hour':    'sqlite:///' + os.path.join(projectpath + '/db/', 'chaudiere_hour.db')
    }
    
elif envname == 'Prod':
    """Production configuration."""
    APP_BASE_URL = 'http://montlevic.hd.free.fr:' + str(PORT) + '/'
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(projectpath + '/db/', 'app.db'))
    SQLALCHEMY_BINDS = {
        'chaudiere':         'sqlite:///' + os.path.join(projectpath + '/db/', 'chaudiere.db'),
        'chaudiere_minute':  'sqlite:///' + os.path.join(projectpath + '/db/', 'chaudiere_minute.db'),
        'chaudiere_hour':    'sqlite:///' + os.path.join(projectpath + '/db/', 'chaudiere_hour.db')
    }
    WTF_CSRF_ENABLED = True
    
elif envname == 'flask-dev' :
    """Windows Development configuration."""
    print 'db path '+os.path.join(projectpath + '\db\\', 'chaudiere.db')

    APP_NAME += ' Win Dev'
    APP_BASE_URL = 'http://localhost:' + str(PORT) + '/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(
        os.path.join(projectpath + '\db\\', 'chaudiere.db'))

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(projectpath + '\db\\', 'app.db'))
    SQLALCHEMY_BINDS = {
        'chaudiere':         'sqlite:///' + os.path.join(projectpath + '\db\\', 'chaudiere.db'),
        'chaudiere_minute':  'sqlite:///' + os.path.join(projectpath + '\db\\', 'chaudiere_minute.db'),
        'chaudiere_hour':    'sqlite:///' + os.path.join(projectpath + '\db\\', 'chaudiere_hour.db')
    }
    

else:
    """Undefined configuration."""
    APP_NAME += ' /!\\'
    
