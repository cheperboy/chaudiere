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

from flask_datepicker import datepicker

# app import
from app.charts import charts_blueprint
from app.monitor import monitor_blueprint
from app.webapi import webapi

import logging, os
from logging.handlers import RotatingFileHandler

def create_app():
    app = Flask(__name__)

def create_app():
    app = Flask(__name__,\
                static_folder="static/",\
                template_folder="templates/",\
                static_url_path="/static")
    
    # set config
    app.config.from_object('config')

    # set up extensions
    cache.init_app(app)
    db.init_app(app)
    datepicker(app)
    
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

