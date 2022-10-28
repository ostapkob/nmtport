#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
from datetime import datetime, timedelta

from rich import print
from rich.console import Console
from rich.table import Table
console = Console()



table_usm2 = Table(title="USM2")
table_usm2.add_column("num", justify="right", style="green", no_wrap=True)
table_usm2.add_column("timestamp", justify="right", style="cyan", no_wrap=True)
table_usm2.add_column("count",    justify="right", style="green")
table_usm2.add_column("bad",    justify="right", style="yellow3")
table_usm2.add_column("dt",    justify="right", style="light_steel_blue")
table_usm2.add_column("lever",   justify="right", style="magenta")
table_usm2.add_column("roll",    justify="right", style="magenta")
table_usm2.add_column("rfid",    justify="right", style="blue")
table_usm2.add_column("flag",    justify="right", style="blue")
table_usm2.add_column("lat",      justify="right", style="green")
table_usm2.add_column("lon",      justify="right", style="green")


def is_int_or_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def test_items_usm(items):
    timestamp, number,  passw, count, lever, roll, rfid, flag, lat, lon = items
    test_nums =  number, lever, roll, count, lat, lon,  
    if not isinstance(timestamp, datetime):
        return False
    if not isinstance(passw, str):
        return False
    if not all([is_int_or_float(x) for x in test_nums]):
        return False
    return True

def test_items_usm2(items):
    num, passw, count, lever, roll, rfid, flag = items
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
    result={}
    for arg in args:
        parametr, value = arg.split('=')
        result[parametr]=value
    return result


def get_args():
    try:
        number_mech = sys.argv[1]
    except IndexError:
        print('No number')
        number_mech = 0 
    try:
        hour_start = int(sys.argv[3])
        time_start = datetime.now().replace(hour=hour_start, minute=59, second=0, microsecond=0)
    except IndexError:
        time_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    try:
        hour_finish = int(sys.argv[4])
        time_finish = datetime.now().replace(hour=hour_finish, minute=59, second=0, microsecond=0)
    except IndexError:
        time_finish = datetime.now()

    try:
        day_before = int(sys.argv[2])
        nginx_log = "/var/log/nginx/access.log.1"
    except IndexError:
        day_before = 0
        nginx_log = "/var/log/nginx/access.log"

    time_start -= timedelta(days=day_before)
    time_finish -= timedelta(days=day_before)
    return number_mech, nginx_log, time_start, time_finish


def main():
    number_mech, nginx_log, time_start, time_finish = get_args()
    with open(nginx_log) as f:
        lines = f.readlines()

    # nginx_log = "/var/log/nginx/access.log"

    print(nginx_log)
    print(time_start)
    print(time_finish)
    print("-----------------------------")
    num=0
    for line_file in lines:
        if 'add_usm_work?' in line_file:
            line = line_file.split('&')
            time = re.search(r'\[.*\]', line[0])[0]
            time = time[1:21]
            timestamp = datetime.strptime(time, '%d/%b/%Y:%H:%M:%S')
            parametrs = convert_reques_to_dict(line_file)

            if timestamp>time_start and timestamp<time_finish:
                number = parametrs.get('number', None)
                passw = parametrs.get('passw', None)
                count = parametrs.get('count', None)
                bad_count = parametrs.get('bad', None)
                lever = parametrs.get('lever', None)
                roll = parametrs.get('roll', None)
                rfid = parametrs.get('rfid', None)
                flag = parametrs.get('flag', None)
                lat = parametrs.get('lat', None)
                lon = parametrs.get('lon', None)
                if not number==number_mech: 
                    continue
                num+=1
                items = (num, passw,  count, lever, roll, rfid, flag )
                if not test_items_usm2(items):
                    print("Err USM v2.0 in", items)
                    continue
                try:
                    dt = round((timestamp - tmp_timestamp).total_seconds()/60, 1)
                except NameError:
                    dt = None
                tmp_timestamp = timestamp
                items_tab = (num, timestamp.time(), count, bad_count, dt, lever, roll, rfid, flag, lat, lon  )
                table_usm2.add_row(*[str(i) for i in items_tab])
    console.print(table_usm2)

if __name__=="__main__":
    main()
