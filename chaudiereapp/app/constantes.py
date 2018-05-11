# -*- coding: utf-8 -*-
"""
Phases constantes
"""
PHASE_UNDEFINED  = 0 
PHASE_COMBUSTION = 6
PHASE_ALLUMAGE   = 7
PHASE_MAINTIEN   = 8
PHASE_ARRET      = 9

PhaseColor = {
    PHASE_UNDEFINED  : '#f2f2f2', #'grey'
    PHASE_COMBUSTION : '#e6f2ff', #'blue'
    PHASE_ALLUMAGE   : '#ffe6e6', #'red'
    PHASE_MAINTIEN   : '#e6ffe6', #'green'
    PHASE_ARRET      : '#b3b3b3', #'black'
}
PhaseName = {
    PHASE_UNDEFINED  : 'UNDEFINED',  
    PHASE_COMBUSTION : 'COMBUSTION',
    PHASE_ALLUMAGE   : 'ALLUMAGE',
    PHASE_MAINTIEN   : 'MAINTIEN',
    PHASE_ARRET      : 'ARRET' 
}

"""
Physical inpurs / database fields
"""
Inputs = { 
    'temp_chaudiere' :  {'db': 'temp0', 'name': 'Temp chaudiere'},
    'temp_fumee' :      {'db': 'temp1', 'name': 'Temp fumee'},
    'temp_retour' :     {'db': 'temp2', 'name': 'Temp retour'},
    'vent_secondaire' : {'db': 'watt0', 'name': 'Vent secondaire'},
    'allumage' :        {'db': 'watt1', 'name': 'Allumage'},
    'vent_primaire' :   {'db': 'watt2', 'name': 'Vent primaire'},
    'alimentation' :    {'db': 'watt3', 'name': 'Alimentation'},
    'phase' :           {'db': 'phase', 'name': 'Phase'}
} 
