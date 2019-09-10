import os

# logger package path used user defined logger in app
APP_PATH        = os.path.abspath(os.path.dirname(__file__))  # /home/pi/Dev/chaudiere/flask_app/app
FLASK_PATH      = os.path.dirname(APP_PATH)                   # /home/pi/Dev/chaudiere/flask_app
PROJECT_PATH    = os.path.dirname(FLASK_PATH)                 # /home/pi/Dev/chaudiere
LOGGER_PATH     = os.path.join(PROJECT_PATH, 'logger')        # /home/pi/Dev/chaudiere/logger
