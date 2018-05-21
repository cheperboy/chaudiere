# -*- coding: utf-8 -*-
from __future__ import absolute_import
import time, datetime, urllib2
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
monitor_blueprint = Blueprint("monitor", __name__, url_prefix='/monitor')

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

def get_entry_temperature(entry):
    return entry.get(TEMP_CHAUDIERE)

def get_entry_dt(entry):
    return entry.dt

"""
list of min value of the given serie sliced in X minutes intervals
"""
def list_of_min_values(all_entries, interval=60):
    min_values = []
    begin = 0
    end   = interval
    out_len = int(len(all_entries)/interval)
    print out_len
    while(begin < len(all_entries)):
        values = [entry.get(TEMP_CHAUDIERE) for entry in all_entries[begin:end] if (entry is not None and\
                                                                                    entry.get(TEMP_CHAUDIERE) is not None)]
        dts = map(get_entry_dt, all_entries[begin:end])
        pprint.pprint(values)
        if len(values) > 0:
            min_values.append(min(values))
        begin += interval
        end   += interval
    return min_values
"""
min value of the given serie
"""
def min_value(all_entries):
    values = [entry.get(TEMP_CHAUDIERE) for entry in all_entries if (entry is not None and\
                                                                                entry.get(TEMP_CHAUDIERE) is not None)]
    return min(values)

@monitor_blueprint.route('/', methods=['GET'])
def monitor():
    dt_end = datetime.now().replace(second=0, microsecond=0)
    dt_begin = dt_end - timedelta(hours=24)
    entries_day = ChaudiereMinute.query\
                         .order_by(ChaudiereMinute.dt)\
                         .filter(ChaudiereMinute.dt >= dt_begin)\
                         .filter(ChaudiereMinute.dt <= dt_end)\
                         .all()

    dt_begin = dt_end - timedelta(days=7)
    entries_week = ChaudiereMinute.query\
                         .order_by(ChaudiereMinute.dt)\
                         .filter(ChaudiereMinute.dt >= dt_begin)\
                         .filter(ChaudiereMinute.dt <= dt_end)\
                         .all()
    dt_begin = dt_end - timedelta(days=14)
    entries_2week = ChaudiereMinute.query\
                         .order_by(ChaudiereMinute.dt)\
                         .filter(ChaudiereMinute.dt >= dt_begin)\
                         .filter(ChaudiereMinute.dt <= dt_end)\
                         .all()
    min_value_of_the_day = min_value(entries_day)
    min_value_of_last_week = min_value(entries_week)
    min_value_of_last_2week = min_value(entries_2week)
    response = make_response('min value of day :'               +str(min_value_of_the_day)+\
                             ' <br>min value of last week :'    +str(min_value_of_last_week)+\
                             ' <br>min value of last 2 weeks :' +str(min_value_of_last_2week)+\
                             ' <br>TEMP_CHAUDIERE_ALERT :'      +str(TEMP_CHAUDIERE_ALERT)+\
                             ' <br>TEMP_CHAUDIERE_FAILURE :'    +str(TEMP_CHAUDIERE_FAILURE))
    return response
    