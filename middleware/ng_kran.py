#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
from datetime import datetime

from rich import print
from rich.console import Console
from rich.table import Table
console = Console()
nginx_log = '/var/log/nginx/access.log'


table_kran2 = Table(title="KRAN-2")
table_kran2.add_column("num", justify="right", style="green", no_wrap=True)
table_kran2.add_column("timestamp", justify="right", style="cyan", no_wrap=True)
table_kran2.add_column("count",    justify="right", style="green")
table_kran2.add_column("bad",    justify="right", style="yellow3")
table_kran2.add_column("dt",    justify="right", style="light_steel_blue")
table_kran2.add_column("value",   justify="right", style="magenta")
table_kran2.add_column("lat",    justify="right", style="blue")
table_kran2.add_column("lon",    justify="right", style="blue")
table_kran2.add_column("x",    justify="right", style="green")
table_kran2.add_column("y",    justify="right", style="green")

def is_int_or_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def test_items_kran(items):
    number,  timestamp, passw, count, bad_count, value, lat, lon, x, y = items
    test_nums =  number, value, count,  lat, lon,  x, y
    # if not isinstance(timestamp, datetime):
    #     return False
    if not isinstance(passw, str):
        return False
    if not all([is_int_or_float(x) for x in test_nums]):
        return False
    return True

def test_items_kran2(items):
    number,  timestamp, passw, count, value, lat, lon, x, y = items
    test_nums =  lever, roll, count   
    if not isinstance(passw, str):
        return False
    if not all([is_int_or_float(x) for x in test_nums]):
        return False
    return True

def convert_reques_to_dict(req):
    req = req.split('?')[1]
    req = req.split(' ')[0]
    args = req.split('&')
    # time = re.search(r'\[.*\]', line[0])[0]
    # time = time[1:21]
    # timestamp = datetime.strptime(time, '%d/%b/%Y:%H:%M:%S')
    result={}
    for arg in args:
        parametr, value = arg.split('=')
        result[parametr]=value
    return result

# def get_time_start_finish():
#     try:
#         hour_start = int(sys.argv[2])
#         time_start = datetime.now().replace(hour=hour_start, minute=0, second=0, microsecond=0)
#     except IndexError:
#         time_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
#     try:
#         hour_finish = int(sys.argv[3])
#         time_finish = datetime.now().replace(hour=hour_finish, minute=0, second=0, microsecond=0)
#     except IndexError:
#         time_finish = datetime.now()

#     return time_start, time_finish

def get_args():
    try:
        number_mech = sys.argv[1]
    except IndexError:
        print('No number')
        number_mech = 0 
    try:
        hour_start = int(sys.argv[2])
        time_start = datetime.now().replace(hour=hour_start, minute=0, second=0, microsecond=0)
    except IndexError:
        time_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    try:
        hour_finish = int(sys.argv[3])
        time_finish = datetime.now().replace(hour=hour_finish, minute=0, second=0, microsecond=0)
    except IndexError:
        time_finish = datetime.now()

    return number_mech, time_start, time_finish


def main():
    with open(nginx_log) as f:
        lines = f.readlines()
    try:
        number_mech = sys.argv[1]
    except IndexError:
        print('No number')
        number_mech = 0 
    number_mech, time_start, time_finish = get_args()

    print(time_start)
    print(time_finish)
    print("-----------------------------")
    num=0
    for line_file in lines:
        if 'add_kran?' in line_file:
            line = line_file.split('&')
            time = re.search(r'\[.*\]', line[0])[0]
            time = time[1:21]
            timestamp = datetime.strptime(time, '%d/%b/%Y:%H:%M:%S')
            parametrs = convert_reques_to_dict(line_file)

            if timestamp>time_start and timestamp<time_finish:
                number = parametrs.get('number', None)
                passw = parametrs.get('passw', None)
                value = parametrs.get('value', None)
                count = parametrs.get('count', None)
                bad_count = parametrs.get('bad', None)
                lat = parametrs.get('lat', None)
                lon = parametrs.get('lon', None)
                x = parametrs.get('x', None)
                y = parametrs.get('y', None)
                if not number==number_mech: 
                    continue
                num+=1
                items = (num, timestamp.time(), passw, count, bad_count, value, lat, lon, x, y )
                
                if not test_items_kran(items):
                    print("Err USM v2.0 in", items)
                    continue
                try:
                    dt = round((timestamp - tmp_timestamp).total_seconds()/60, 1)
                except NameError:
                    dt = None
                tmp_timestamp = timestamp
                items_tab = (num, timestamp.time(), count, bad_count, dt, value, lat, lon, x, y )
                table_kran2.add_row(*[str(i) for i in items_tab])
    console.print(table_kran2)

if __name__=='__main__':
    main()
