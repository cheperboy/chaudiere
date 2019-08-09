# -*- coding: utf-8 -*-
from __future__ import absolute_import
import time, datetime
import urllib, requests
import json
from datetime import datetime, timedelta
from random import random
import pprint
import copy

from flask import Blueprint, render_template, request, jsonify, make_response, redirect, url_for
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from app.admin.system_info import *
from app.controllers.auth import auth
from app.models import AdminConfig
from app.constantes import *
from util import *
import config

admin_blueprint = Blueprint("admin", __name__, url_prefix='/admin')

@admin_blueprint.route('/', methods=['GET'])
@login_required
def index():
    params = {}
    params["chaudiere"] = {
        'temp failure'            : AdminConfig.get(AdminConfig, 'temp_chaudiere_failure')
    }
    params["network"] = {
        'ip'            : local_ip(),
        'hostname' : hostname()
    }
    params["system"] = {
        'date' :          system_date(),
        'uptime' :          system_uptime(),
        'cpu_temp' :   cpu_temp()
    }
    params["Nexmo (SMS)"] = {
        'Balance' :   nexmo_balance()
    }
    params["disk_space"] = disk_space()
    params["db_size"] = db_size()

    return render_template('admin/admin.html', params =  params)
    
@admin_blueprint.route('/config', methods=['GET'])
@login_required
def config():
    params = {}
    params["chaudiere"] = {
        'ip'            : local_ip(),
        'hostname' : hostname()
    }
    params["network"] = {
        'ip'            : local_ip(),
        'hostname' : hostname()
    }
    params["system"] = {
        'date' :          system_date(),
        'uptime' :          system_uptime(),
        'cpu_temp' :   cpu_temp()
    }
    params["Nexmo (SMS)"] = {
        'Balance' :   nexmo_balance()
    }
    params["disk_space"] = disk_space()
    params["db_size"] = db_size()

    return render_template('admin/admin.html', params =  params)
    