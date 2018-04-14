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

class TeleinfoBase(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    base = db.Column(db.Integer)
    papp = db.Column(db.Integer)
    iinst1 = db.Column(db.Float)
    iinst2 = db.Column(db.Float)
    iinst3 = db.Column(db.Float)

    def __init__(self, timestamp, base, papp, iinst1, iinst2, iinst3):
        self.timestamp = timestamp
        self.base = base
        self.papp = papp
        self.iinst1 = iinst1
        self.iinst2 = iinst2 
        self.iinst3 = iinst3

    def __repr__(self):
        return '<Teleinfo {0} {1} : {2}, {3}>'.format(self.id, self.timestamp, self.base, self.papp)

    @classmethod
    def create(self, cls, timestamp, base, papp, iinst1, iinst2, iinst3):
        try:
            entry = cls(timestamp, base, papp, iinst1, iinst2, iinst3)
            entry = cls(timestamp, base, papp, iinst1, iinst2, iinst3)
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
            self.base,
            self.papp,
            self.iinst1,
            self.iinst2,
            self.iinst3,
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

                        
class TeleinfoMinute(TeleinfoBase):
    __bind_key__ = 'teleinfo_minute'
        
class TeleinfoHour(TeleinfoBase):
    __bind_key__ = 'teleinfo_hour'
    
class Teleinfo(TeleinfoBase):
    __bind_key__ = 'teleinfo'
        
    def __init__(self, timestamp, base=1, papp=1, iinst1=1, iinst2=1, iinst3=1):
        self.timestamp = timestamp
        self.base = base
        self.papp = papp
        self.iinst1 = iinst1
        self.iinst2 = iinst2 
        self.iinst3 = iinst3

       
