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
    except OperationalError as e:
        print ("OperationalError " + str(e.message))
        return False
    except Error as e:
        print ("generic Error" + str(e.message))
        return False
    else:
        return True
