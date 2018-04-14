# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
from datetime import datetime, timedelta

from app import create_app, db
from app.models import Teleinfo

from app import create_app
app = create_app().app_context().push()


def createTeleinfo(timestamp, base, papp, iinst1, iinst2, iinst3):
    ret = 'NOK'
    try:
        entry = Teleinfo(timestamp, base, papp, iinst1, iinst2, iinst3)
        db.session.add(entry)
        db.session.commit()
        print entry
    except RuntimeError,e:
        print e.message


if __name__ == '__main__':
    createTeleinfo()