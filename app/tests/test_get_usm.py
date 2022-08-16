import sys
sys.path.insert(0, '/home/admin/nmtport')
import os
import requests
from requests.exceptions import HTTPError
import time
from rich import print
from psw import post_passw
from app.functions_for_all import id_by_number

from typing import Literal
# current_dir = os.path.dirname(os.path.abspath(
#     inspect.getfile(inspect.currentframe())))
# parent_dir = os.path.dirname(current_dir)


class USM:
    api_work = '/api/v2.0/add_usm_work?'
    api_rfid = '/api/v2.0/add_usm_rfid?'
    type_mech:str = 'usm'
    address: str
    passw: str
    number: int
    count: int
    lever: float
    roll:int
    lat: float
    lon: float
    flag: int
    rfid: str

    def __repr__(self):
        return f'{self.number=}, {self.count=}, {self.rfid=}, {self.flag=}'

    def __init__(self,  number, passw='superpass', lever=0, roll=0, lat=0, lon=0, ip='127.0.0.1', port=5000):
        self.address = 'http://' + ip + ":" + str(port)
        self.passw = passw
        self.number = number
        self.count = -1
        self.lever = lever
        self.roll = roll
        self.lat = lat
        self.lon = lon
        self.flag = 0
        self.rfid = '0' * 10
        self.mech_id = id_by_number(self.type_mech, self.number)

    def send_req_work(self) -> bool:
        self.count += 1
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
            http = self.address + self.api_work
            response = requests.get(http, params)
            response.raise_for_status()
            # print(http, self.number, self.count, self.passw, self.lever,
            #       self.roll, self.lat, self.lon)
        except HTTPError as http_err:
            print(f'HTTP error occurred -> {http_err}')
            return False
        except Exception as err:
            print(f'Other error occurred -> {err}')
            return False
        else:
            # print('Success! ->', datetime.now())
            return True

    def send_req_rfid(self) -> bool:
        params = {'number': self.number,
                  'passw': self.passw,
                  'count': self.count,
                  'rfid': self.rfid,
                  'flag': self.flag,
                  }
        http = (self.address + self.api_rfid)
        print(http)
        try:
            http = (self.address + self.api_rfid)
            response = requests.get(http, params)
            print(response)
            response.raise_for_status()
            print(http, self.number, self.rfid, self.flag)
        except HTTPError as http_err:
            print(f'HTTP error occurred -> {http_err}')
            return False
        except Exception as err:
            print(f'Other error occurred -> {err}')
            return False
        else:
            print('Success!')
            return True

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

    def change_passw(self, value):
        self.passw = value

    def change_number(self, value):
        self.number = value

    def get_position(self):
        return [self.lat, self.lon]

    def get_rfid(self):
        return self.rfid


        # self.passw = post_passw[1]
if __name__ == "__main__":
    S5 = USM( number=5, passw=post_passw[1], lever=0,
             roll=0,  lat=42.8118, lon=132.8893)
    S6 = USM( number=6, passw=post_passw[1], lever=0,
             roll=0,  lat=42.8122, lon=132.8887)
    S7 = USM( number=7, passw=post_passw[1], lever=0,
             roll=0,  lat=0.0,     lon=0.0)
    # S7  = USM( number=7,  lever=0, roll=0,  lat=42.8144, lon=132.8899)
    S8 = USM( number=8, passw=post_passw[1], lever=0,
             roll=0,  lat=42.8171, lon=132.8926)
    U9 = USM( number=9, passw=post_passw[1], lever=0,
             roll=0,  lat=42.8132, lon=132.8899)
    U10 = USM( number=10, passw=post_passw[1], lever=0,
              roll=0,  lat=42.8144, lon=132.8913)
    E11 = USM( number=11, passw=post_passw[1], lever=0,
              roll=0,  lat=42.8152, lon=132.8910)
    E12 = USM( number=12, passw=post_passw[1], lever=0,
              roll=0,  lat=42.8152, lon=132.8910)
    E13 = USM( number=13, passw=post_passw[1], lever=0,
              roll=0,  lat=42.8152, lon=132.8910)

    usms = S5,  S6,  S7,  S8, U9,  # U10, E11, E12, E13

    rfid_ids = ['0002419252',  '0015730188',  '0001006462']
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
            [m.change_position(lat, lon)
             for m in usms if m.get_position()[1] > 1]  # ! fuck
            if counter == 1:
                break
                [x.change_rfid(r) for x, r in zip(usms, rfid_ids)]
                [m.change_flag(1) for m in usms if m.get_rfid() != '0'*10]
                S5.send_req_rfid()
                S6.send_req_rfid()
                S7.send_req_rfid()
            if counter % 5 == 0:
                S6.change_flag()
                S6.send_req_rfid()
            if flagPosition:
                lat = -0.0002
                lon = -0.0005
            else:
                lat = 0.0002
                lon = 0.0004
            flagPosition = not flagPosition
            [m.send_req_work() for m in usms]
            [print(x) for x in usms]
            counter += 1
