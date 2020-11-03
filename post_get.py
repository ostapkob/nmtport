import requests
from requests.exceptions import HTTPError
from psw import post_pass, debug
import time
from datetime import datetime


class Mechanism:
    # ip ='http://18.139.162.128'
    if debug:
        ip = 'http://127.0.0.1:5000'
    else:
        ip = 'https://m1.nmtport.ru'

    def __init__(self, mechanism_id, value, value2,
                 value3, count, latitude, longitude):
        self.mechanism_id = mechanism_id
        self.password = post_pass
        self.value = value
        self.value2 = value2
        self.value3 = value3
        self.latitude = latitude
        self.longitude = longitude
        self.count = count

    def send_get_request(self):
        params = {'mechanism_id': self.mechanism_id,
                  'password': self.password,
                  'value': self.value,
                  'value2': self.value2,
                  'value3': self.value3,
                  'count': self.count,
                  'latitude': round(self.latitude, 4),
                  'longitude': round(self.longitude, 4)}
        try:
            http = (self.ip+self.api)
            response = requests.get(http, params)
            response.raise_for_status()
            print(self.mechanism_id, http, self.password, self.value,
                  self.value2, self.value3, self.count,
                  self.latitude, self.longitude)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print('Success!', datetime.now())
        self.count += 1

    def chenge_value(self, value):
        self.value = value

    def chenge_value2(self, value):
        self.value2 = value

    def chenge_value3(self, value):
        self.value3 = value

    def chenge_position(self, lat, lng):
        self.latitude += lat
        self.longitude += lng


class USM(Mechanism):
    api = '/api/v1.0/add_get_usm?'

    def __repr__(self):
        return f'u{self.mechanism_id, self.password, self.value, self.value2, self.value3, self.count, self.latitude, self.longitude}'


class Kran(Mechanism):
    api = '/api/v1.0/add_get_kran?'

    def __repr__(self):
        return f'k{self.mechanism_id, self.password, self.value,self.value2, self.value3, self.count, self.latitude, self.longitude}'


if __name__ == "__main__":
    Pt1 = USM(mechanism_id=32046, value=0, value2=0, value3=0,
              count=0, latitude=42.8089, longitude=132.8865)
    Pt2 = USM(mechanism_id=32047, value=0, value2=0, value3=0,
              count=0, latitude=42.8082, longitude=132.8869)
    E3 = USM(mechanism_id=32711, value=0, value2=0, value3=0,
             count=0, latitude=42.8094, longitude=132.8878)
    E4 = USM(mechanism_id=32740, value=0, value2=0, value3=0,
             count=0, latitude=42.8106, longitude=132.8885)
    S5 = USM(mechanism_id=32770, value=0, value2=0, value3=0,
             count=0, latitude=42.8118, longitude=132.8893)
    S6 = USM(mechanism_id=32771, value=0, value2=0, value3=0,
             count=0, latitude=42.8122, longitude=132.8887)
    S7 = USM(mechanism_id=32772, value=0, value2=0, value3=0,
             count=0, latitude=42.8144, longitude=132.8899)
    S8 = USM(mechanism_id=32773, value=0, value2=0, value3=0,
             count=0, latitude=42.8171, longitude=132.8926)
    U9 = USM(mechanism_id=32941, value=0, value2=0, value3=0,
             count=0, latitude=42.8132, longitude=132.8899)
    U10 = USM(mechanism_id=32942, value=0, value2=0, value3=0,
              count=0, latitude=42.8144, longitude=132.8913)
    E11 = USM(mechanism_id=33287, value=0, value2=0, value3=0,
              count=0, latitude=42.8152, longitude=132.8910)
    kran4 = Kran(mechanism_id=30301, value=0, value2=0, value3=0,
                 count=0, latitude=42.8106, longitude=132.8880)
    kran12 = Kran(mechanism_id=13893, value=0, value2=0, value3=0,
                  count=0, latitude=42.8099, longitude=132.8884)
    kran13 = Kran(mechanism_id=15125, value=0, value2=0, value3=0,
                  count=0, latitude=42.8099, longitude=132.8884)
    kran22 = Kran(mechanism_id=5908,  value=0, value2=0, value3=0,
                  count=0, latitude=42.8088, longitude=132.8877)
    usms = Pt1, Pt2,  E4, S5,  S6,  S7,  S8, U9,  U10, E11
    usms = Pt1, Pt2,  E4,  S6,  S7  # ,  S8, U9,  U10, E11
    # usms= E3,  E4, S5,  S6,  S7,  S8, U9,  U10, E11
    # usms=Pt1, Pt2, S5,  S6,  S7,  S8, U9,  U10, E11
    krans = kran4, kran12, # kran13, kran22
    mechanisms = usms+krans

    flag = True
    lat = 0.0001
    lng = -0.0001
    last_sent = time.time() - 61
    [x.chenge_value(0) for x in usms[1::2]]
    [x.chenge_value(0.8) for x in usms[::2]]
    # Pt1.chenge_value(0.7)
    [x.chenge_value3(20) for x in usms]

    [print(x) for x in mechanisms]
    kran13.chenge_value(1)
    kran12.chenge_value(2)
    kran4.chenge_value(3)
    # Pt1.chenge_value(0)
    # Pt4.chenge_value(0)
    # n = 0
    while True:
        if time.time() - last_sent >= 70.0:
            last_sent = time.time()
            # n += 0.01
            # [x.chenge_value(n) for x in usms[::3]]
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
