import requests
from requests.exceptions import HTTPError
from psw import post_pass
import time
from datetime import datetime

class Mechanism:
    def __init__(self, mechanism_id, value, latitude, longitude):
        self.mechanism_id= mechanism_id
        self.password=post_pass
        self.value=value
        self.latitude=latitude
        self.longitude=longitude
        self.ip ='http://127.0.0.1:5000/api/v1.0/add_get?'
        # self.ip ='http://35.241.126.216/api/v1.0/add_get?'

    def send_get_request(self):
        print(self.mechanism_id, self.password, self.value, self.latitude, self.longitude)
        params = {'mechanism_id': self.mechanism_id,
                 'password': self.password,
                 'value': self.value,
                 'latitude': round(self.latitude, 4),
                 'longitude':round(self.longitude, 4)}
        try:
            response = requests.get(self.ip, params)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!', datetime.now())

    def show(self):
        print(self.mechanism_id, self.password, self.value, self.latitude, self.longitude)

    def chenge_value(self, value):
        self.value=value

    def chenge_position(self, lat, lng ):
        self.latitude+=lat
        self.longitude+=lng

    def show(self):
        print(self.mechanism_id, self.password, self.value, self.latitude, self.longitude)

if __name__ == "__main__":
    Pt1=Mechanism(32046, 0,42.8089,132.8865)
    Pt2=Mechanism(32047, 0,42.8082,132.8869)
    E3 =Mechanism(32711, 0,42.8094,132.8878)
    E4 =Mechanism(32740, 0,42.8106,132.8885)
    S5 =Mechanism(32770, 0,42.8118,132.8893)
    S6 =Mechanism(32771, 0,42.8122,132.8887)
    S7 =Mechanism(32772, 0,42.8144,132.8899)
    S8 =Mechanism(32773, 0,42.8171,132.8926)
    U9 =Mechanism(32941, 0,42.8132,132.8899)
    U10 =Mechanism(32942, 0,42.8144,132.8913)
    E11 =Mechanism(33287, 0,42.8152,132.8910)
    Sen1 =Mechanism(32777, 0,42.8147,132.8913)
    # mechanisms=Pt1, Pt2, E3, E4, S5,  S6,  S7,  S8, U9,  U10, E11, Sen1
    mechanisms=Pt1,

    flag = True
    lat= 0.0001
    lng=-0.0001
    last_sent = time.time() - 61
    while True:
        if time.time() - last_sent >= 60.0:
            last_sent = time.time()
            [m.chenge_value(1) for m in mechanisms]
            # E3.chenge_value(0)
            E4.chenge_value(1)
            [m.chenge_position(lat, lng) for m in mechanisms]
            [m.send_get_request() for m in mechanisms]

            if flag:
                lat= 0.0001
                lng=-0.0001
                flag=False
            else:
                lat=-0.0001
                lng= 0.0001
                flag=True

