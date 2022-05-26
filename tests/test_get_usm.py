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

class USM:
    api_work = '/api/v2.0/add_usm_work?'
    api_rfid = '/api/v2.0/add_usm_rfid?'
    ip = 'http://127.0.0.1:5000'
    # ip = 'http://127.0.0.2'

    def __repr__(self):
        # return f'{self.number=}, {self.count=}, {self.lever=}, {self.roll=}, {self.lat=}, {self.lon=}'
        return f'{self.number=}, {self.count=}, {self.rfid=}, {self.flag=}'

    def __init__(self, mechanism_id, number, lever, roll, lat, lon):
        self.passw = post_passw[1]
        self.mechanism_id = mechanism_id
        self.number = number
        self.count = 0
        self.lever = lever
        self.roll = roll
        self.lat = lat
        self.lon = lon
        self.flag = 0
        self.rfid = '0'*10

    def send_req_work(self):
        params = {'number': self.number,
                  'passw': self.passw,
                  'count': self.count,
                  'lever': self.lever,
                  'roll': self.roll,
                  'rfid': self.rfid,
                  'flag': self.flag,
                  'lat': round(self.lat, 4),
                  'lon': round(self.lon, 4)}
        try:
            http = (self.ip+self.api_work)
            response = requests.get(http, params)
            response.raise_for_status()
            print(http, self.number, self.count, self.passw, self.lever,
                  self.roll, self.lat, self.lon)
        except HTTPError as http_err:
            print(f'HTTP error occurred -> {http_err}')
        except Exception as err:
            print(f'Other error occurred -> {err}')
        else:
            print('Success! ->', datetime.now())
        self.count += 1

    def send_req_rfid(self):
        params = {'number': self.number,
                  'passw': self.passw,
                  'count': self.count,
                  'rfid': self.rfid,
                  'flag': self.flag,
                  }
        try:
            http = (self.ip+self.api_rfid)
            response = requests.get(http, params)
            response.raise_for_status()
            print(http, self.number, self.rfid, self.flag) 
        except HTTPError as http_err:
            print(f'HTTP error occurred -> {http_err}')
        except Exception as err:
            print(f'Other error occurred -> {err}')
        else:
            print('Success! ->', datetime.now())
        self.count += 1

    def change_lever(self, value):
        self.lever = value

    def change_roll(self, value):
        self.roll = value

    def change_position(self, lat, lon):
        self.lat += lat
        self.lon += lon

    def change_flag(self, value=None):
        if value is None:
            self.flag = int(not bool(self.flag))
        else:
            self.flag = int(bool(value))

    def change_rfid(self, value):
        self.rfid = value 

    def get_position(self):
        return [self.lat, self.lon]

    def get_rfid(self):
        return self.rfid


if __name__ == "__main__":
    S5  = USM(mechanism_id=32770, number=5,  lever=0, roll=0,  lat=42.8118, lon=132.8893)
    S6  = USM(mechanism_id=32771, number=6,  lever=0, roll=0,  lat=42.8122, lon=132.8887)
    # S7  = USM(mechanism_id=32772, number=7,  lever=0, roll=0,  lat=0.0,     lon=0.0)
    S7  = USM(mechanism_id=32772, number=7,  lever=0, roll=0,  lat=42.8144, lon=132.8899)
    S8  = USM(mechanism_id=32773, number=8,  lever=0, roll=0,  lat=42.8171, lon=132.8926)
    U9  = USM(mechanism_id=32941, number=9,  lever=0, roll=0,  lat=42.8132, lon=132.8899)
    U10 = USM(mechanism_id=32942, number=10, lever=0, roll=0,  lat=42.8144, lon=132.8913)
    E11 = USM(mechanism_id=33287, number=11, lever=0, roll=0,  lat=42.8152, lon=132.8910)
    E12 = USM(mechanism_id=34213, number=12, lever=0, roll=0,  lat=42.8152, lon=132.8910)
    E13 = USM(mechanism_id=34214, number=13, lever=0, roll=0,  lat=42.8152, lon=132.8910)

    usms = S5,  S6,  S7,  S8, U9, #  U10, E11, E12, E13

    rfid_ids =   [ '0002419252',  '0015730188',  '0001006462' ]
    flagPosition = True
    lat = 0.0
    lon = 0.0
    last_sent = time.time() - 61
    [x.change_lever(0.4) for x in usms]
    [x.change_roll(20) for x in usms[:1]]
    
    counter = 0
    while True:
        time.sleep(1)
        if time.time() - last_sent >= 60.0:
            last_sent = time.time()
            # [m.change_position(lat, lon) for m in usms if m.get_position()[1] > 1] #! fuck
            if counter == 1: 
                [x.change_rfid(r) for x, r in zip(usms, rfid_ids)]
                [m.change_flag(1) for m in usms if m.get_rfid()!='0'*10]

                S5.send_req_rfid()
                S6.send_req_rfid()
                S7.send_req_rfid()
            if counter%3==0: 
                S6.change_flag()
            if counter%2==0: 
                S5.change_flag()
            # if flagPosition:
            #     lat = -0.0002
            #     lon = -0.0005
            # else:
            #     lat = 0.0002
            #     lon = 0.0004
            # flagPosition = not flagPosition
            [m.send_req_work() for m in usms]
            [print(x) for x in usms]
            counter += 1
