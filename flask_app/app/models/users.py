from . import db
from flask import current_app
from app import db

from flask_login import UserMixin

class User(db.Model, UserMixin):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    
    @classmethod
    def last(self, cls):
        return(db.session.query(cls).order_by(cls.id.desc()).first())

    @classmethod
    def all(self, cls):
        return(db.session.query(cls).order_by(cls.id.desc()).all())
    
    @classmethod
    def get_by_name(self, cls, name):
        return db.session.query(cls).filter_by(name=name).first()
    