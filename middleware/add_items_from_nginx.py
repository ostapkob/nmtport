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

from rich import print
from rich.console import Console
from rich.table import Table
HOURS = 10
console = Console()

table_kran = Table(title="Kran")
table_kran.add_column("timestamp", justify="right", style="cyan", no_wrap=True)
table_kran.add_column("number",   style="magenta")
table_kran.add_column("mech_id",  style="magenta")
table_kran.add_column("pass",     justify="right", style="green")
table_kran.add_column("value",    justify="right", style="blue")
table_kran.add_column("count",    justify="right", style="green")
table_kran.add_column("lat",      justify="right", style="blue")
table_kran.add_column("lon",      justify="right", style="green")
table_kran.add_column("x",        justify="right", style="blue")
table_kran.add_column("y",        justify="right", style="green")
table_kran.add_column("terminal", justify="right", style="blue")


table_usm = Table(title="USM")
table_usm.add_column("timestamp", justify="right", style="cyan", no_wrap=True)
table_usm.add_column("number",   style="magenta")
table_usm.add_column("mech_id",  style="magenta")
table_usm.add_column("pass",     justify="right", style="green")
table_usm.add_column("value",    justify="right", style="blue")
table_usm.add_column("value2",   justify="right", style="green")
table_usm.add_column("value3",   justify="right", style="blue")
table_usm.add_column("count",    justify="right", style="green")
table_usm.add_column("lat",      justify="right", style="blue")
table_usm.add_column("lon",      justify="right", style="green")
table_usm.add_column("terminal", justify="right", style="blue")

def is_int_or_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def test_items_kran(items):
    timestamp,number, mechanism_id, passw, value, count, lat, lon, x, y, terminal = items
    test_nums =  number, mechanism_id,  value, count, lat, lon, x, y, terminal 
    if not isinstance(timestamp, datetime):
        return False
    if not isinstance(passw, str):
        return False
    if not all([is_int_or_float(x) for x in test_nums]):
        return False
    return True

def test_items_usm(items):
    timestamp, number, mechanism_id, passw, value, value2, value3, count, lat, lon, terminal = items
    test_nums =  number, mechanism_id,  value, value2, value3, count, lat, lon, terminal 
    if not isinstance(timestamp, datetime):
        return False
    if not isinstance(passw, str):
        return False
    if not all([is_int_or_float(x) for x in test_nums]):
        return False
    return True


nginx_log = '/var/log/nginx/access.log'
with open(nginx_log) as f:
    lines = f.readlines()

time_start = datetime(2022, 7, 17, 19, 10, 0)
time_finish = datetime(2022, 7, 17, 19, 34, 0)
for line_file in lines:
    # if 'add_kran' in line_file:
    #     line = line_file.split('&')
    #     time = re.search(r'\[.*\]', line[0])[0]
    #     time = time[1:21]
    #     time = datetime.strptime(time, '%d/%b/%Y:%H:%M:%S')
    #     if time<time_start or time>time_finish:
    #         continue
    #     number = line[0].split('=')[1].strip()
    #     passw = line[1].split('=')[1].strip()
    #     value = line[2].split('=')[1].strip()
    #     count = line[3].split('=')[1].strip()
    #     lat = line[4].split('=')[1].strip()
    #     lon = line[5].split('=')[1].strip()
    #     x = line[6].split('=')[1].strip()
    #     y = line[7].split(' ')[0].split('=')[1].strip()
    #     mechanism_id = dict_mechanisms_id_by_number['kran'][int(number)]
    #     terminal = which_terminal('kran', number, lat, lon) 
    #     timestamp=time-timedelta(hours=HOURS)
    #     items = (timestamp,number, mechanism_id, passw, value, count, lat, lon, x, y, terminal)
    #     if not test_items_kran(items):
    #         print("Err kran in", items)
    #         continue
    #     table_kran.add_row(*[str(i) for i in items])
    #     new_post = Post(
    #                 timestamp=timestamp,
    #                 mechanism_id=mechanism_id, 
    #                 value=value,
    #                 count=count,
    #                 latitude=lat,
    #                 longitude=lon,
    #                 terminal=terminal,
    #     )
    #     db.session.add(new_post)
    if 'add_usm?' in line_file:
        line = line_file.split('&')
        time = re.search(r'\[.*\]', line[0])[0]
        time = time[1:21]
        time = datetime.strptime(time, '%d/%b/%Y:%H:%M:%S')
        if time<time_start or time>time_finish:
            continue
        mechanism_id = line[0].split('=')[1]
        try:
            number = dict_mechanisms_number_by_id['usm'][int(mechanism_id)]
        except KeyError:
            print("Not this number" )
            print(line_file)
            continue

        passw = line[1].split('=')[1]
        value = line[2].split('=')[1]
        value2 = line[3].split('=')[1]
        value3 = line[4].split('=')[1]
        count = line[5].split('=')[1]
        lat = line[6].split('=')[1]
        lon = line[7].split(' ')[0].split('=')[1]
        # if mechanism_id=='32942' and int(value3)>0:
        #     value=0.7
            
        terminal = which_terminal('usm', number, lat, lon) 
        timestamp=time-timedelta(hours=HOURS)

        items = (timestamp, number, mechanism_id, passw, value, value2, value3, count, lat, lon, terminal)
        if not test_items_usm(items):
            print("Err kran in", items,  style="red")
            continue

        table_usm.add_row(*[str(i) for i in items])
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
        db.session.add(new_post)

console.print(table_kran)
console.print(table_usm)



print('FINISH')
db.session.commit()
