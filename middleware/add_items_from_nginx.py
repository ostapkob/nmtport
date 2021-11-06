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
from app.model import Post
import re
from datetime import datetime, timedelta
from app.functions import  get_dict_mechanisms_id_by_number, get_dict_mechanisms_number_by_id
from app.functions import which_terminal, mech_periods
dict_mechanisms_id_by_number = get_dict_mechanisms_id_by_number()
dict_mechanisms_number_by_id = get_dict_mechanisms_number_by_id()

nginx_log = '/var/log/nginx/access.log'
with open(nginx_log) as f:
    lines = f.readlines()

time_start = datetime(2021, 11, 2, 1, 1, 0)
time_finish = datetime(2021, 11, 2, 1, 2, 0)
for line in lines:
    # if 'add_kran' in line:
    #     line = line.split('&')
    #     time = re.search(r'\[.*\]', line[0])[0]
    #     time = time[1:21]
    #     time = datetime.strptime(time, '%d/%b/%Y:%H:%M:%S')
    #     if time<time_start or time>time_finish:
    #         continue
    #     number = line[0].split('=')[1]
    #     passw = line[1].split('=')[1]
    #     value = line[2].split('=')[1]
    #     count = line[3].split('=')[1]
    #     lat = line[4].split('=')[1]
    #     lon = line[5].split('=')[1]
    #     x = line[6].split('=')[1]
    #     y = line[7].split(' ')[0].split('=')[1]
    #     mechanism_id = dict_mechanisms_id_by_number['kran'][int(number)]
    #     terminal = which_terminal('kran', number, lat, lon) 
    #     timestamp=time-timedelta(hours=10)
        # print(timestamp,number, mechanism_id, passw, value, count, lat, lon, x, y, terminal)
        # new_post = Post(
        #             timestamp=timestamp,
        #             mechanism_id=mechanism_id, 
        #             value=value,
        #             count=count,
        #             latitude=lat,
        #             longitude=lon,
        #             terminal=terminal,
        # )
        # db.session.add(new_post)
    if 'add_usm' in line:
        line = line.split('&')
        time = re.search(r'\[.*\]', line[0])[0]
        time = time[1:21]
        time = datetime.strptime(time, '%d/%b/%Y:%H:%M:%S')
        if time<time_start or time>time_finish:
            continue
        mechanism_id = line[0].split('=')[1]
        number = dict_mechanisms_number_by_id['usm'][int(mechanism_id)]
        passw = line[1].split('=')[1]
        value = line[2].split('=')[1]
        value2 = line[3].split('=')[1]
        value3 = line[4].split('=')[1]
        count = line[5].split('=')[1]
        lat = line[6].split('=')[1]
        lon = line[7].split(' ')[0].split('=')[1]
        terminal = which_terminal('usm', number, lat, lon) 
        timestamp=time-timedelta(hours=10)
        new_post = Post(
                    timestamp=timestamp,
                    mechanism_id=mechanism_id, 
                    value=value,
                    value2=value2,
                    value3=value3,
                    count=count,
                    latitude=lat,
                    longitude=lon,
                    terminal=terminal,
        )
        if mechanism_id!='34214':
            continue
        print(timestamp,number, mechanism_id, value, value2, value3, count, lat, lon, terminal)
        # db.session.add(new_post)
# db.session.commit()
# print('FINISH')
