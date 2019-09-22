# -*- coding: utf-8 -*-
# from __future__ import absolute_import
import time, datetime
import urllib, requests
import json
from datetime import datetime, timedelta
from random import random
import pprint
import copy

from flask import Blueprint, render_template, request, jsonify, make_response, redirect, url_for
from flask import current_app as app

from ..views.auth import auth
from ..models import Chaudiere, ChaudiereMinute
from ..constantes import *
from util import datetime_to_timestamp
from util import pretty_date

debug_blueprint = Blueprint("debug", __name__, url_prefix='/debug')

@debug_blueprint.route('/now', defaults={'hours': 1}, methods=['GET'])
@debug_blueprint.route('/now/<int:hours>', methods=['GET'])
def now(hours):
    """ 
    This route print a chart with datas 
    from : N `hours` ago to : now

    :param hours: Number of hours back history from now. 
    :type hours: int. 
    :returns: render_template('charts/charts.html', ...). 

    """ 
    dt_end      = datetime.now().replace(second=0, microsecond=0)
    dt_begin    = dt_end - timedelta(hours=hours)
    json_chart_minute = create_chart_minute(dt_begin, dt_end)
    json_chart_second = create_chart_second(dt_begin, dt_end)
    return render_template('charts/charts.html',
                            chart_debug_conf_minute    = json_chart_minute,
                            chart_debug_conf_second    = json_chart_second,
                            render_debugchart_minute   = True,
                            render_debugchart_second   = True)

def create_chart_minute(dt_begin, dt_end):
    entries     = get_ChaudiereMinute(dt_begin, dt_end)
    chart_minute = Chart(entries,
                        default_template, 
                        chart_type='stepline',
                        # chart_type='spline',
                        title_text='Minute',
                        exporting_filename='Minute')
                        
    chart_minute.add_serie(InputName[TEMP_CHAUDIERE], InputDb[TEMP_CHAUDIERE], yAxis=0)
    chart_minute.add_serie(InputName[TEMP_FUMEE], InputDb[TEMP_FUMEE], yAxis=0)
    chart_minute.add_serie(InputName[ALLUMAGE], InputDb[ALLUMAGE], yAxis=1)
    chart_minute.add_serie(InputName[ALIMENTATION], InputDb[ALIMENTATION], yAxis=1)
    chart_minute.add_serie(InputName[VENT_PRIMAIRE], InputDb[VENT_PRIMAIRE], yAxis=1)
    chart_minute.add_serie(InputName[PHASE], InputDb[PHASE], yAxis=2)
    
    chart_minute.subtitle_entries_date()
    chart_minute.add_yAxis('température', opposite=False)
    chart_minute.add_yAxis('current', opposite=True)
    chart_minute.add_yAxis('phase', opposite=True)
    chart_minute.navigator_enable(True)
    chart_minute.scrollbar_enable(True)
    chart_minute.range_selector()
    chart_minute.add_plotbands_phase()
    return (chart_minute.json)

def create_chart_second(dt_begin, dt_end):
    entries     = get_Chaudiere(dt_begin, dt_end)
    chart_second = Chart(entries,
                        default_template, 
                        chart_type='stepline',
                        # chart_type='spline',
                        title_text='Second',
                        exporting_filename='second')
                        
    chart_second.add_serie(InputName[TEMP_CHAUDIERE], InputDb[TEMP_CHAUDIERE], yAxis=0)
    chart_second.add_serie(InputName[TEMP_FUMEE], InputDb[TEMP_FUMEE], yAxis=0)
    chart_second.add_serie(InputName[ALLUMAGE], InputDb[ALLUMAGE], yAxis=1)
    chart_second.add_serie(InputName[ALIMENTATION], InputDb[ALIMENTATION], yAxis=1)
    chart_second.add_serie(InputName[VENT_PRIMAIRE], InputDb[VENT_PRIMAIRE], yAxis=1)
    chart_second.add_serie(InputName[PHASE], InputDb[PHASE], yAxis=2)
    
    chart_second.subtitle_entries_date()
    chart_second.add_yAxis('température', opposite=False)
    chart_second.add_yAxis('current', opposite=True)
    chart_minute.add_yAxis('phase', opposite=True)
    chart_second.navigator_enable(True)
    chart_second.scrollbar_enable(True)
    chart_second.range_selector()
    chart_second.add_plotbands_phase()
    return (chart_second.json)

def get_ChaudiereMinute(dt_begin, dt_end):
    entries = ChaudiereMinute.query\
                         .order_by(ChaudiereMinute.dt)\
                         .filter(ChaudiereMinute.dt >= dt_begin)\
                         .filter(ChaudiereMinute.dt <= dt_end)\
                         .all()
    return(entries)

