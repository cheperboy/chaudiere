# -*- coding: utf-8 -*-
from __future__ import division
from datetime import datetime

# from flask import current_app
from .. import db
from ..constantes import *

  
class AdminConfig(db.Model):
    __bind_key__ = 'admin_config'
    
    id                              = db.Column(db.Integer, primary_key=True)
    temp_chaudiere_failure          = db.Column(db.Integer, nullable=False) # used for process_phase.py
    chaudiere_db_rotate_hours       = db.Column(db.Integer, nullable=False) 
    chaudiere_minute_db_rotate_days = db.Column(db.Integer, nullable=False) 
    alerts_enable                   = db.Column(db.Boolean, nullable=False) 
    comment                         = db.Column(db.String(300), nullable=True) # free comment
    updated_at                      = db.Column(db.DateTime, 
                                                default=datetime.now(),
                                                nullable=False,
                                                onupdate=datetime.now())

    def __init__(
                self, 
                temp_chaudiere_failure, 
                chaudiere_db_rotate_hours,
                chaudiere_minute_db_rotate_days,
                alerts_enable,
                comment):
        
        self.temp_chaudiere_failure          = temp_chaudiere_failure
        self.chaudiere_db_rotate_hours       = chaudiere_db_rotate_hours
        self.chaudiere_minute_db_rotate_days = chaudiere_minute_db_rotate_days
        self.alerts_enable                   = alerts_enable
        self.comment                         = comment

    def __repr__(self):
        ret = 'AdminConfig\n'
        ret += 'id : {0}\n'.format(self.id)
        ret += 'temp_chaudiere_failure : {0}\n'.format(self.temp_chaudiere_failure)
        ret += 'chaudiere_db_rotate_hours : {0}\n'.format(self.chaudiere_db_rotate_hours)
        ret += 'chaudiere_minute_db_rotate_days : {0}\n'.format(self.chaudiere_minute_db_rotate_days)
        ret += 'alerts_enable : {0}\n'.format(self.alerts_enable)
        ret += 'comment : {0}\n'.format(self.comment)
        ret += 'updated_at : {0}\n'.format(self.updated_at)
        return (ret)

    @classmethod
    def first(self, cls):
        try:
            return(db.session.query(cls).order_by(cls.id.asc()).first())
        except Exception:
            return(None)
    
    @classmethod
    def last(self, cls):
        return(db.session.query(cls).order_by(cls.id.desc()).first())
    
    @classmethod
    def all(self, cls):
        return(db.session.query(cls).order_by(cls.id.desc()).all())
    
    @classmethod
    def get(self, cls, field_name):
        admin_config = db.session.query(cls).order_by(cls.id.asc()).first()
        return getattr(admin_config, field_name)
