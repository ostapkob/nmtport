import requests
from requests.exceptions import HTTPError
from psw import post_pass, debug
import time
from datetime import datetime


class Mechanism:
    if debug:
        ip = 'http://127.0.0.1:5000'
    else:
        # ip = 'http://127.0.0.1:5000'
        ip = 'http://94.154.76.136'

    def __init__(self, number, x, y, count, latitude, longitude):
        self.number = number
        self.password = post_pass
        self.x = x
        self.y = y
        self.latitude = latitude
        self.longitude = longitude
        self.count = count

    def send_get_request(self):
        params = {'number': self.number,
                  'password': self.password,
                  'x': self.x,
                  'y': self.y,
                  'count': self.count,
                  'latitude': round(self.latitude, 4),
                  'longitude': round(self.longitude, 4)}
        try:
            http = (self.ip+self.api)
            response = requests.get(http, params)
            response.raise_for_status()
            print(self.number, http, self.password, self.x,
                  self.y, self.count,
                  self.latitude, self.longitude)
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

    def chenge_position(self, lat, lng):
        self.latitude += lat
        self.longitude += lng


class Sennebogen(Mechanism):
    api = '/api/v1.0/add_sennebogen?'

    def __repr__(self):
        return f's{self.number, self.password, self.x, self.y, self.count, self.latitude, self.longitude}'

if __name__ == "__main__":
    S1 = Sennebogen(number=1, x=5001, y=910, count=0, latitude=42.8089, longitude=132.8865)
    S2 = Sennebogen(number=2, x=5002, y=10, count=0, latitude=42.8098, longitude=132.8841)
    S3 = Sennebogen(number=3, x=5003, y=1110, count=0, latitude=42.8089, longitude=132.8872)
    S4 = Sennebogen(number=4, x=5004, y=1110, count=0, latitude=42.8098, longitude=132.8865)
    S5 = Sennebogen(number=5, x=5005, y=410, count=0, latitude=42.80441, longitude=132.8855)
    S6 = Sennebogen(number=6, x=5006, y=1110, count=0, latitude=42.8078, longitude=132.8865)
    S7 = Sennebogen(number=7, x=5007, y=1110, count=0, latitude=42.8101, longitude=132.8855)
    S8 = Sennebogen(number=8, x=908, y=1110, count=0, latitude=42.8096, longitude=132.8859)
    S9 = Sennebogen(number=9, x=5009, y=1110, count=0, latitude=42.8083, longitude=132.8871)

    flag = True
    lat = 0.0001
    lng = -0.0001
    last_sent = time.time() - 61
    mechanisms = S1, S2, S3, S4, S5, S6, S7, S8, S9

    [print(x) for x in mechanisms]
    while True:
        if time.time() - last_sent >= 70.0:
            last_sent = time.time()
            [m.chenge_position(lat, lng) for m in mechanisms]
            [m.send_get_request() for m in mechanisms]
            if flag:
                lat = -0.0002
                lng = -0.0005
                flag = False
            else:
                lat = 0.0002
                lng = 0.0004
                flag = True
