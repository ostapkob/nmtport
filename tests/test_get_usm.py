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

class USM:
    api_work = '/api/v2.0/add_usm_work?'
    api_rfid = '/api/v2.0/add_usm_rfid?'
    ip = 'http://127.0.0.1:5000'

    def __repr__(self):
        return f'u{self.number, self.passw, self.count, self.lever, self.roll, self.lat, self.lon}'

    def __init__(self, mechanism_id, number, count, lever, roll, lat, lon):
        self.passw = post_passw[1]
        self.mechanism_id = mechanism_id
        self.number = number
        self.count = count
        self.lever = lever
        self.roll = roll
        self.lat = lat
        self.lon = lon
        self.flag = 0
        self.rfid_id = 0

    def send_req_work(self):
        params = {'number': self.number,
                  'passw': self.passw,
                  'count': self.count,
                  'lever': self.lever,
                  'roll': self.roll,
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

    def send_req_rfid(self, rfid_id, flag):
        params = {'number': self.number,
                  'passw': self.passw,
                  'rfid': rfid_id,
                  'flag': flag,
                  }
        try:
            http = (self.ip+self.api_rfid)
            response = requests.get(http, params)
            response.raise_for_status()
            print(http, self.number, self.rfid_id, self.flag) 
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

    def change_flag(self):
        self.flag = not flag


if __name__ == "__main__":
    S5  = USM(mechanism_id=32770, number=5,  count=0, lever=0, roll=0,  lat=42.8118, lon=132.8893)
    S6  = USM(mechanism_id=32771, number=6,  count=0, lever=0, roll=0,  lat=42.8122, lon=132.8887)
    S7  = USM(mechanism_id=32772, number=7,  count=0, lever=0, roll=0,  lat=42.8144, lon=132.8899)
    S8  = USM(mechanism_id=32773, number=8,  count=0, lever=0, roll=0,  lat=42.8171, lon=132.8926)
    U9  = USM(mechanism_id=32941, number=9,  count=0, lever=0, roll=0,  lat=42.8132, lon=132.8899)
    U10 = USM(mechanism_id=32942, number=10, count=0, lever=0, roll=0,  lat=42.8144, lon=132.8913)
    E11 = USM(mechanism_id=33287, number=11, count=0, lever=0, roll=0,  lat=42.8152, lon=132.8910)
    E12 = USM(mechanism_id=34213, number=12, count=0, lever=0, roll=0,  lat=42.8152, lon=132.8910)
    E13 = USM(mechanism_id=34214, number=13, count=0, lever=0, roll=0,  lat=42.8152, lon=132.8910)

    usms = S5,  S6,  S7,  S8, U9, #  U10, E11, E12, E13
    rfid_ids = 2403, 17481, 17138, 20562, 2356, 17272, 17254, 11224, 1234

    rfid_ids =  '36,59956', '240,01548', '015,23422', '182,55028', '010,34767',
    rfid_ids =   [
        '0002419252', 
        '0015730188', 
        '0001006462', 
    ]

    flagMove = True
    lat = 0.0001
    lon = -0.0001
    last_sent = time.time() - 61
    [x.change_lever(0) for x in usms]
    [x.change_roll(0) for x in usms]
    [m.send_req_rfid(r, 1) for m, r in zip(usms, rfid_ids)]
    [print(x) for x in usms]

    # while True:
    #     if time.time() - last_sent >= 60.0:
    #         last_sent = time.time()
    #         time.sleep(1)
    #         [m.change_position(lat, lon) for m in usms]
    #         [m.send_req_work() for m in usms]
    #         if flagMove:
    #             lat = -0.0002
    #             lon = -0.0005
    #         else:
    #             lat = 0.0002
    #             lon = 0.0004
    #         flagMove = not flagMove
