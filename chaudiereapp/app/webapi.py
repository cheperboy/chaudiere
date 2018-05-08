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


@webapi.route('/conso_by_date/<int:year>/<int:month>/<int:day>', methods=['GET'])
def conso_by_date(year, month, day):
    entries = list()
#    ts = datetime.now() - timedelta(hours=25)
#                     .filter(Chaudiere.timestamp >= ts)\
    for entry in Chaudiere.query\
                     .order_by(Chaudiere.timestamp)\
                     .limit(1000)\
                     .all():
        entries.append(entry.watt0tolist())
    return jsonify(entries), 200


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
#@webapi.route('/getchaudiere', defaults={'hours': 1,'type': 0,'sensor': 0}, methods=['GET'])
@webapi.route('/getchaudiere/<int:hours>/<string:type>/<int:sensor>', methods=['GET'])
#@cache.cached(timeout=10)
def getchaudiere(hours, type, sensor):
    last = Chaudiere.query.order_by(Chaudiere.id.desc()).limit(1)[0]
    ts = last.timestamp - timedelta(hours=hours)
    entries = list()
    for entry in Chaudiere.query\
                     .order_by(Chaudiere.timestamp)\
                     .filter(Chaudiere.timestamp >= ts)\
                     .all():
        entries.append(entry.datatolist(str(type)+str(sensor))) # e.g. 'temp0'
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
    
@webapi.route('/getlastentries', defaults={'limit': 1}, methods=['GET'])
@webapi.route('/getlastentries/<int:limit>', methods=['GET'])
def getlastentries(limit):
    entries = list()
    for entry in Chaudiere.query\
                     .order_by(Chaudiere.id.desc())\
                     .limit(limit):
        entries.append(entry.tolist())    
    return jsonify(entries), 200

@webapi.route('/fakedataall', methods=['GET'])
def fakedataall():
    entries = Chaudiere.alltolist(Chaudiere)
    last = Chaudiere.query.order_by(Chaudiere.id.desc()).limit(1)
    
    ts = datetime.now() - timedelta(minutes=len(entries))
    for entry in entries:
        ts = ts + timedelta(minutes=1)
        entry[0] = time.mktime(ts.timetuple())*5000
    return jsonify(entries), 200

@webapi.route('/live.json')
def live_json():
    # Create a PHP array and echo it as JSON
    data = [time.time() * 1000, random() * 100]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response
