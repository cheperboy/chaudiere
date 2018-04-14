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
static_conf = {
        "chart": { 
            "renderTo": 'mystaticchart-container',
            "defaultSeriesType": 'spline',
        },
        'rangeSelector' : {
            'inputEnabled': 'false',
            'selected' : 4,
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
            'text': 'Conso EDF'
        },

        'yAxis': [{
            'labels': {
                'align': 'right',
                'x': -3
            },
            'title': {
                'text': 'Puissance'
            },
            'height': '60%',
            'lineWidth': 1,
        }],
        'tooltip': {
            'shared': True,
            'crosshairs': True
        },
        "series": [{
			"name": 'Random data',
			"data": []
        }]
}
live_conf = {
        "chart": { 
            "renderTo": 'data-container',
            "defaultSeriesType": 'spline',
            "events": {
                "load": 'requestLastPapp'
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

@charts_blueprint.route('/')
@charts_blueprint.route('/allchart')
def allchart():
    return render_template('index.html', baseURL=baseURL, mylivechart=True, mystaticchart=True)

@charts_blueprint.route('/mylivechart')
def mylivechart():
    return render_template('index.html', baseURL=baseURL, mylivechart=True)

@charts_blueprint.route('/mystaticchart')
def mystaticchart():
    return render_template('index.html', baseURL=baseURL, mystaticchart=True)

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

@charts_blueprint.route('/staticconf', methods=['GET'])
def staticconf():
    response = make_response(json.dumps(static_conf))
    response.content_type = 'application/json'
    return response
