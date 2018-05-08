# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division

import time, calendar
from datetime import datetime, timedelta
from flask import current_app
from app import db

def dump_timestamp(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
#    return int(time.mktime(value.timetuple())*1000)
    return int(calendar.timegm(value.timetuple())*1000)

def totimestamp(value):
    return time.mktime(value.timetuple())

class ChaudiereBase(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    temp0 = db.Column(db.Float)
    temp1 = db.Column(db.Float)
    temp2 = db.Column(db.Float)
    watt0 = db.Column(db.Integer)
    watt1 = db.Column(db.Integer)
    watt2 = db.Column(db.Integer)
    watt3 = db.Column(db.Integer)
    phase = db.Column(db.Integer)
    event = db.Column(db.String(100))

    def __init__(self, timestamp, temp0, temp1, temp2, watt0, watt1, watt2, watt3, phase, event):
        self.timestamp = timestamp
        self.temp0 = temp0
        self.temp1 = temp1
        self.temp2 = temp2
        self.watt0 = watt0
        self.watt1 = watt1 
        self.watt2 = watt2
        self.watt3 = watt3
        self.phase = phase
        self.event = event

    def __repr__(self):
        return '<Chaudiere {0} {1} {2} {3} {4} {5} {6}>'.format(self.id, self.timestamp, self.temp0, self.temp1, self.temp2, self.watt0, self.watt1, self.watt2, self.watt3)

    @classmethod
    def create(self, cls, timestamp, temp0, temp1, temp2, watt0, watt1, watt2, watt3, phase, event):
        try:
            entry = cls(timestamp, temp0, temp1, temp2, watt0, watt1, watt2, watt3, phase, event)
            db.session.add(entry)
            db.session.commit()
            ret = str(entry)
            print ret
        except Exception as e:
            ret = 'Not Ok'
            print e
        return ret
    
    def tolist(self):
        """Return Object data in list format"""
        return [
            dump_timestamp(self.timestamp),
            self.temp0, 
            self.temp1, 
            self.temp2, 
            self.watt0, 
            self.watt1, 
            self.watt2,
            self.watt3,
            self.phase,
            self.event,
            self.id
        ]
       
    def watt0tolist(self):
        return [
            dump_timestamp(self.timestamp),
            self.watt0,
       ]

    """
    return one field called data in a list with timestamp
    [timestamp, data]
    """
    def datatolist(self, data):
        return [
            dump_timestamp(self.timestamp),
            getattr(self, data) # same as e.g. self.temp0
       ]

    @classmethod
    def last(self, cls):
        return(db.session.query(cls).order_by(cls.id.desc()).first())

    @classmethod
    def first(self, cls):
        return(db.session.query(cls).order_by(cls.id.asc()).first())

    @classmethod
    def get_between_date(self, cls, begin, end):
        return (db.session.query(cls) \
                .filter(cls.timestamp > datetime(begin.year, begin.month, begin.day, begin.hour, begin.minute)) \
                .filter(cls.timestamp < datetime(end.year, end.month, end.day, end.hour, end.minute)) \
                .order_by(cls.id.desc()) \
                .all())

    @classmethod
    def get_by_date(self, cls, dt):
        ts = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)
        return db.session.query(cls).filter_by(timestamp=ts).first()

    @classmethod
    def get_by_timestamp(self, cls, ts):
        return db.session.query(cls).filter_by(timestamp=ts).first()

                        
class ChaudiereMinute(ChaudiereBase):
    __bind_key__ = 'chaudiere_minute'
    
    """ return precedent entry: one minute before self"""
    def prec(self):
        ts = datetime(self.timestamp.year, self.timestamp.month, self.timestamp.day, self.timestamp.hour, self.timestamp.minute)
        ts = ts - timedelta(minutes=1)
        return db.session.query(self.__class__).filter_by(timestamp=ts).first()
        
    """ return a list of precedents entries: x minute before self"""
    def precs(self, minutes): 
        entries = []
        ts = datetime(self.timestamp.year, self.timestamp.month, self.timestamp.day, self.timestamp.hour, self.timestamp.minute)
        for minute in range(1, minutes):
            entry = db.session.query(self.__class__).filter_by(timestamp=ts - timedelta(minutes=minute)).first()
            entries.append(entry)
        return entries
        
    """ at least onre prec respect condition """
    def at_least_one_prec_verify_condition(self, minutes, condition):
        for prec in self.precs(minutes):
            if eval(condition):
                return True
        return False
        
class ChaudiereHour(ChaudiereBase):
    __bind_key__ = 'chaudiere_hour'
    
class Chaudiere(ChaudiereBase):
    __bind_key__ = 'chaudiere'
"""    
    def __init__(self, timestamp, temp0=1, temp1=1, temp2=2, watt0=1, watt1=1, watt2=1, watt3=1):
        self.timestamp = timestamp
        self.temp0 = temp0
        self.temp1 = temp1
        self.temp2 = temp2
        self.watt0 = watt0
        self.watt1 = watt1 
        self.watt2 = watt2
        self.watt3 = watt3
"""
