# -*- coding: utf-8 -*-
from __future__ import absolute_import
import time, datetime, urllib2
import urllib, requests
import json
from datetime import datetime, timedelta
from random import random
import util

from flask import Blueprint, render_template, request, jsonify, make_response, redirect, url_for
from app.auth import auth
from app.models import Chaudiere, Inputs

import config
charts_blueprint = Blueprint("charts", __name__, url_prefix='/charts')

static_conf_raw = {
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
                    'type': 'hour',
                    'count': 1,
                    'text': '1h'
                },{
                    'type': 'hour',
                    'count': 2,
                    'text': '2h'
                },{
                    'type': 'hour',
                    'count': 4,
                    'text': '4h'
                },{
                    'type': 'hour',
                    'count': 6,
                    'text': '6h'
                },{
                    'type': 'all',
                    'text': 'All'
                }]
        },

        'title': {
            'text': 'Chaudière'
        },

        'yAxis': [
            {
                'labels': {'align': 'right','x': -3},
                'title': {'text': 'Température'},
                'softMin': 55,
                'softMax': 70,
                'top': str((100/4)*0+3*0)+'%',
                'height': '25%',
                'lineWidth': 1,
            },
            {
                'labels': {'align': 'right','x': -3},
                'title': {'text': 'Vent'},
                'softMin': 0,
                'softMax': 20,
                'top': str((100/4)*1+3*1)+'%',
                'height': '25%',
                'offset': 0,
                'lineWidth': 1,
            },
            {
                'labels': {'align': 'right','x': -3},
                'title': {'text': 'Alimentation'},
                'softMin': 0,
                'softMax': 30,
                'top': str((100/4)*2+3*2)+'%',
                'height': '25%',
                'offset': 0,
                'lineWidth': 1,
            },
            {
                'labels': {'align': 'right','x': -3},
                'title': {'text': 'Allumage'},
                'softMin': 0,
                'softMax': 100,
                'top': str((100/4)*3+3*3)+'%',
                'height': '12%',
                'offset': 0,
                'lineWidth': 1,
            }
        ],
        'tooltip': {
            'shared': True,
            'split': False,
            'crosshairs': True
        },
        "series": [
            {
                "name": Inputs['temp_chaudiere']['name'],
                "db": Inputs['temp_chaudiere']['db'],
                "data": [],
                "yAxis": 0,
                "tooltip": {"valueDecimals": 1}
            }, 
            {
                "name": Inputs['temp_fumee']['name'],
                "db": Inputs['temp_fumee']['db'],
                "data": [],
                "yAxis": 0,
                "tooltip": {"valueDecimals": 1}
            },
            {
                "name": Inputs['vent_primaire']['name'],
                "db": Inputs['vent_primaire']['db'],
                "data": [],
                "yAxis": 1,
                "tooltip": {"valueDecimals": 0}
            },
            {
                "name": Inputs['alimentation']['name'],
                "db": Inputs['alimentation']['db'],
                "data": [],
                "yAxis": 2,
                "tooltip": {"valueDecimals": 0}
            },
            {
                "name": Inputs['allumage']['name'],
                "db": Inputs['allumage']['db'],
                "data": [],
                "yAxis": 3,
                "tooltip": {"valueDecimals": 0}
            }
        ]
}
static_conf_minute = {
        "chart": {
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
                    'type': 'hour',
                    'count': 1,
                    'text': '1h'
                },{
                    'type': 'hour',
                    'count': 2,
                    'text': '2h'
                },{
                    'type': 'hour',
                    'count': 4,
                    'text': '4h'
                },{
                    'type': 'hour',
                    'count': 6,
                    'text': '6h'
                },{
                    'type': 'all',
                    'text': 'All'
                }]
        },

        'title': {
            'text': 'Chaudière'
        },

        'yAxis': [
        {
            'labels': {'align': 'right','x': -3},
            'title': {'text': 'Température'},
            'softMin': 55,
            'softMax': 70,
            'top': str((100/4)*0+3*0)+'%',
            'height': '25%',
            'lineWidth': 1,
        },
        {
            'labels': {'align': 'right','x': -3},
            'title': {'text': 'Vent'},
            'softMin': 0,
            'softMax': 20,
            'top': str((100/4)*1+3*1)+'%',
            'height': '25%',
            'offset': 0,
            'lineWidth': 1,
        },
        {
            'labels': {'align': 'right','x': -3},
            'title': {'text': 'Alimentation'},
            'softMin': 0,
            'softMax': 30,
            'top': str((100/4)*2+3*2)+'%',
            'height': '25%',
            'offset': 0,
            'lineWidth': 1,
        },
        {
            'labels': {'align': 'right','x': -3},
            'title': {'text': 'Allumage'},
            'softMin': 0,
            'softMax': 15,
            'top': str((100/4)*3+3*3)+'%',
            'height': '12%',
            'offset': 0,
            'lineWidth': 1,
        },
        ],
        'tooltip': {
            'shared': True,
            'split': False,
            'crosshairs': True
        },
        "series": [
            {
                "name": Inputs['phase']['name'],
                "db": Inputs['phase']['db'],
                "data": [],
                "yAxis": 0,
                "tooltip": {"valueDecimals": 0}
            }, 
            {
                "name": Inputs['temp_chaudiere']['name'],
                "db": Inputs['temp_chaudiere']['db'],
                "data": [],
                "yAxis": 0,
                "tooltip": {"valueDecimals": 1}
            }, 
            {
                "name": Inputs['temp_fumee']['name'],
                "db": Inputs['temp_fumee']['db'],
                "data": [],
                "yAxis": 0,
                "tooltip": {"valueDecimals": 1}
            },
            {
                "name": Inputs['vent_primaire']['name'],
                "db": Inputs['vent_primaire']['db'],
                "data": [],
                "yAxis": 1,
                "tooltip": {"valueDecimals": 0}
            },
            {
                "name": Inputs['alimentation']['name'],
                "db": Inputs['alimentation']['db'],
                "data": [],
                "yAxis": 2,
                "tooltip": {"valueDecimals": 0}
            },
            {
                "name": Inputs['allumage']['name'],
                "db": Inputs['allumage']['db'],
                "data": [],
                "yAxis": 3,
                "tooltip": {"valueDecimals": 0}
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

"""
hour_length param is not used in view but parsed by javascript to request datas
"""
@charts_blueprint.route('/raw', defaults={'hour_length': 1}, methods=['GET'])
@charts_blueprint.route('/raw/<int:hour_length>', methods=['GET'])
def raw(hour_length):
    lastRecorddate = Chaudiere.last(Chaudiere).timestamp
    debugData = None
    return render_template('index.html', 
                            baseURL=baseURL, 
                            staticchartraw=True, 
                            staticchartminute=True, 
                            staticchartraw_conf = False,
                            lastRecordAgo=util.pretty_date(lastRecorddate),
                            debugData=debugData)


"""
params for date, hours : length
"""
@charts_blueprint.route('/history/<string:year>/<string:month>/<string:day>/<string:hour>/<string:hours>', methods=['GET'])
def history(year, month, day, hour, hours):
    date = year+'/'+month+'/'+day+'/'+hour
    return render_template('index.html', 
                            baseURL=baseURL, 
                            staticchartraw=True,
                            history_date = date,
                            history_hours = hours,
                            staticchartminute=False)


 
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
    if type == 'raw':
        response = make_response(json.dumps(static_conf_raw))
    elif type == 'minute':
        response = make_response(json.dumps(static_conf_minute))
    response.content_type = 'application/json'
    return response
