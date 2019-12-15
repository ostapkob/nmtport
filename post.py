from datetime import datetime, timedelta
import time
import requests
import json
from random import random, randint
import time


date = datetime.now()
dt = datetime.strftime(date,  "%d.%m.%Y  %H:%M")
# print(dt)
ids = 32046, 32047, 32711, 32740, 32770, 32771, 32772, 32773, 32941, 32942, 33287, 32777
host='http://127.0.0.1:5000/api/v1.0/add_post'
# host='http://35.241.126.216/api/v1.0/add_post'
data = {"password" : "super_pass",
        "value" : round(random(), 3),
        "latitude"  : 42.814722,
        "longitude" : 132.891338,
        "mechanism_id" : 1,
        }
head = {"Content-type": "application/json",
          "Accept": "text/plain"}
last_sent = time.time() - 61
while True:
    # print(time.time()- last_sent)
    if time.time() - last_sent > 60.0:
        last_sent = time.time()
        print(datetime.now())
        for i in range(0, 12, 1):
            data['mechanism_id'] =ids[i]
            # data['value']= round(random(), 2)
            data['value']= 1
            data['latitude'] = 42.8153 
            data['longitude'] = 132.8905 
            jdata = json.dumps(data)
            r = requests.post(host,data=jdata, headers=head)
            print(ids[i], r.status_code, r.reason, sep=' : ', end = " | ")
        # for i in range(1, 11, 2):]
        #     data['mechanism_id'] =ids[i]
        #     data['value']= 0.099 # round(random(),3)
        #     jdata = json.dumps(data)
        #     r = requests.post(host,data=jdata, headers=head)
        #     print(i, r.status_code, r.reason, sep=' : ', end = " | ")
        print()
