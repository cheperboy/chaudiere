# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
from datetime import datetime, timedelta

from app import create_app, db
from app.models import Chaudiere, Wattbuffer

from app import create_app
app = create_app().app_context().push()


def createChaudiere(timestamp, temp0, temp1, watt0, watt1, watt2):
    try:
        entry = Chaudiere(timestamp, temp0, temp1, watt0, watt1, watt2)
        db.session.add(entry)
        db.session.commit()
        print entry
    except RuntimeError,e:
        print e.message

def createWattbuffer(timestamp, watt0, watt1, watt2):
    try:
        entry = Wattbuffer(timestamp, watt0, watt1, watt2)
        db.session.add(entry)
        db.session.commit()
        print entry
    except RuntimeError,e:
        print e.message

if __name__ == '__main__':
    createChaudiere()