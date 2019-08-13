# -*- coding: utf-8 -*-
from __future__ import division

import time, calendar
from datetime import datetime, timedelta
from flask import current_app
from app import db
from app.constantes import *
from util import *

  
class ChaudiereBase(db.Model):
    __abstract__ = True
    id      = db.Column(db.Integer, primary_key=True)
    dt      = db.Column(db.DateTime)
    temp0   = db.Column(db.Float)
    temp1   = db.Column(db.Float)
    temp2   = db.Column(db.Float)
    watt0   = db.Column(db.Integer)
    watt1   = db.Column(db.Integer)
    watt2   = db.Column(db.Integer)
    watt3   = db.Column(db.Integer)
    phase   = db.Column(db.Integer)     # filled with constant
    change  = db.Column(db.Boolean)     # filled with constant in phase change
    event   = db.Column(db.String(100)) # filled with constant in case of ALERT

    def __init__(self, dt, temp0, temp1, temp2, watt0, watt1, watt2, watt3, phase, change, event):
        self.dt     = dt
        self.temp0  = temp0
        self.temp1  = temp1
        self.temp2  = temp2
        self.watt0  = watt0
        self.watt1  = watt1 
        self.watt2  = watt2
        self.watt3  = watt3
        self.phase  = phase
        self.change = change
        self.event  = event

    def __repr__(self):
        return '<Chaudiere {0} {1} {2} {3} {4} {5} {6}>'.format(self.id, self.dt, self.watt0, self.temp0, self.phase, self.change, self.event)

    @classmethod
    def create(self, cls, dt, temp0, temp1, temp2, watt0, watt1, watt2, watt3, phase, change, event):
        try:
            entry = cls(dt, temp0, temp1, temp2, watt0, watt1, watt2, watt3, phase, change, event)
            db.session.add(entry)
            db.session.commit()
            ret = str(entry)
            print (ret)
        except Exception as e:
            ret = 'Not Ok'
            print (e)
        return (ret)
    
    """
    return one field corresponding to given InputDb constante (ATTR_ID)
    """
    def get(self, ATTR_ID):
        return getattr(self, InputDb[ATTR_ID])

    def tolist(self):
        """Return Object data in list format"""
        return [
            datetime_to_timestamp(self.dt),
            self.temp0, 
            self.temp1, 
            self.temp2, 
            self.watt0, 
            self.watt1, 
            self.watt2,
            self.watt3,
            self.phase,
            self.change,
            self.event,
            self.id
        ]
       
    """
    return one field called data in a list with timestamp
    [datetime, data]
    """
    def datatolist(self, data):
        return [
            datetime_to_timestamp(self.dt),
            getattr(self, data) # same as e.g. self.temp0
       ]

    @classmethod
    def last(self, cls):
        return(db.session.query(cls).order_by(cls.dt.desc()).first())

    @classmethod
    def all(self, cls):
        return(db.session.query(cls).order_by(cls.dt.desc()).all())

    @classmethod
    def first(self, cls):
        return(db.session.query(cls).order_by(cls.dt.asc()).first())

    @classmethod
    def get_between_date(self, cls, dt_begin, dt_end):
        return (db.session.query(cls) \
                .filter(cls.dt > dt_begin) \
                .filter(cls.dt < dt_end) \
                .order_by(cls.dt.desc()) \
                .all())

    @classmethod
    def get_older_than(self, cls, dt_end):
        return (db.session.query(cls) \
                .filter(cls.dt < dt_end) \
                .order_by(cls.dt.desc()) \
                .all())

    @classmethod
    def get_by_timestamp(self, cls, ts):
        dt = datetime.fromtimestamp(ts)
        return db.session.query(cls).filter_by(dt=dt).first()

    @classmethod
    def get_by_approx_date(self, cls, dt):
        entry = db.session.query(cls)\
            .filter(cls.dt > datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)) \
            .first()
        return entry

    @classmethod
    def get_by_datetime(self, cls, dt):
        return db.session.query(cls).filter_by(dt=dt).first()

                        
class ChaudiereMinute(ChaudiereBase):
    __bind_key__ = 'chaudiere_minute'
    
    """ return precedent entry: one minute before self"""
    def prec(self):
        dt = self.dt - timedelta(minutes=1)
        return db.session.query(self.__class__).filter_by(dt=dt).first()
        
    """ return next entry: one minute after self"""
    def next(self):
        dt = self.dt + timedelta(minutes=1)
        return db.session.query(self.__class__).filter_by(dt=dt).first()
        
    """ return a list of precedents entries: x minute before self"""
    def precs(self, minutes): 
        entries = []
        for minute in range(1, minutes):
            entry = db.session.query(self.__class__).filter_by(dt=self.dt - timedelta(minutes=minute)).first()
            entries.append(entry)
        return entries
        
    """ return a list of precedents entries: x minute before self"""
    def nexts(self, minutes): 
        entries = []
        for minute in range(1, minutes):
            entry = db.session.query(self.__class__).filter_by(dt=self.dt + timedelta(minutes=minute)).first()
            entries.append(entry)
        return entries
        
    def at_least_one_prec_verify_condition(self, minutes, condition):
        """ 
        At least one prec respect condition 
        eg : 
        condition = '((prec is not None) and (prec.phase is PHASE_ALLUMAGE))'
        entry.at_least_one_prec_verify_condition(5, condition)
        """
        for prec in self.precs(minutes):
            if eval(condition):
                return True
        return False
        
    def all_prec_verify_condition(self, minutes, condition):
        for prec in self.precs(minutes):
            if prec is not None:
                if not eval(condition):
                    return False
        return True
        
    def all_next_verify_condition(self, minutes, condition):
        for next in self.nexts(minutes):
            if next is not None:
                if not eval(condition):
                    return False
        return True
        
        
class ChaudiereHour(ChaudiereBase):
    __bind_key__ = 'chaudiere_hour'
    
class Chaudiere(ChaudiereBase):
    __bind_key__ = 'chaudiere'
