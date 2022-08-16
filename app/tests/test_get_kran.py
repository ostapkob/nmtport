#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import time
from requests.exceptions import HTTPError
import requests
import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from psw import post_passw, debug
from rich import print

class Kran:
    api_work = '/api/v2.0/add_kran?'
    # api_rfid = '/api/v2.0/add_usm_rfid?'
    # ip = 'http://127.0.0.1:5000'
    ip = 'http://127.0.0.1'


    def __repr__(self):
        return f'{self.number=}, {self.value=}, {self.count=},  {self.lat=}, {self.lon=}, {self.x=}, {self.y=}'

    def __init__(self, number, value, x, y, lat, lon):
        self.passw = post_passw[1]
        # self.mechanism_id = mechanism_id
        self.number = number
        self.count = 0
        self.value = value
        self.lat = lat
        self.lon = lon
        self.x = x
        self.y = y
        # self.flag = 0
        # self.rfid = '0'*10

    def send_req_work(self):
        params = {'number': self.number,
                  'passw': self.passw,
                  'count': self.count,
                  'value': self.value,
                  # 'rfid': self.rfid,
                  # 'flag': self.flag,
                  'lat': round(self.lat, 4),
                  'lon': round(self.lon, 4),
                  'x': self.x,
                  'y': self.y,
                  }
        try:
            http = (self.ip+self.api_work)
            response = requests.get(http, params)
            response.raise_for_status()
            print(http, self.number, self.count, self.passw, self.value,
                  self.lat, self.lon, self.x, self.y )
        except HTTPError as http_err:
            print(f'HTTP error occurred -> {http_err}')
        except Exception as err:
            print(f'Other error occurred -> {err}')
        else:
            print('Success! ->', datetime.now())
        self.count += 1

    # def send_req_rfid(self):
    #     params = {'number': self.number,
    #               'passw': self.passw,
    #               'count': self.count,
    #               'rfid': self.rfid,
    #               'flag': self.flag,
    #               }
    #     try:
    #         http = (self.ip+self.api_rfid)
    #         response = requests.get(http, params)
    #         response.raise_for_status()
    #         print(http, self.number, self.rfid, self.flag) 
    #     except HTTPError as http_err:
    #         print(f'HTTP error occurred -> {http_err}')
    #     except Exception as err:
    #         print(f'Other error occurred -> {err}')
    #     else:
    #         print('Success! ->', datetime.now())

    def change_value(self, value):
        self.value = value

    def change_position(self, lat, lon):
        self.lat += lat
        self.lon += lon

    # def change_flag(self, value=None):
    #     if value is None:
    #         self.flag = int(not bool(self.flag))
    #     else:
    #         self.flag = int(bool(value))

    # def change_rfid(self, value):
    #     self.rfid = value 

    def get_position(self):
        return [self.lat, self.lon]

    # def get_rfid(self):
    #     return self.rfid


if __name__ == "__main__":
    k28 = Kran(number=28, value=0, x=1400, y=910,  lon=132.902908, lat=42.803509)
    k18 = Kran(number=18, value=0, x=1400, y=910,  lon=132.902708, lat=42.803409)
    k1  = Kran(number=1,  value=0, x=5001, y=910,  lon=132.903457, lat=42.806760)
    k35 = Kran(number=35, value=0, x=5001, y=910,  lon=132.903457, lat=42.806760)
    k31 = Kran(number=31, value=0, x=5001, y=910,  lon=132.903457, lat=42.806760)
    k17 = Kran(number=17, value=0, x=5001, y=910,  lon=132.903457, lat=42.806760)
    k58 = Kran(number=58, value=0, x=1400, y=910,  lon=132.902808, lat=42.803509)

    krans = k28, k18, k1, k35, k31, k17, k58
    lat = 0.0
    lon = 0.0
    last_sent = time.time() - 61
    [x.change_value(1) for x in krans[:5]]
    flagPosition = False
    counter = 0
    while True:
        time.sleep(1)
        if time.time() - last_sent >= 60.0:
            last_sent = time.time()
            [m.change_position(lat, lon) for m in krans if m.get_position()[1] > 1] #! fuck
            if counter%5==0: 
                [m.send_req_work() for m in krans[5:]]
            if flagPosition:
                lat = -0.0002
                lon = -0.0005
            else:
                lat = 0.0002
                lon = 0.0004
            flagPosition = not flagPosition
            [m.send_req_work() for m in krans[:5]]
            [print(x) for x in krans]
            counter += 1
