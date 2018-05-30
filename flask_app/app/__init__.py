# -*- coding: utf-8 -*-
from __future__ import absolute_import

# ext import
from flask import Flask
from flask_assets import Environment, Bundle

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_caching import Cache
cache = Cache(config={'CACHE_TYPE': 'simple'})

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

from flask_mail import Mail
mail = Mail()

from flask_datepicker import datepicker

# app import
from app.charts import charts_blueprint
from app.monitor import monitor_blueprint
from app.webapi import webapi

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
            "MAIL_PASSWORD" : "mypassword",
            "URL" : "http://myip:",
            "SECRET_KEY" : "mysecret"    
        },
        "Prod" : {
            "USERS" : [ "mj@gmail.com", 
                        "tj@gmail.com", 
                        "ej@gmail.com", 
                        "acj@gmail.com"
                       ]
        },
        "Dev" : {
            "USERS" : ["mj@gmail.com"]
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
        print('IOError loading conf file (file not existing?): ' + file + str(e))
    except ValueError as e:
        print('ValueError loading JSON : ' + secret_conf_com + ' ' + str(e))

    app.config['APP_BASE_URL'] = app.config['URL'] + str(app.config['PORT']) + '/'
    #app.config['USERS_EMAILS'] = list(map(lambda x: x+'@gmail.com', app.config['USERS']))

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
    app.register_blueprint(charts_blueprint)
    app.register_blueprint(webapi)
    app.register_blueprint(monitor_blueprint)
    
    #form csrf
    csrf.init_app(app)

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

    return app

