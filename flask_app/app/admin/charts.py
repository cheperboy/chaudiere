import json

from ..constantes import *
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