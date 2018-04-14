import os

currentpath = os.path.abspath(os.path.dirname(__file__)) # /home/pi/Development/teleinfo/teleinfoapp
projectpath = os.path.dirname(currentpath)               # /home/pi/Development/teleinfo
envpath = os.path.dirname(projectpath)                   # /home/pi/Development
envname = os.path.basename(envpath)                      # Development
"""
print 'currentpath '+currentpath
print 'projectpath '+projectpath
print 'envpath '+envpath
print 'ENVNAME '+envname
"""
print 'ENVNAME : '+envname

"""Base configuration."""
APP_NAME = "Teleinfo"
SECRET_KEY = os.getenv('SECRET_KEY', default='my_secret')
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False
PORT = 5002


#detect env from filesystem location (Proc/Dev)
if envname == 'Development' :
    """Development configuration."""
    print 'db path '+os.path.join(projectpath + '/db/', 'teleinfo.db')

    APP_NAME += ' Dev'
    APP_BASE_URL = 'http://montlevic.hd.free.fr:' + str(PORT) + '/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(projectpath + '/db/', 'app.db'))
    SQLALCHEMY_BINDS = {
        'teleinfo':         'sqlite:///' + os.path.join(projectpath + '/db/', 'teleinfo.db'),
        'teleinfo_minute':  'sqlite:///' + os.path.join(projectpath + '/db/', 'teleinfo_minute.db'),
        'teleinfo_hour':    'sqlite:///' + os.path.join(projectpath + '/db/', 'teleinfo_hour.db')
    }
    
elif envname == 'Production':
    """Production configuration."""
    APP_BASE_URL = 'http://montlevic.hd.free.fr:' + str(PORT) + '/'
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(projectpath + '/db/', 'app.db'))
    SQLALCHEMY_BINDS = {
        'teleinfo':         'sqlite:///' + os.path.join(projectpath + '/db/', 'teleinfo.db'),
        'teleinfo_minute':  'sqlite:///' + os.path.join(projectpath + '/db/', 'teleinfo_minute.db'),
        'teleinfo_hour':    'sqlite:///' + os.path.join(projectpath + '/db/', 'teleinfo_hour.db')
    }
    WTF_CSRF_ENABLED = True
    
elif envname == 'flask-dev' :
    """Windows Development configuration."""
    print 'db path '+os.path.join(projectpath + '\db\\', 'teleinfo.db')

    APP_NAME += ' Win Dev'
    APP_BASE_URL = 'http://localhost:' + str(PORT) + '/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(
        os.path.join(projectpath + '\db\\', 'teleinfo.db'))

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(projectpath + '\db\\', 'app.db'))
    SQLALCHEMY_BINDS = {
        'teleinfo':         'sqlite:///' + os.path.join(projectpath + '\db\\', 'teleinfo.db'),
        'teleinfo_minute':  'sqlite:///' + os.path.join(projectpath + '\db\\', 'teleinfo_minute.db'),
        'teleinfo_hour':    'sqlite:///' + os.path.join(projectpath + '\db\\', 'teleinfo_hour.db')
    }
    

else:
    """Undefined configuration."""
    APP_NAME += ' /!\\'
    