def get_Chaudiere(dt_begin, dt_end):
    entries = Chaudiere.query\
                         .order_by(Chaudiere.dt)\
                         .filter(Chaudiere.dt >= dt_begin)\
                         .filter(Chaudiere.dt <= dt_end)\
                         .all()
    return(entries)


class Chart:
    """ Build a chart with options
        1. init with some entries (eg: class Entry)
            * give a template
            * give a chart_type (stepline | spline)
        2. Add series (selected fields in Entry model)
        3. select options
    """
    def __init__(self, 
                entries,
                template,
                chart_type,             # spline | stepline
                exporting_filename='chart', 
                title_text='chart'):
                
        self.entries = entries
        self.json = json.loads(json.dumps(template))
        self.chart_type = chart_type
        # self.add_entries()
        if self.chart_type == 'spline':
            self.json['chart']['defaultSeriesType'] = 'spline'            
        self.json['title']['text']         = title_text            # chart title
        self.json['exporting']['filename'] = exporting_filename    # downloaded filename
    
    def add_serie(self, name, db_fieldname, yAxis=0):
        """ Add a serie of data
        name         : display in chart legend
        db_fieldname : used to retrive data among entries fields (temp0, temp1, watt0, ...)
        yAxis        : 0 or 1 (yAxis must be defined)
        """
        data = []
        for entry in self.entries:
            if entry is not None:
                data.append(entry.datatolist(db_fieldname))

        serie = {
            "name"      : name,
            "db"        : db_fieldname,
            "data"      : data,
            "yAxis"     : yAxis,
            "tooltip"   : {"valueDecimals": 1}
        } 
        if self.chart_type == 'stepline':
            serie["step"] = True
        
        self.json['series'].append(serie)
        
    def add_yAxis(self, title_text, opposite=False):
        """ 
        """
        yAxis = {
            'labels': {'align': 'right','x': -3},
            'title': {'text': title_text},
            'softMin': 55,
            'softMax': 70,
            'top': str((0))+'%',
            'height': '100%',
            'lineWidth': 1,
            'opposite': opposite
        }
 
        self.json['yAxis'].append(yAxis)
        
    def navigator_enable(self, enable):
        self.json['navigator']['enabled']   = enable
    
    def scrollbar_enable(self, enable):
        self.json['scrollbar']['enabled']   = enable

    def range_selector(self):
        self.json["rangeSelector"] = {
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
        }

    def subtitle_entries_date(self):
        """ Add subtitle (date begin,  date end) """
        if len(self.entries) > 3:
            begin = pretty_date(self.entries[0].dt)
            end = pretty_date(self.entries[len(self.entries)-1].dt)
            self.json["subtitle"]["text"] = ' du {0} au {1}'.format(begin, end)
            self.json["subtitle"]["useHTML"] = True
            self.json["subtitle"]["verticalAlign"] = 'top'
            self.json["subtitle"]["y"] = 40

    def add_plotbands_phase(self):
        """ Add PlotBands related to show Phase""" 
        plotBands = []
        last_entry = len(self.entries)-1
        n = 1
        while n < last_entry and\
        self.entries[n].phase is not None and\
        self.entries[n] is not None and\
        self.entries[n].next().phase is not None:
            begin = self.entries[n].dt
            phase = self.entries[n].phase
            n += 1
            while self.entries[n] is not None and\
            self.entries[n].phase is not None and\
            self.entries[n].phase == phase and\
            n < last_entry:
                n += 1
            end = self.entries[n].dt
            plotBand = {
                            'color': PhaseColor[phase],
                            'from': datetime_to_timestamp(begin),
                            'to': datetime_to_timestamp(end)
                        }
            plotBands.append(plotBand)
        self.json['xAxis']['plotBands'] = plotBands
        
    
default_template = {
    "chart": {},
    "subtitle": {},
    "credits": {"enabled": False},
    "exporting": {"filename": ''},
    "legend" : {
        "enabled": True,
        "align": 'left',
        "layout": 'vertical',
        "verticalAlign": 'top',
        "x": 50,
        "y": 80,
        "floating": True,
        "borderWidth": 1,
        "backgroundColor": '#FFFFFF'
    },
    'rangeSelector' : False,
    'navigator': {'enabled': False},
    'scrollbar': {'enabled': False},
    'title': {'text': ''},
    'xAxis': {'plotBands': None},
    'yAxis': [
    ],
    'tooltip': {
        'shared': True,
        'split': False,
        'crosshairs': True
    },
    "series": []
}
