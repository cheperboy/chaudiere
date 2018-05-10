# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Blueprint, jsonify, make_response
import json, time
from datetime import datetime, timedelta
from random import random

from app.auth import auth
from app.models import Chaudiere, ChaudiereMinute
from app import cache

import config

webapi = Blueprint("webapi", __name__, url_prefix='/webapi')

"""
return a serie of a database Column with timestamp
return format is [
  [
    1524597668000,  # timestamp
    62.875          # value
  ], 
  ...
]
hours : time from now 
type : temp OR watt
sensor : integer from 0 to N sensor
"""
@webapi.route('/getchaudiere/<int:hours>/<string:db_field>', methods=['GET'])
#@cache.cached(timeout=10)
def getchaudiere(hours, db_field):
    last = Chaudiere.query.order_by(Chaudiere.id.desc()).limit(1)[0]
    ts = last.timestamp - timedelta(hours=hours)
    entries = list()
    for entry in Chaudiere.query\
                     .order_by(Chaudiere.timestamp)\
                     .filter(Chaudiere.timestamp >= ts)\
                     .all():
        entries.append(entry.datatolist(str(db_field))) # e.g. 'temp0'
    return jsonify(entries), 200

@webapi.route('/getchaudierehistory/<int:year>/<int:month>/<int:day>/<int:hour>/<int:hours>/<string:db_field>', methods=['GET'])
def getchaudierehistory(year, month, day, hour, hours, db_field):
    ts_end = datetime(year, month, day, hour, 0)
    ts_begin = ts_end - timedelta(hours=hours)
    entries = list()
    for entry in ChaudiereMinute.query\
                     .order_by(ChaudiereMinute.timestamp)\
                     .filter(ChaudiereMinute.timestamp >= ts_begin)\
                     .filter(ChaudiereMinute.timestamp <= ts_end)\
                     .all():
        entries.append(entry.datatolist(str(db_field))) # e.g. 'temp0'
    return jsonify(entries), 200
    
@webapi.route('/getminute/<int:hours>/<string:type>/<int:sensor>', methods=['GET'])
@webapi.route('/getminute/<int:hours>/<string:type>', methods=['GET']) 
#@cache.cached(timeout=10)
def getminute(hours, type, sensor=''):
    last = ChaudiereMinute.query.order_by(ChaudiereMinute.id.desc()).limit(1)[0]
    ts = last.timestamp - timedelta(hours=hours)
    entries = list()
    for entry in ChaudiereMinute.query\
                     .order_by(ChaudiereMinute.timestamp)\
                     .filter(ChaudiereMinute.timestamp >= ts)\
                     .all():
        entries.append(entry.datatolist(str(type)+str(sensor))) # e.g. 'temp0'
    return jsonify(entries), 200
    
@webapi.route('/live.json')
def live_json():
    # Create a PHP array and echo it as JSON
    data = [time.time() * 1000, random() * 100]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response
