# -*- coding: utf-8 -*-

import os
import sys

import pathlib
from subprocess import check_output
import time, datetime
import urllib, requests
import json
from datetime import datetime, timedelta
from random import random
import pprint
import copy

from flask import Blueprint, render_template, request, jsonify, make_response, redirect, url_for, flash
from flask_login import login_required
from flask import send_file

from .system_info import *
from .forms import AdminConfigForm
from ..views.auth import auth
from ..models import AdminConfig
# from ..constantes import LOGGER_PATH
from .. import db
from .charts import *

from util import *
import config

admin_blueprint = Blueprint("admin", __name__, url_prefix='/admin')

@admin_blueprint.route('/chart', methods=['GET'])
@login_required
def chart():

    return render_template('admin/chart.html', params =  params)
    
@admin_blueprint.route('/', methods=['GET'])
@login_required
def index():
    """Display System Info"""
    params = {}
    params["network"] = {
        'ip lan eth'    : ip_lan_eth(),
        'ip lan wifi'   : ip_lan_wifi(),
        'hostname'      : hostname()
    }
    params["system"] = {
        'date'          : system_date(),
        'uptime'        : system_uptime(),
        'cpu_temp'      : cpu_temp()
    }
    params["Nexmo (SMS)"] = {
        'Balance'       : nexmo_balance()
    }
    params["disk_space"] = disk_space()
    params["supervisor"] = supervisor_status()
    params["db_size"]    = db_size()
    
    return render_template('admin/admin.html', params =  params)
    
@admin_blueprint.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    admin_config = AdminConfig.query.first()
    if admin_config is None:
        abort(404)
    form = AdminConfigForm(obj=admin_config, csrf_enabled=False)
    if request.method == 'POST': 
        if form.validate():
            # admin_config.temp_chaudiere_failure = form.temp_chaudiere_failure.data
            form.populate_obj(admin_config)
            db.session.commit()
            # flash(u'updated', 'success')
            sys.stdout.write("Update admin config\n")
            return render_template('admin/admin_config.html', form=form, success=True)
        else:
            pass
            # flash(u'Error in form', 'danger')
    return render_template('admin/admin_config.html', form=form)

    
@admin_blueprint.route('/log', defaults={'file': None}, methods=['GET'])
@admin_blueprint.route('/log/<string:file>', methods=['GET'])
@login_required
def log(file):
    """ list all log files in ~/Prod/log/ ending with *.err or *.log
    """
    # LOG_PATH = '/home/pi/Dev/log'
    # log_path = pathlib.Path('LOG_PATH')
    log_path = pathlib.Path(app.config['LOG_PATH'])
    all_files = os.listdir(log_path)
    files = [ file for file in all_files if (file.endswith('.log') or file.endswith('.err')) ]
    content = ''
    if file and (file in files):
        stream = open(log_path / file, 'r')
        content = stream.read()
        stream.close()
        # try:
            # stream = open(log_path / file, 'r+')
        # except PermissionError:
            # if file owned by root, must be chown by pi to be readable
            # check_output("sudo chown pi "+ str(log_path / file), shell=True)
            # stream = open(log_path / file, 'r+')
        # finally:
            # content = stream.read()
            # stream.close()
    
    return render_template('admin/admin_log.html',  content=content,
                                                    active_file=file,
                                                    files=files)

@admin_blueprint.route('/log/download/<string:file>', methods=['GET'])
@login_required
def download_log(file):
    """ Download a log file
    """
    if (file.endswith('.log') or file.endswith('.err')):
        log_path = pathlib.Path(app.config['LOG_PATH'])
        return send_file(str(log_path / file), as_attachment=True)
    
    