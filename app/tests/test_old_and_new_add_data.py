#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db, app, redis_client, mongodb_client
from app.model import Mechanism, Post
from datetime import datetime, timedelta
from app.functions import   mech_periods
from app.functions_for_all import *
from app.handlers import *
from app.usm import time_for_shift_usm, usm_periods
from app.kran import time_for_shift_kran, kran_periods
from app.sennebogen import time_for_shift_sennebogen, sennebogen_periods
from psw import post_passw
from config import HOURS
from rich import print
from app.add_fio_1c import add_fio_and_grab_from_1c
from app.add_fio_rfid import add_fio_from_rfid
from app.add_resons_1c import add_resons_from_1c

mongodb = mongodb_client.db
TYPE = 'usm'


if __name__ == "__main__":
    date_shift = datetime.now().date()
    date_shift -= timedelta(days=0)
    dates_shifts = [  date_shift - timedelta(days=x) for x in range(1, 2) ]
    shift = 2

    for date in dates_shifts:
        # data = mech_periods(TYPE, date, shift)
        name_file_pickle = TYPE+'_'+str(date)+"_"+str(shift)
        with open(name_file_pickle, 'rb') as f:
            data = pickle.load(f)
        data = add_fio_and_grab_from_1c(data, date, shift)
        data = add_fio_from_rfid(data, date, shift)
        data = add_resons_from_1c(data, date, shift)
        date_str = date.strftime("%d.%m.%Y")
        mongo_request = mongodb[TYPE].find_one( 
            {"_id": f"{date_str}|{shift}"})

        del mongo_request["_id"]
        mech = '11'
        key = 'rfid'
        # mk = mongo_request.keys()[0]
        # dk = data.keys()[0]
        # print(data[mech][key] )

