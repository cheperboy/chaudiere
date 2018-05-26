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
from flask import current_app as app
from app.auth import auth
from app.models import Chaudiere, ChaudiereMinute, datetime_to_timestamp
from app.constantes import *
from util import *

charts_blueprint = Blueprint("charts", __name__, url_prefix='/charts')

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class HistoryForm(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])
    submit = SubmitField('Go')


static_conf_raw = {
    "chart": {"defaultSeriesType": 'spline'},
    "credits": {"enabled": False},
    "exporting": {"filename": 'chaudiere'},
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
            "name": InputName[TEMP_CHAUDIERE],
            "db": InputDb[TEMP_CHAUDIERE],
            "data": [],
            "yAxis": 0,
            "tooltip": {"valueDecimals": 1}
        }, 
        {
            "name": InputName[TEMP_FUMEE],
            "db": InputDb[TEMP_FUMEE],
            "data": [],
            "yAxis": 0,
            "tooltip": {"valueDecimals": 1}
        },
        {
            "name": InputName[VENT_PRIMAIRE],
            "db": InputDb[VENT_PRIMAIRE],
            "data": [],
            "yAxis": 1,
            "tooltip": {"valueDecimals": 0}
        },
        {
            "name": InputName[ALIMENTATION],
            "db": InputDb[ALIMENTATION],
            "data": [],
            "yAxis": 2,
            "tooltip": {"valueDecimals": 0}
        },
        {
            "name": InputName[ALLUMAGE],
            "db": InputDb[ALLUMAGE],
            "data": [],
            "yAxis": 3,
            "tooltip": {"valueDecimals": 0}
        }
    ]
}
static_conf_minute_full = {
    "chart": {"defaultSeriesType": 'spline'},
    "credits": {"enabled": False},
    "exporting": {"filename": 'chaudiere'},       
    'rangeSelector' : {
        'inputEnabled': 'false',
        'selected' : 5,
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
            }
        ]
    },
    'title': {'text': 'Chaudière'},

    'xAxis': {
            'plotBands': None
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
            "name": InputName[TEMP_CHAUDIERE],
            "db": InputDb[TEMP_CHAUDIERE],
            "data": [],
            "yAxis": 0,
            "tooltip": {"valueDecimals": 1}
        }, 
        {
            "name": InputName[TEMP_FUMEE],
            "db": InputDb[TEMP_FUMEE],
            "data": [],
            "yAxis": 0,
            "tooltip": {"valueDecimals": 1}
        },
        {
            "name": InputName[VENT_PRIMAIRE],
            "db": InputDb[VENT_PRIMAIRE],
            "data": [],
            "yAxis": 1,
            "tooltip": {"valueDecimals": 0}
        },
        {
            "name": InputName[ALIMENTATION],
            "db": InputDb[ALIMENTATION],
            "data": [],
            "yAxis": 2,
            "tooltip": {"valueDecimals": 0}
        },
        {
            "name": InputName[ALLUMAGE],
            "db": InputDb[ALLUMAGE],
            "data": [],
            "yAxis": 3,
            "tooltip": {"valueDecimals": 0}
        }
    ]
}
static_conf_minute = {
    "chart": {"defaultSeriesType": 'spline'},
    "subtitle": {
        "text": '',
        "useHTML": True,
        "verticalAlign": 'top',
        "y": 40,
    },
    "credits": {"enabled": False},
    "exporting": {"filename": 'chaudiere'},
    "legend" : {
        "enabled": True,
        "align": 'left',
        "layout": 'vertical',
        "verticalAlign": 'top',
        "x": 10,
        "y": 80,
        "floating": True,
        "borderWidth": 1,
        "backgroundColor": '#FFFFFF'
    },
    'rangeSelector' : {
        'inputEnabled': 'false',
        'selected' : 5,
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
            }
        ]
    },
    'title': {'text': 'Chaudière'},

    'xAxis': {
            'plotBands': None
        },
    'yAxis': [
        {
            'labels': {'align': 'right','x': -3},
            'title': {'text': 'Température'},
            'softMin': 55,
            'softMax': 70,
            'top': str((0))+'%',
            'height': '100%',
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
            "name": InputName[TEMP_CHAUDIERE],
            "db": InputDb[TEMP_CHAUDIERE],
            "data": [],
            "yAxis": 0,
            "tooltip": {"valueDecimals": 1}
        }, 
        {
            "name": InputName[TEMP_FUMEE],
            "db": InputDb[TEMP_FUMEE],
            "data": [],
            "yAxis": 0,
            "tooltip": {"valueDecimals": 1}
        },
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

def json_context():
    context = {
        'app_base_url' : app.config['APP_BASE_URL'],
        'app_name' : app.config['APP_NAME']
    }
    return context

def json_date_picker():
    min = ChaudiereMinute.first(ChaudiereMinute).dt
    min_year =  min.strftime("%Y")
    min_month = str(int(min.strftime("%m")) - 1)
    min_day =   min.strftime("%d")
    max = ChaudiereMinute.last(ChaudiereMinute).dt
    max_year =  max.strftime("%Y")
    max_month = str(int(max.strftime("%m")) - 1)
    max_day =   max.strftime("%d")
    data = {
        'min_date' : str(min_year+'-'+min_month+'-'+min_day),
        'max_date' : str(max_year+'-'+max_month+'-'+max_day)
    }
    return data

"""
hour_length param is not used in view but parsed by javascript to request datas
"""
@charts_blueprint.route('/raw', defaults={'hour_length': 1}, methods=['GET'])
@charts_blueprint.route('/raw/<int:hour_length>', methods=['GET'])
def raw(hour_length):
    lastRecorddate = Chaudiere.last(Chaudiere).dt
    debugData = None
    return render_template('index.html', 
                            staticchartraw=True, 
                            staticchartminute=True, 
                            lastRecordAgo=util.pretty_date_ago(lastRecorddate),
                            debugData=debugData)

"""
receive form (navbar date)
"""
@charts_blueprint.route('/history_form', methods=['POST'])
def history_form():
    form = HistoryForm()
    if form.validate_on_submit():
        date = form.date.data.split('-')
        history_url = url_for('charts.history', year=date[0], month=date[1], day=date[2], hour=0, minute=0, hours=24)
        return redirect(history_url)
    else:
        return redirect(url_for('charts.now'))

"""
params for date, hours : length
"""
@charts_blueprint.route('/history/<string:year>/<string:month>/<string:day>/<string:hour>/<string:minute>/<string:hours>', methods=['GET'])
def history(year, month, day, hour, minute, hours):
    begin_date = year+'/'+month+'/'+day+'/'+hour+'/'+minute
    chart_date_hours = {'begin_date': begin_date, 'hours_length' : hours}
    return render_template('index.html',
                            context =             json_context(),
                            chart_date_hours =    chart_date_hours,
                            chart_legend =        ChartLegend,
                            render_static_chart = True,
                            history_form_data =   json_date_picker())

@charts_blueprint.route('/now', defaults={'hours': 1}, methods=['GET'])
@charts_blueprint.route('/now/<int:hours>', methods=['GET'])
def now(hours):
    """ 
    print a chart with datas 
    from : N `hours` ago 
    to : now
    """
    dt_now = datetime.now().replace(second=0, microsecond=0)
    dt = dt_now - timedelta(hours=hours)
    begin_date = str(dt.year)+'/'+str(dt.month)+'/'+str(dt.day)+'/'+str(dt.hour)+'/'+str(dt.minute)
    chart_date_hours = {'begin_date': begin_date, 'hours_length' : hours}
    return render_template('index.html',
                            context =             json_context(),
                            chart_date_hours =    chart_date_hours,
                            chart_legend =        ChartLegend,
                            render_static_chart = True,
                            history_form_data =   json_date_picker())

@charts_blueprint.route('/api_now', defaults={'hours': 1}, methods=['GET'])
@charts_blueprint.route('/api_now/<int:hours>', methods=['GET'])
def api_now(hours):
    """ 
    returns a json chart with datas 
    from : N `hours` ago 
    to : now
    """
    conf = json.loads(json.dumps(static_conf_minute)) #make a copy of original object
    dt_end = datetime.now().replace(second=0, microsecond=0)
    dt_begin = dt_end - timedelta(hours=hours)
    entries = ChaudiereMinute.query\
                         .order_by(ChaudiereMinute.dt)\
                         .filter(ChaudiereMinute.dt >= dt_begin)\
                         .filter(ChaudiereMinute.dt <= dt_end)\
                         .all()
    conf = create_chart(conf, entries)
    # Html Response
    response = make_response(json.dumps(conf))
    response.content_type = 'application/json'
    return response
    
@charts_blueprint.route('/api_history/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:hours>', methods=['GET'])
def api_history(year, month, day, hour, minute, hours):
    """ 
    returns a json chart with datas 
    from : given date (y m d h m) 
    to : given date + `hours`
    """
    conf = json.loads(json.dumps(static_conf_minute))#make a copy of original object
    dt_begin = datetime(year, month, day, hour, minute)
    dt_end = dt_begin + timedelta(hours=hours)
    entries = ChaudiereMinute.query\
                         .order_by(ChaudiereMinute.dt)\
                         .filter(ChaudiereMinute.dt >= dt_begin)\
                         .filter(ChaudiereMinute.dt <= dt_end)\
                         .all()
    conf = create_chart(conf, entries)
    # Html Response
    response = make_response(json.dumps(conf))
    response.content_type = 'application/json'
    return response

def create_chart(conf, entries):
    """ 
    Update Chart configuration and Datas 
    """
    serie_index = 0
    for serie in conf['series']:
        data = []
        for entry in entries:
            if entry is not None:
                data.append(entry.datatolist(str(serie['db'])))
        conf['series'][serie_index]['data'] = data
        serie_index += 1
    
    """ Add PlotBands """ 
    plotBands = []
    last_entry = len(entries)-1
    n = 1
    while n < last_entry and\
    entries[n].phase is not None and\
    entries[n] is not None and\
    entries[n].next().phase is not None:
        begin = entries[n].dt
        phase = entries[n].phase
        n += 1
        while entries[n] is not None and\
        entries[n].phase is not None and\
        entries[n].phase == phase and\
        n < last_entry:
            n += 1
        end = entries[n].dt
        plotBand = {
                        'color': PhaseColor[phase],
                        'from': datetime_to_timestamp(begin),
                        'to': datetime_to_timestamp(end)
                    }
        plotBands.append(plotBand)
    conf['xAxis']['plotBands'] = plotBands
    
    """ Add Labels """ 
    condition_flag_allumage =   '((prec.phase is not None) and (prec.phase is not PHASE_ALLUMAGE))'
    condition_next_is_not_maintien = '((next.phase is not None) and (next.phase is not PHASE_MAINTIEN))'
    labels = json.loads(json.dumps(ChartLabel)) #make a copy of original object
    labels['name'] = 'Labels'
    for entry in entries:
        if entry is not None and entry.phase is not None:
            #Label Allumage    
            if entry.phase == PHASE_ALLUMAGE and entry.all_prec_verify_condition(8, condition_flag_allumage):
                data = {
                        "x": datetime_to_timestamp(entry.dt),
                        "title": 'Allumage'
                       }
                labels['data'].append(data)
            """
            # Label Combustion    
            if entry.phase == PHASE_COMBUSTION and\
                entry.prec() is not None and\
                entry.prec().phase is not PHASE_COMBUSTION and\
                entry.all_next_verify_condition(5, condition_next_is_not_maintien):
                    data = {
                            "x": datetime_to_timestamp(entry.dt),
                            "title": 'Combustion'
                           }
                    labels['data'].append(data)
            """
    conf['series'].append(labels)

    """ Add Subtitle (plotbands legend) """
    #conf["subtitle"] = ChartLegend

    """ Add Title (date begin date end) """
    if len(entries) > 3:
        begin = pretty_date(entries[0].dt)
        end = pretty_date(entries[len(entries)-1].dt)
        #conf["title"]["text"] = 'Monitoring Chaudière du {0} au {1}'.format(begin, end)
        conf["title"]["text"]       = 'Monitoring Chaudière'
        conf["subtitle"]["text"]    = ' du {0} au {1}'.format(begin, end)

    else:
        conf["title"]["text"] = 'Monitoring Chaudière'

    """ Return new conf """
    return conf
     