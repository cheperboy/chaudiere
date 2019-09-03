# -*- coding: utf-8 -*-
"""
Application Values
"""
TEMP_CHAUDIERE_FAILURE_DEFAULT          = 62    # Min Water temp before alerting of potential chaudiere failure
CHAUDIERE_DB_ROTATE_HOURS_DEFAULT       = 2     
CHAUDIERE_MINUTE_DB_ROTATE_DAYS_DEFAULT = 35
ALERTS_ENABLE_DEFAULT                   = False # Boolean to disable alerts (SMS/Mail) unless enable by user

"""
Phases
"""
PHASE_UNDEFINED         = 0 
PHASE_COMBUSTION        = 6
PHASE_ALLUMAGE          = 7
PHASE_MAINTIEN          = 8
PHASE_ARRET             = 9
PHASE_RISQUE_BOURAGE    = 10
PHASE_SURVEILLANCE      = 11 # idem COMBUSTION Mais mais fonctionnement à surveiller

PhaseColor = {
    PHASE_UNDEFINED         : '#f2f2f2', # grey
    PHASE_COMBUSTION        : '#e6f2ff', # blue
    PHASE_ALLUMAGE          : '#ffff99', # yellow
    PHASE_MAINTIEN          : '#e6ffe6', # green
    PHASE_ARRET             : '#ff4d4d', # red
    PHASE_RISQUE_BOURAGE    : '#b32400', # rouge sombre
    PHASE_SURVEILLANCE      : '#ff80b3', # rose
    }
PhaseName = {
    PHASE_UNDEFINED         : 'Non defini',  
    PHASE_COMBUSTION        : 'Combustion',
    PHASE_ALLUMAGE          : 'Allumage',
    PHASE_MAINTIEN          : 'Maintien de feu',
    PHASE_ARRET             : 'Arret',
    PHASE_RISQUE_BOURAGE    : 'Silo vide ou Risque Bourrage',
    PHASE_SURVEILLANCE      : 'Combustion a surveiller',
    }

"""
Events
"""
EVENT_ALERT     = 0
EVENT_ALLUMAGE  = 1
EVENT_ARRET     = 2

EventColor = {
    EVENT_ALERT     : '#f2f2f2', # grey
    EVENT_ALLUMAGE  : '#e6f2ff', # blue
    EVENT_ARRET     : '#ffff99', # yellow
    }
EventName = {
    EVENT_ALERT     : 'Alert mail/sms',  
    EVENT_ALLUMAGE  : 'Allumage',
    EVENT_ARRET     : 'Arret',
    }

"""
Physical inputs / database fields
"""
TEMP_CHAUDIERE  = 0 
TEMP_FUMEE      = 1
TEMP_RETOUR     = 2
VENT_SECONDAIRE = 3
ALLUMAGE        = 4
VENT_PRIMAIRE   = 5
ALIMENTATION    = 6
PHASE           = 7

InputDb = {
    TEMP_CHAUDIERE  : 'temp0',
    TEMP_FUMEE      : 'temp1',
    TEMP_RETOUR     : 'temp2',
    VENT_SECONDAIRE : 'watt0',
    ALLUMAGE        : 'watt1',
    VENT_PRIMAIRE   : 'watt2',
    ALIMENTATION    : 'watt3',
    PHASE           : 'phase'
    }
    
InputName = {
    TEMP_CHAUDIERE  : 'Temp chaudiere'  ,
    TEMP_FUMEE      : 'Temp fumee'      ,
    TEMP_RETOUR     : 'Temp retour'     ,
    VENT_SECONDAIRE : 'Vent secondaire' ,
    ALLUMAGE        : 'Allumage'        ,
    VENT_PRIMAIRE   : 'Vent primaire'   ,
    ALIMENTATION    : 'Alimentation'    ,
    PHASE           : 'Phase'           
    }

""" ChartLabel """    
ChartLabel = {
    "type": 'flags',
    "name": '',
    "data": [],
    "onSeries": 'dataseries',
    "shape": 'squarepin',
    "showInLegend": False
    }

""" ChartLegend """    
ChartLegend = {
    "text": '<b>Phases</b> : ',
    "useHTML": True,
    "verticalAlign": 'top',
    "y": 55,
    }
        
for key in PhaseName.keys():
    ChartLegend['text'] += '<span style="background-color: '+PhaseColor[key]+\
                                            '; border-radius: 3px; padding: 2px 6px; margin: 4px 5px;">' +\
                                            PhaseName[key] + '</span>'


