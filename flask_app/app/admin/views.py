# -*- coding: utf-8 -*-
import time, datetime
import urllib, requests
import json
from datetime import datetime, timedelta
from random import random
import pprint
import copy

from flask import Blueprint, render_template, request, jsonify, make_response, redirect, url_for, flash
from flask_login import login_required

from .system_info import *
from .forms import AdminConfigForm
from ..views.auth import auth
from ..models import AdminConfig
from ..constantes import *
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
    
@admin_blueprint.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    admin_config = AdminConfig.query.first()
    if admin_config is None:
        abort(404)
    form = AdminConfigForm(obj=admin_config)
    if request.method == 'POST': 
        if form.validate():
            # admin_config.temp_chaudiere_failure = form.temp_chaudiere_failure.data
            form.populate_obj(admin_config)
            db.session.commit()
            print(form.errors)
            # flash(u'updated', 'success')
            return render_template('admin/admin_config.html', form=form, success=True)
        else:
            pass
            # flash(u'Error in form', 'danger')
    return render_template('admin/admin_config.html', form=form)
    