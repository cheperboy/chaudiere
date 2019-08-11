# -*- coding: ISO-8859-1 -*-

import json

from ...constantes import *
from util import *

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
            if entry.event is not None:
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
    'navigator': {
        'enabled': True
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
local_display_static_conf_minute = {
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
    'rangeSelector': {
        'selected': 4,
        'inputEnabled': False,
        'buttonTheme': {
            'visibility': 'hidden'
        },
        'labelStyle': {
            'visibility': 'hidden'
        }
    },
    'navigator': {
        'enabled': False
    },
    'scrollbar': {
        'enabled': False
    },
    'title': {'text': 'chaudière'},

    'xAxis': {
            'plotBands': None
        },
    'yAxis': [
        {
            'labels': {'align': 'right','x': -3, 'style':{"fontSize": "20px"}},
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

