import requests
from requests.exceptions import HTTPError
from psw import post_pass
import time
from datetime import datetime

class Mechanism:
    def __init__(self, mechanism_id, value,value2, value3, latitude, longitude):
        self.mechanism_id= mechanism_id
        self.password=post_pass
        self.value=value
        self.value2=value2
        self.value3=value3
        self.latitude=latitude
        self.longitude=longitude
        # self.ip ='http://127.0.0.1:5000'
        self.ip ='http://18.139.162.128'
        self.api_usm ='/api/v1.0/add_get_usm?'
        self.api_kran ='/api/v1.0/add_get_kran?'
    def send_get_request(self):
        params = {'mechanism_id': self.mechanism_id,
                 'password': self.password,
                 'value': self.value,
                 # 'value2': self.value2,
                 'value3': self.value3,
                 'latitude': round(self.latitude, 4),
                 'longitude':round(self.longitude, 4)}
        try:
            http = (self.ip+self.api_usm)
            http = (self.ip+self.api_kran)
            response = requests.get(http, params)
            response.raise_for_status()
            print(self.mechanism_id, http, self.password, self.value, self.latitude, self.longitude)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print('Success!', datetime.now())

    def show(self):
        print(self.mechanism_id, self.password, self.value, self.latitude, self.longitude)

    def chenge_value(self, value):
        self.value=value

    def increase_value3(self):
        self.value3+=1

    def chenge_position(self, lat, lng ):
        self.latitude+=lat
        self.longitude+=lng

    def show(self):
        print(self.mechanism_id, self.password, self.value, self.latitude, self.longitude)

if __name__ == "__main__":
    Pt1=     Mechanism(mechanism_id=32046, value=0, value2=0, value3=0, latitude=42.8089, longitude=132.8865)
    Pt2=     Mechanism(mechanism_id=32047, value=0, value2=0, value3=0, latitude=42.8082, longitude=132.8869)
    E3 =     Mechanism(mechanism_id=32711, value=0, value2=0, value3=0, latitude=42.8094, longitude=132.8878)
    E4 =     Mechanism(mechanism_id=32740, value=0, value2=0, value3=0, latitude=42.8106, longitude=132.8885)
    S5 =     Mechanism(mechanism_id=32770, value=0, value2=0, value3=0, latitude=42.8118, longitude=132.8893)
    S6 =     Mechanism(mechanism_id=32771, value=0, value2=0, value3=0, latitude=42.8122, longitude=132.8887)
    S7 =     Mechanism(mechanism_id=32772, value=0, value2=0, value3=0, latitude=42.8144, longitude=132.8899)
    S8 =     Mechanism(mechanism_id=32773, value=0, value2=0, value3=0, latitude=42.8171, longitude=132.8926)
    U9 =     Mechanism(mechanism_id=32941, value=0, value2=0, value3=0, latitude=42.8132, longitude=132.8899)
    U10 =    Mechanism(mechanism_id=32942, value=0, value2=0, value3=0, latitude=42.8144, longitude=132.8913)
    E11 =    Mechanism(mechanism_id=33287, value=0, value2=0, value3=0, latitude=42.8152, longitude=132.8910)
    Sen1 =   Mechanism(mechanism_id=32777, value=0, value2=0, value3=0, latitude=42.8147, longitude=132.8913)
    kran4=   Mechanism(mechanism_id=30301, value=0, value2=0, value3=0, latitude=42.8140, longitude=132.8913)
    kran12=  Mechanism(mechanism_id=13893, value=0, value2=0, value3=0, latitude=42.8138, longitude=132.8914)
    kran22=  Mechanism(mechanism_id=5908,  value=0, value2=0, value3=0, latitude=42.8136, longitude=132.8912)
    #mechanisms=Pt1, Pt2, E3, S5,  S6,  S7,  S8, U9,  U10, E11, Sen1, kran4, kran12, kran22
    # mechanisms=Pt1, Pt2, E3, S5,  S6,  S7,  S8, U9,  U10, E11
    mechanisms=kran4, kran12, kran22

    flag = True
    lat= 0.0001
    lng=-0.0001
    last_sent = time.time() - 61
    while True:
        if time.time() - last_sent >= 60.0:
            last_sent = time.time()
            [m.chenge_value(0.5) for m in mechanisms]
            E3.chenge_value(0)
            kran4.chenge_value(1)
            kran12.chenge_value(1)
            kran22.chenge_value(2)

            [m.chenge_position(lat, lng) for m in mechanisms]
            [m.send_get_request() for m in mechanisms]
            [m.increase_value3() for m in mechanisms]
            if flag:
                lat= 0.0001
                lng=-0.0001
                flag=False
            else:
                lat=-0.0001
                lng= 0.0001
                flag=True

