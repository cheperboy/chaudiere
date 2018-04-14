# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os, click
from random import randint
from datetime import datetime, timedelta

from flask.cli import FlaskGroup

from app import create_app, db
from app.models import Teleinfo


def create_my_app(info):
    from app import create_app
    return create_app()

@click.group(cls=FlaskGroup, create_app=create_my_app)
def cli():
    """This is a management script for the application."""

@cli.command()
def create_db():
    """Recreate the db tables."""
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def drop_db():
    """Drops the db tables."""
    db.drop_all()

@cli.command()
def create_data():
    """Creates a data Entry."""
    me = Teleinfo(datetime.now())
    db.session.add(me)
    db.session.commit()
    print me


if __name__ == '__main__':
    cli()