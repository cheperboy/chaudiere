# -*- coding: utf-8 -*-
#from __future__ import absolute_import

import os, sys, click
from random import randint
from datetime import datetime, timedelta
from flask.cli import FlaskGroup

sys.path.append('..')
from app import create_app, db
from app.models import Teleinfo


def create_my_app(info):
    from app import create_app
    return create_app()

@click.group(cls=FlaskGroup, create_app=create_my_app)
def app():
    """This is a management script for the application."""

@app.command()
def create_db():
    """Recreate the db tables."""
    db.drop_all()
    db.create_all()
    db.session.commit()

@app.command()
def drop_db():
    """Drops the db tables."""
    db.drop_all()

@app.command()
@click.option('--base', default=666)
def create_data(base):
    """Creates a data Entry."""
    me = Teleinfo(datetime.now(), base=base)
    db.session.add(me)
    db.session.commit()
    print me


if __name__ == '__main__':
    app()