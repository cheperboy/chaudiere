# -*- coding: utf-8 -*-
from __future__ import absolute_import
import time, datetime, urllib2
import urllib
import json
from datetime import datetime, timedelta
from random import random

from flask import Blueprint, render_template, request, jsonify, make_response
from app.auth import auth
import config
charts_blueprint = Blueprint("charts", __name__, url_prefix='/charts')
static_conf_temp = {
        "chart": { 
            "renderTo": 'mystaticchart-container',
            "defaultSeriesType": 'spline',
        },
        'rangeSelector' : {
            'inputEnabled': 'false',
            'selected' : 2,
            'buttons': [
                {
                    'type': 'minute',
                    'count': 15,
                    'text': '15m'
                },{
                    'type': 'minute',
                    'count': 60,
                    'text': '1h'
                },{
                    'type': 'minute',
                    'count': 120,
                    'text': '2h'
                },{
                    'type': 'day',
                    'count': 1,
                    'text': '24h'
                },{
                    'type': 'day',
                    'count': 7,
                    'text': '1w'
                },{
                    'type': 'all',
                    'text': 'All'
                }]
        },

        'title': {
            'text': 'Température'
        },

        'yAxis': [{
            'labels': {
                'align': 'right',
                'x': -3
            },
            'title': {
                'text': 'Degre'
            },
            'height': '60%',
            'lineWidth': 1,
        }],
        'tooltip': {
            'shared': True,
            'crosshairs': True
        },
        "series": [
            {
                "name": 'temp chaudière',
                "data": [],
                "sensor_type": 'temp',
                "sensor_id": '0'
            },
            {
                "name": 'temp fumée',
                "data": [],
                "sensor_type": 'temp',
                "sensor_id": '1',
                "linkedTo": '1'
            },
            {
                "name": 'temp retour',
                "data": [],
                "sensor_type": 'temp',
                "sensor_id": '2',
                "linkedTo": 'temp chaudière'
            }
        ]
}

static_conf_watt = {
        "chart": { 
            "renderTo": 'mystaticchart-container',
            "defaultSeriesType": 'spline',
        },
        'rangeSelector' : {
            'inputEnabled': 'false',
            'selected' : 2,
            'buttons': [
                {
                    'type': 'minute',
                    'count': 15,
                    'text': '15m'
                },{
                    'type': 'minute',
                    'count': 60,
                    'text': '1h'
                },{
                    'type': 'minute',
                    'count': 120,
                    'text': '2h'
                },{
                    'type': 'day',
                    'count': 1,
                    'text': '24h'
                },{
                    'type': 'day',
                    'count': 7,
                    'text': '1w'
                },{
                    'type': 'all',
                    'text': 'All'
                }]
        },

        'title': {
            'text': 'Puissance'
        },

        'yAxis': [{
            'labels': {
                'align': 'right',
                'x': -3
            },
            'title': {
                'text': 'Watt'
            },
            'height': '60%',
            'lineWidth': 1,
        }],
        'tooltip': {
            'shared': True,
            'crosshairs': True
        },
        "series": [
            {
                "name": 'watt 0',
                "data": [],
                "sensor_type": 'watt',
                "sensor_id": '0'
            },
            {
                "name": 'watt 1',
                "data": [],
                "sensor_type": 'watt',
                "sensor_id": '1'
            },
            {
                "name": 'watt 2',
                "data": [],
                "sensor_type": 'watt',
                "sensor_id": '2'
            },
            {
                "name": 'watt 3',
                "data": [],
                "sensor_type": 'watt',
                "sensor_id": '3'
            }
        ]
}
live_conf = {
        "chart": { 
            "renderTo": 'data-container',
            "defaultSeriesType": 'spline',
            "events": {
                "load": 'requestLastWatt0'
            }
        },
        "title": {
            "text": 'Live random data'
        },
        "xAxis": {
            "type": 'datetime',
        },
        "series": [{
			"name": 'Random data',
			"data": []
        }]
}
opt_conf = {
        "chart": { 
            "renderTo": 'mystaticchart-container',
            "defaultSeriesType": 'spline'
        },
        "title": {
            "text": 'Live random data'
        },
        "xAxis": {
            "type": 'datetime',
        },
        "series": [{
			"name": 'Random data',
			"data": []
        }]
}

baseURL = {'value' : config.APP_BASE_URL}

@charts_blueprint.route('/allchart')
def allchart():
    return render_template('index.html', baseURL=baseURL, mylivechart=True, mystaticchart=True)

@charts_blueprint.route('/mylivechart')
def mylivechart():
    return render_template('index.html', baseURL=baseURL, mylivechart=True)

@charts_blueprint.route('/')
@charts_blueprint.route('/mystaticchart')
def mystaticchart():
    return render_template('index.html', baseURL=baseURL, staticcharttemp=True, staticchartwatt=True)

@charts_blueprint.route('/livedatas')
def livedatas():
    # Create a PHP array and echo it as JSON
    data = [time.time() * 1000, random() * 100, random() * 10]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response
    
@charts_blueprint.route('/liveconf', methods=['GET'])
def liveconf():
    response = make_response(json.dumps(live_conf))
    response.content_type = 'application/json'
    return response

"""
data : temp OR watt
"""
@charts_blueprint.route('/staticconf/<string:type>', methods=['GET'])
def staticconf(type):
    if type == 'temp':
        response = make_response(json.dumps(static_conf_temp))
    elif type == 'watt':
        response = make_response(json.dumps(static_conf_watt))
    response.content_type = 'application/json'
    return response
