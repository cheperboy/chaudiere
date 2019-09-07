# -*- coding: utf-8 -*-
"""
.. module:: app
   :synopsis: Main module of the flask application

.. moduleauthor:: cheperboy
"""
from datetime import datetime
# ext import
from flask import Flask
from flask_assets import Environment, Bundle

from flask_debugtoolbar import DebugToolbarExtension

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_caching import Cache
cache = Cache(config={'CACHE_TYPE': 'simple'})

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

from flask_mail import Mail
mail = Mail()

from flask_datepicker import datepicker

from flask_login import LoginManager 

# app import
from app.admin import admin_blueprint
from app.views.auth import auth
from app.views.charts.views import charts_blueprint
from app.views.monitor import monitor_blueprint
from app.views.webapi import webapi

import logging, os, json
from logging.handlers import RotatingFileHandler

import config, sys

def set_config(app):
    """
    loads config then override from secret file
    secret file directory must be : /home/pi/CONFIG_CHAUDIERE
    secret file name must be : chaudiere_secret_config_{common|Dev|Prod}.py
    first overrinde with common secret conf file
    then override with specific env secret conf file
    example of chaudiere_secret_config.py
    {
        "Common" : {
            "MAIL_PASSWORD" : "xxx",
            "SECRET_KEY" : "xxx",
            "NEXMO_API_KEY" : "xxx",
            "NEXMO_API_SECRET" : "xxx"
        },
        "Prod" : {
            "URL" : "http://xxx.hd.free.fr:",
            "USERS_EMAILS" :  ["xx@gmail.com", 
                               "xx@gmail.com", 
                               "xx@gmail.com", 
                               "xx@gmail.com"
                              ],
            "USERS_PHONES" :  ["336xxxxxxxx", 
                               "336xxxxxxxx", 
                               "336xxxxxxxx", 
                               "336xxxxxxxx"
                              ]
        },
        "Dev" : {
            "USERS_EMAILS" :  ["xx@gmail.com"],
            "USERS_PHONES" :  ["336xxxxxxxx"]
        }
    }
    """
    # set config from config.py
    app.config.from_object('config')

    # override config from secret conf files
    pi_home                 = os.path.dirname(app.config['ENVPATH'])    # /home/pi
    secret_conf_dir         = os.path.join(pi_home, 'CONFIG_CHAUDIERE') # /home/pi/CONFIG_CHAUDIERE
    secret_conf_com_file    = 'chaudiere_secret_config.py'
    secret_conf_com         = secret_conf_dir+'/'+secret_conf_com_file
    try:
        with open(secret_conf_com) as f:
            json_config = json.load(f)
        for conf in ['Common', app.config['ENVNAME']]:
            app.config.update(json_config[conf])
    except IOError as e:
        print('IOError loading conf file (file not existing?): ' + secret_conf_com + str(e))
    except ValueError as e:
        print('ValueError loading JSON : ' + secret_conf_com + ' ' + str(e))

    #app.config['USERS_EMAILS'] = list(map(lambda x: x+'@gmail.com', app.config['USERS']))    
    # app.logger.error('test error')   # <-- This works !!!     

def init_db_admin_config():
    """
    This function is supposed to be call when the app is instanciated by create_app()
    AdminConfig is the database to store constants editable by admin user (eg: temp_chaudiere_failure)
    This database must be filled with one row contaning default values at stat-up if it doesn't exists yet.
    Algo:
    If database admin_config contains no entry, then create one and set temp_chaudiere_failure to the default value (see constantes.py TEMP_CHAUDIERE_FAILURE_DEFAULT)
    """
    from app.constantes import TEMP_CHAUDIERE_FAILURE_DEFAULT, \
                                CHAUDIERE_DB_ROTATE_HOURS_DEFAULT, \
                                CHAUDIERE_MINUTE_DB_ROTATE_DAYS_DEFAULT, \
                                ALERTS_ENABLE_DEFAULT
    from app.models.admin_config import AdminConfig
    
    db.create_all('admin_config')
    
    if AdminConfig.first(AdminConfig) == None:
        new_config = AdminConfig(
            temp_chaudiere_failure          = TEMP_CHAUDIERE_FAILURE_DEFAULT,
            chaudiere_db_rotate_hours       = CHAUDIERE_DB_ROTATE_HOURS_DEFAULT,
            chaudiere_minute_db_rotate_days = CHAUDIERE_MINUTE_DB_ROTATE_DAYS_DEFAULT,
            alerts_enable                   = ALERTS_ENABLE_DEFAULT,
            comment = ''
        )
        
        db.session.add(new_config)
        db.session.commit()
        print("\n * NEW AdminConfig")
        print(AdminConfig.first(AdminConfig))
        
def create_app():
    app = Flask(__name__,\
                static_folder="static/",\
                template_folder="templates/",\
                static_url_path="/static")

    set_config(app)
    
    # set up extensions
    cache.init_app(app)
    db.init_app(app)
    datepicker(app)
    mail.init_app(app)
    
    # blueprints
    app.register_blueprint(auth)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(charts_blueprint)
    app.register_blueprint(webapi)
    app.register_blueprint(monitor_blueprint)
    
    # form csrf
    csrf.init_app(app)

    # login_manager
    login_manager = LoginManager()
    login_manager.login_view = 'charts.now'
    login_manager.init_app(app)
    
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    # Scss
    assets = Environment(app)
    assets.versions = 'timestamp'
    assets.url_expire = True
    assets.manifest = 'file:/tmp/manifest.to-be-deployed'  # explict filename
    assets.cache = False
    assets.auto_build = True

    assets.url = app.static_url_path
    scss = Bundle('scss/__main__.scss', filters='pyscss', output='css/main.css',  depends=['scss/*.scss'])
    assets.register('scss_all', scss)

    assets.debug = False
    app.config['ASSETS_DEBUG'] = False
    
    with app.app_context():
        init_db_admin_config()
        
    toolbar = DebugToolbarExtension(app)
    return (app)

