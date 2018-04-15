# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division

import time
from datetime import datetime, timedelta
from flask import current_app
from app import db

def dump_timestamp(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return int(time.mktime(value.timetuple())*1000)

def totimestamp(value):
    return time.mktime(value.timetuple())

class ChaudiereBase(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    temp0 = db.Column(db.Float)
    temp1 = db.Column(db.Float)
    watt0 = db.Column(db.Float)
    watt1 = db.Column(db.Float)
    watt2 = db.Column(db.Float)

    def __init__(self, timestamp, temp0, temp1, watt0, watt1, watt2):
        self.timestamp = timestamp
        self.temp0 = temp0
        self.temp1 = temp1
        self.watt0 = watt0
        self.watt1 = watt1 
        self.watt2 = watt2

    def __repr__(self):
        return '<Chaudiere {0} {1} {2} {3} {4} {5} {6}>'.format(self.id, self.timestamp, self.temp0, self.temp1, self.watt0, self.watt1, self.watt2)

    @classmethod
    def create(self, cls, timestamp, temp0, temp1, watt0, watt1, watt2):
        try:
            entry = cls(timestamp, temp0, temp1, watt0, watt1, watt2)
            db.session.add(entry)
            db.session.commit()
            ret = 'OK'
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
            self.watt0, 
            self.watt1, 
            self.watt2,
            self.id
        ]
       
    def papptolist(self):
        return [
            dump_timestamp(self.timestamp),
            self.papp,
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

                        
class ChaudiereMinute(ChaudiereBase):
    __bind_key__ = 'chaudiere_minute'
        
class ChaudiereHour(ChaudiereBase):
    __bind_key__ = 'chaudiere_hour'
    
class Chaudiere(ChaudiereBase):
    __bind_key__ = 'chaudiere'
    
    def __init__(self, timestamp, temp0=1, temp1=1, watt0=1, watt1=1, watt2=1):
        self.timestamp = timestamp
        self.temp0 = temp0
        self.temp1 = temp1
        self.watt0 = watt0
        self.watt1 = watt1 
        self.watt2 = watt2

class Wattbuffer(db.Model):
    __bind_key__ = 'watt_buffer'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    watt0 = db.Column(db.Float)
    watt1 = db.Column(db.Float)
    watt2 = db.Column(db.Float)

    def __init__(self, timestamp, watt0, watt1, watt2):
        self.timestamp = timestamp
        self.watt0 = watt0
        self.watt1 = watt1 
        self.watt2 = watt2

    def __repr__(self):
        return '<Wattbuffer {0} {1} {2} {3} {4}>'.format(self.id, self.timestamp, self.watt0, self.watt1, self.watt2)

    @classmethod
    def create(self, cls, timestamp, watt0, watt1, watt2):
        try:
            entry = cls(timestamp, watt0, watt1, watt2)
            db.session.add(entry)
            db.session.commit()
            ret = 'OK'
        except Exception as e:
            ret = 'Not Ok'
            print e
        return ret
    
    def tolist(self):
        """Return Object data in list format"""
        return [
            dump_timestamp(self.timestamp),
            self.watt0, 
            self.watt1, 
            self.watt2,
            self.id
        ]
       
    def papptolist(self):
        return [
            dump_timestamp(self.timestamp),
            self.papp,
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
