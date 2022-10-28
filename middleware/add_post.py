#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from app import db
from app.model import Post, Mechanism
from datetime import  datetime, timedelta
from middleware import  list_mechanisms
from  random import randint
kran = list_mechanisms.kran
usm = list_mechanisms.usm
mech = kran[22]

#=======================================================
time_start  = datetime(2022, 10, 26, 5, 0, 0)
time_finish = datetime(2022, 10, 26, 7, 27, 0)
time = time_start

lat=0
lon=0
i = 0

while time<time_finish:
    i+=1
    dt_min = 1+ randint(0,9)/10
    time+=timedelta(minutes=dt_min)
    new_post = Post(
                timestamp=time,
                mechanism_id= mech,
                value=2,
                value3=0,
                count=i,
                latitude=lat,
                longitude=lon,
                terminal=13,
    )
    db.session.add(new_post)
    print(new_post)
db.session.commit()
print('FINISH')
# # lat=42.815608
# # lon=132.892540
# # x=409
# # y=1048
