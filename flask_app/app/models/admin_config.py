# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division

from flask import current_app
from app import db
from app.constantes import *

  
class AdminConfig(db.Model):
    __bind_key__ = 'admin_config'
    
    id                                = db.Column(db.Integer, primary_key=True)
    temp_chaudiere_failure  = db.Column(db.Integer) # used for process_phase.py
    comment                     = db.Column(db.String(300), nullable=True) # free comment
    updated_at                  = db.Column(db.DateTime, nullable=True)     # last modif date

    def __init__(self, temp_chaudiere_failure, comment, updated_at):
        self.temp_chaudiere_failure = temp_chaudiere_failure
        self.comment  = comment
        self.updated_at  = updated_at

    def __repr__(self):
        ret = 'AdminConfig\n'
        ret += 'id {0}'.format(self.id)
        ret += 'temp_chaudiere_failure {0}'.format(self.temp_chaudiere_failure)
        ret += 'comment {0}'.format(self.comment)
        ret += 'updated_at {0}'.format(self.updated_at)
        return (ret)

    @classmethod
    def first(self, cls):
        return(db.session.query(cls).order_by(cls.id.asc()).first())
    
    @classmethod
    def get(self, cls, field_name):
        admin_config = db.session.query(cls).order_by(cls.id.asc()).first()
        return getattr(admin_config, field_name)
