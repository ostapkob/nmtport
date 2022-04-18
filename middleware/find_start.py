#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from app import db
from app.model import Post, Mechanism
from datetime import date, datetime, timedelta
from middleware import  list_mechanisms 
import pickle
from pprint import pp
from app.functions_for_all import *
import pandas as pd

TYPE = "kran"
HOURS = 10
all_mechs = all_mechanisms_id(TYPE)


def get_start(cursor, zone_start):
    mech_list = []
    time_list = []
    for i in cursor:
        type_mech = i.mech.type
        number = i.mech.number
        start = i.timestamp + timedelta(hours=HOURS)
        if type_mech == TYPE\
                and number not in mech_list\
                and i.terminal<16\
                and start<zone_start:
            # print(type_mech, number, start, i.value, i.terminal)
            mech_list.append(number)
            time_list.append(start)
    return time_list


def get_avr_time(time_start):
    assert time_start, "no items"
    print(time_start)
    mysum = timedelta()
    for i in time_start:
        h = i.hour
        m = i.minute
        mysum += timedelta(hours=int(h), minutes=int(m))
    return mysum/len(time_start)


if __name__ == "__main__":
    date_shift = date(2022, 4, 1)
    for shift in (1,1):
        start_shift = get_start_shift(date_shift, shift)
        start_shift_h = timedelta(hours=start_shift.hour)
        zone_start = start_shift + timedelta(hours=1, minutes=30)
        print(zone_start)

        cursor = db.session.query(Post).filter(
            Post.date_shift == date_shift,
            Post.shift == shift,
            # Post.value != 0,
            # Post.value !=4,
            Post.mechanism_id.in_(all_mechs)
        )
        # for i in cursor:
        #     print(i)
        df = pd.DataFrame(cursor)
        print(df)
        # time_start = get_start(cursor, zone_start)
        # dt = get_avr_time(time_start)
        # avg_time_start = (dt-start_shift_h)
        # print(date_shift, shift, avg_time_start)
