from datetime import datetime, timedelta
import requests
import json
from random import random

print(random())
date = datetime.now()
dt = datetime.strftime(date,  "%d.%m.%Y  %H:%M")
print(dt)

host='http://127.0.0.1:5000/add_post'
data = {"password" : "super",
        "value" : round(random(), 3),
        "latitude"  : 42.814723,
        "longitude" : 132.891339,
        "mechanism_id" : 1,
        }
head = {"Content-type": "application/json",
          "Accept": "text/plain"}
jdata = json.dumps(data)
r = requests.post(host,data=jdata, headers=head)

print(r.text)
print(r.status_code, r.reason, sep=' | ')
