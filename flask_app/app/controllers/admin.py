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

from app.controllers.auth import auth
from app.models import Chaudiere, ChaudiereMinute, datetime_to_timestamp
from app.constantes import *
from app.helpers.system_info import *
from util import *
import config

admin_blueprint = Blueprint("admin", __name__, url_prefix='/admin')

def set_params():
    params = {}
    params["network"] = {
        'ip'            : local_ip(),
        'hostname' : hostname()
    }
    params["system"] = {
        'date' :          system_date(),
        'uptime' :          system_uptime(),
        'cpu_temp' :   cpu_temp()
    }
    params["disk_space"] = disk_space()
    params["db_size"] = db_size()
    return params

@admin_blueprint.route('/', methods=['GET'])
@login_required
def index():
    params = set_params()

    return render_template('admin/admin.html', params =  params)
    