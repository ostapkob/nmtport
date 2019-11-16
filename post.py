from datetime import datetime, timedelta
import requests
import json
from random import random

date = datetime.now()
dt = datetime.strftime(date,  "%d.%m.%Y  %H:%M")
# print(dt)

# host='http://127.0.0.1:5000/add_post'
host='http://35.241.126.216/add_post'
data = {"password" : "super",
        "value" : round(random(), 3),
        "latitude"  : 42.814723,
        "longitude" : 132.891339,
        "mechanism_id" : 2,
        }
head = {"Content-type": "application/json",
          "Accept": "text/plain"}

for i in range(1, 12, 2):
    data['mechanism_id'] =i
    data['value']= round(random(),3)
    jdata = json.dumps(data)
    r = requests.post(host,data=jdata, headers=head)
    print(i, r.status_code, r.reason, sep=' | ')

