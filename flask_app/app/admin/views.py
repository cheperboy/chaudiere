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

from util import *
import config

admin_blueprint = Blueprint("admin", __name__, url_prefix='/admin')

@admin_blueprint.route('/', methods=['GET'])
@login_required
def index():
    """Display System Info"""
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
    
@admin_blueprint.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    admin_config = AdminConfig.query.first()
    if admin_config is None:
        abort(404)
    form_temp_chaudiere_failure     = AdminConfigForm(obj=admin_config)
    form_chaudiere_db_rotate_days   = AdminConfigForm(obj=admin_config)
    if request.method == 'POST': 
        # Manage temp_chaudiere_failure
        if (admin_config.temp_chaudiere_failure != form_temp_chaudiere_failure.temp_chaudiere_failure.data):
            if form_temp_chaudiere_failure.validate():
                print ("form_temp_chaudiere_failure IS VALID")
                admin_config.temp_chaudiere_failure = form_temp_chaudiere_failure.temp_chaudiere_failure.data
                db.session.commit()
                print ("form_temp_chaudiere_failure updated to " + str(form_temp_chaudiere_failure.temp_chaudiere_failure.data))
                setattr(form_temp_chaudiere_failure, name, StringField(name.title()))
                form_temp_chaudiere_failure[temp_chaudiere_failure_success = True
                return render_template('admin/admin_config.html', 
                                        form_temp_chaudiere_failure=form_temp_chaudiere_failure, 
                                        form_chaudiere_db_rotate_days=form_chaudiere_db_rotate_days, 
                                        temp_chaudiere_failure_updated=True)
            else:
                return render_template('admin/admin_config.html', 
                                        form_temp_chaudiere_failure=form_temp_chaudiere_failure,
                                        form_chaudiere_db_rotate_days=form_chaudiere_db_rotate_days)
        
        # Manage chaudiere_db_rotate_days
        if (admin_config.chaudiere_db_rotate_days != form_chaudiere_db_rotate_days.chaudiere_db_rotate_days.data):
            if form_chaudiere_db_rotate_days.validate():
                admin_config.chaudiere_db_rotate_days = form_chaudiere_db_rotate_days.chaudiere_db_rotate_days.data
                db.session.commit()
                return render_template('admin/admin_config.html', 
                                        form_temp_chaudiere_failure=form_temp_chaudiere_failure, 
                                        form_chaudiere_db_rotate_days=form_chaudiere_db_rotate_days, 
                                        chaudiere_db_rotate_days_updated=True)
            else:
                return render_template('admin/admin_config.html', 
                                        form_temp_chaudiere_failure=form_temp_chaudiere_failure, 
                                        form_chaudiere_db_rotate_days=form_chaudiere_db_rotate_days)
    return render_template('admin/admin_config.html', 
                            form_temp_chaudiere_failure=form_temp_chaudiere_failure, 
                            form_chaudiere_db_rotate_days=form_chaudiere_db_rotate_days)

def config_save():
    admin_config = AdminConfig.query.first()
    if admin_config is None:
        abort(404)
    form = AdminConfigForm(obj=admin_config)
    if request.method == 'POST': 
        if form.validate():
            print (form.temp_chaudiere_failure)
            admin_config.temp_chaudiere_failure = form.temp_chaudiere_failure.data
            db.session.commit()
            print(form.errors)
            # flash(u'updated', 'success')
            return render_template('admin/admin_config.html', form=form, temp_chaudiere_failure_updated=True)
        else:
            pass
            # flash(u'Error in form', 'danger')
    return render_template('admin/admin_config.html', form=form)
    