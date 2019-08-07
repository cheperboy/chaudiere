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
from app.auth import auth
from app.models import Chaudiere, ChaudiereMinute, datetime_to_timestamp
from app.constantes import *
from util import *

import config

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

admin_blueprint = Blueprint("admin", __name__, url_prefix='/admin')


def db_size():
    """
    The command returns:
        EMPTY LINE
        app.db 0
        chaudiere.db 536576
        chaudiere_hour.db 8192
        chaudiere_minute.db 241664        
    This function returns:
        {'app.db': '0 Mo', 'chaudiere.db': '537 Mo', 'chaudiere_hour.db': '8 Mo', 'chaudiere_minute.db': '242 Mo'}
    """
    import subprocess
    cmd = """ls -l /home/pi/Prod/db | awk '{ print $9 " " $5 }' """
    stdout = subprocess.check_output(cmd, shell=True)
    stdout = stdout.decode('utf-8')
    ret = {}
    for line in stdout.splitlines():
        line = line.split( )
        if len(line) > 0:
            size = "{:.0f}".format(int(line[1])/1000)
            size = str(size) + " Mo"
            ret[line[0]] = size
    return (ret)

def system_uptime():
    """
    """
    import subprocess
    cmd = '''uptime -p'''
    stdout = subprocess.check_output(cmd, shell=True)
    stdout = stdout.decode('utf-8')
    return (stdout)

def system_date():
    """
    """
    import subprocess
    cmd = '''date'''
    stdout = subprocess.check_output(cmd, shell=True)
    stdout = stdout.decode('utf-8')
    return (stdout)

def cpu_temp():
    """
    The shell command (vcgencmd measure_temp) returns
    temp=64.5'C
    This function returns
    64.5'C
    """
    import subprocess
    cmd = '''vcgencmd measure_temp'''
    stdout = subprocess.check_output(cmd, shell=True)
    stdout = stdout.decode('utf-8')
    stdout = stdout.split("=")
    return(stdout[1])

def disk_space():
    """
    The shell command (df with options...) returns
    /dev/root          7,0G    3,5G  52%
    This function returns
    {'cpu_temp': '7,0G', 'used': '3,5G', 'used_percent': '52%'}    
    """
    import subprocess
    cmd = '''df -h --output=source,size,used,pcent | grep /dev/root'''
    stdout = subprocess.check_output(cmd, shell=True)
    stdout = stdout.decode('utf-8')
    stdout = stdout.split( )
    ret = {"size" : stdout[1], "used": stdout[2], "used_percent": stdout[3]}
    return (ret)
    
def set_params():
    params = {}
    params["system"] = {
        'date' :          system_date(),
        'uptime' :          system_uptime(),
        'cpu_temp' :   cpu_temp()
    }
    params["disk_space"] = disk_space()
    params["db_size"] = db_size()
    return params

@admin_blueprint.route('/', methods=['GET'])
def index():
    params = set_params()

    return render_template('admin/admin.html', params =  params)
    