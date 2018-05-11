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
    PHASE_COMBUSTION : '#ffe6e6', #'red'
    PHASE_ALLUMAGE   : '#fff0e6', #'orange'
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
Phases = {
    0 : {'value': 0, 'name': 'UNDEFINED',   'color': 'grey'     },
    6 : {'value': 6, 'name': 'COMBUSTION',  'color': 'red'      },
    7 : {'value': 7, 'name': 'ALLUMAGE',    'color': 'orange'   },
    8 : {'value': 8, 'name': 'MAINTIEN',    'color': 'green'    },
    9 : {'value': 9, 'name': 'ARRET',       'color': 'black'    }
}                              
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
