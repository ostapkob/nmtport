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
from psw import post_pass, debug

pasw = post_pass[2]

class Mechanism:
    if debug:
        ip = 'http://127.0.0.1:5000'
    else:
        ip = 'http://127.0.0.1:5000'
        # ip = 'http://94.154.76.136'

    def __init__(self, number, value, count, x, y, lat, lon):
        self.number = number
        self.value = value,
        self.password = pasw
        self.x = x
        self.y = y
        self.lat = lat
        self.lon = lon
        self.count = count

    def send_get_request(self):
        params = {'number': self.number,
                  'passw': self.password,
                  'value': self.value,
                  'x': self.x,
                  'y': self.y,
                  'count': self.count,
                  'lat': round(self.lat, 6),
                  'lon': round(self.lon, 6)}
        try:
            http = (self.ip+self.api)
            response = requests.get(http, params)
            response.raise_for_status()
            print(self.number, http, self.password, 
                  self.value, self.count,
                  self.x, self.y, 
                  self.lat, self.lon)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print('Success!', datetime.now())
        self.count += 1

    def chenge_x(self, x):
        self.x = x

    def chenge_y(self, y):
        self.y = y

    def chenge_position(self, lat, lon):
        self.lat += lat
        self.lon += lon


class Sennebogen(Mechanism):
    api = '/api/v1.0/add_sennebogen?'

    def __repr__(self):
        return f's{self.number, self.password, self.x, self.y, self.count, self.lat, self.lon}'

class Kran(Mechanism):
    api = '/api/v2.0/add_kran?'

    def __repr__(self):
        return f's{self.number, self.password, self.x, self.y, self.count, self.lat, self.lon}'


if __name__ == "__main__":
    # S1 = Sennebogen(number=1, x=5001, y=910, count=0,
    #                 lat=42.8089, lon=132.8865)
    # S2 = Sennebogen(number=2, x=5002, y=10, count=0,
    #                 lat=42.8098, lon=132.8841)
    # S3 = Sennebogen(number=3, x=5003, y=1110, count=0,
    #                 lat=42.8089, lon=132.8872)
    # S4 = Sennebogen(number=4, x=5004, y=1110, count=0,
    #                 lat=42.8098, lon=132.8865)
    # S5 = Sennebogen(number=5, x=5005, y=410, count=0,
    #                 lat=42.80441, lon=132.8855)
    # S6 = Sennebogen(number=6, x=5006, y=1110, count=0,
    #                 lat=42.8078, lon=132.8865)
    # S7 = Sennebogen(number=7, x=5007, y=1110, count=0,
    #                 lat=42.8101, lon=132.8855)
    # S8 = Sennebogen(number=8, x=908, y=1110, count=0,
    #                 lat=42.8096, lon=132.8859)
    # S9 = Sennebogen(number=9, x=5009, y=1110, count=0,
    #                 lat=42.8083, lon=132.8871)

    k22 = Kran(number=22,  value=0,  count=0, x=0, y=0,
               lat=42.809935859, lon=132.8883382114 )

    k14 = Kran(number=14,  value=0,  count=0, x=0, y=0,
               lon = 132.8884068900412, lat=42.81000536341068)

    k28 = Kran(number=28, value=0, x=1400, y=910, count=0,
                lon=132.90290816212828, lat=42.803509357113114)

    k18 = Kran(number=18, value=0, x=1400, y=910, count=0,
                    lon=132.90270816212828, lat=42.803409357113114)

    k1 = Kran(number=1, value=0, x=5001, y=910, count=0,
                    lon=132.9034574490496, lat=42.80676015655138)

    k35 = Kran(number=35, value=0, x=5001, y=910, count=0,
                    lon=132.9034574490496, lat=42.80676015655138)

    k31 = Kran(number=31, value=0, x=5001, y=910, count=0,
                    lon=132.9034574490496, lat=42.80676015655138)

    k17 = Kran(number=17, value=0, x=5001, y=910, count=0,
                    lon=132.9034574490496, lat=42.80676015655138)

    k58 = Kran(number=58, value=0, x=1400, y=910, count=0,
                    lon=132.90280816212828, lat=42.803509357113114)



    flag = True
    lat = 0.0001
    lon = -0.0001
    last_sent = time.time() - 61
    # mechanisms = S1, S2, S3, S4, S5, S6, S7, S8, S9
    mechanisms = k28, k18, k1, k35, k31, k17

    [print(x) for x in mechanisms]
    while True:
        if time.time() - last_sent >= 61.0:
            last_sent = time.time()
            [m.chenge_position(lat, lon) for m in mechanisms]
            [m.send_get_request() for m in mechanisms]
            if flag:
                lat = -0.0002
                lon = -0.0005
                flag = False
            else:
                lat = 0.0002
                lon = 0.0004
                flag = True

