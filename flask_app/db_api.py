# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
from datetime import datetime, timedelta

from app import create_app, db
from app.models import Chaudiere

from app import create_app
app = create_app().app_context().push()


def createSensorRecord(timestamp, temp0, temp1, temp2, watt0, watt1, watt2, watt3):
    try:
        entry = Chaudiere(timestamp, temp0, temp1, temp2, watt0, watt1, watt2, watt3, None, None, None)
        db.session.add(entry)
        db.session.commit()
    except RuntimeError,e:
        print e.message
        return False
    else:
        return True

if __name__ == '__main__':
    createChaudiere()