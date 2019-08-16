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

from ...views.auth import auth
from ...models import Chaudiere, ChaudiereMinute
from ...constantes import *
from .charts import *
from util import datetime_to_timestamp

charts_blueprint = Blueprint("charts", __name__, url_prefix='/charts')

def json_context():
    context = {
        'app_base_url' : app.config['APP_BASE_URL'],
        'app_name' : app.config['APP_NAME']
    }
    return context

def json_date_picker():
    if ChaudiereMinute.first(ChaudiereMinute):
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
    else:
        return ""
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
                            lastRecordAgo=pretty_date_ago(lastRecorddate),
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
    json_template = static_conf_minute
    chart_params = {'json_template': json_template, 'begin_date': begin_date, 'hours_length' : hours}
    return render_template('index.html',
                            context =             json_context(),
                            chart_params =        chart_params,
                            chart_legend =        ChartLegend,
                            render_static_chart = True,
                            history_form_data =   json_date_picker())

@charts_blueprint.route('/now', defaults={'hours': 1}, methods=['GET'])
@charts_blueprint.route('/now/<int:hours>', methods=['GET'])
def now(hours):
    """ 
    This route print a chart with datas 
    from : N `hours` ago to : now

    :param hours: Number of hours back history from now. 
    :type hours: int. 
    :returns: render_template('charts/charts.html', ...). 

    """ 
    dt_now = datetime.now().replace(second=0, microsecond=0)
    dt = dt_now - timedelta(hours=hours)
    begin_date = str(dt.year)+'/'+str(dt.month)+'/'+str(dt.day)+'/'+str(dt.hour)+'/'+str(dt.minute)
    chart_params = {'json_template': 'static_conf_minute', 'begin_date': begin_date, 'hours_length' : hours}
    return render_template('charts/charts.html',
                            context =             json_context(),
                            chart_params =        chart_params,
                            chart_legend =        ChartLegend,
                            render_static_chart = True,
                            history_form_data =   json_date_picker())

@charts_blueprint.route('/', defaults={'hours': 1}, methods=['GET'])
@charts_blueprint.route('/<int:hours>', methods=['GET'])
def local_display(hours):
    """ 
    print a chart with datas 
    from : N `hours` ago 
    to : now
    """
    dt_now = datetime.now().replace(second=0, microsecond=0)
    dt = dt_now - timedelta(hours=hours)
    begin_date = str(dt.year)+'/'+str(dt.month)+'/'+str(dt.day)+'/'+str(dt.hour)+'/'+str(dt.minute)
    chart_params = {'json_template': 'local_display_static_conf_minute', 'begin_date': begin_date, 'hours_length' : hours}
    return render_template('charts/charts.html',
                            local_display =       True,
                            context =             json_context(),
                            chart_params =        chart_params,
                            chart_legend =        ChartLegend,
                            render_static_chart = True)
    
@charts_blueprint.route('/api_chart_data/<string:chart_json_template>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:hours>', methods=['GET'])
def api_chart_data(chart_json_template, year, month, day, hour, minute, hours):
    """ 
    returns a json chart with datas 
    from : given date (y m d h m) 
    to : given date + `hours`
    the template of json conf is selected with chart_json_template passed by url. this parameter shall be equal to one of the json variable defined at the begining of this file (eg: static_conf_minute)
    """
    template = eval(chart_json_template) #retrive the json variable defined at the beginning of this file whose name is given by javascript
    conf = json.loads(json.dumps(template))# make a copy of original object
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

