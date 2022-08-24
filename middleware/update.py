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
from datetime import date, datetime, timedelta
from middleware import  list_mechanisms 
kran = list_mechanisms.kran
usm = list_mechanisms.usm
date = date(2022, 8, 20)
shift = 2
mech = usm[11]
# cursor = db.session.query(Post).filter(Post.mechanism_id == mech,
#                                        Post.date_shift == date, Post.shift == shift, Post.value == value)
# delta = timedelta(seconds=1)
# db.session.query(Post)\
#     .filter(Post.mechanism_id == mech, 
#             Post.date_shift == date, 
#             Post.shift == shift, 
#             # Post.id==2046832,
#             Post.value == 1,
#             )\
#     .update({
#         "value": 2
        # "timestamp": Post.timestamp + delta,
    # })

# db.session.query(Post).filter(
#     Post.mechanism_id == mech, 
#     Post.terminal == 78,
#     Post.date_shift == date,
#     Post.shift == shift
# ).update({"terminal": 76})

# cursor = db.session.query(Post).filter(
    # Post.mechanism_id == mech, 
    # Post.timestamp > datetime.now(),
    # Post.shift == shift
# )

# for i in cursor:
#     print(i.value, i.timestamp)

# cursor = db.session.query(Post).filter(
#     Post.mechanism_id == mech,
#     Post.date_shift == date,
#     Post.shift == shift,
    # Post.value > 0.3,
   # )

# for i in cursor:
   #  print(i.timestamp, i.value, i.value3)

# print(mech)
# db.session.query(Post)\
#     .filter(
#         Post.mechanism_id == mech,
#         Post.date_shift == date, 
#         Post.shift == shift,
#         Post.value == 2
#     )\
#     .update({"value": 1})
    # .update({"value": Post.value*0.55})

# print(mech)
# db.session.query(Post)\
#     .filter(
#         Post.mechanism_id == mech,
#         Post.date_shift == date, 
#         Post.shift == shift,
#         Post.value <=0.5

#     )\
#     .update({"value": 0.55})
    # .update({"value": Post.value*0.55})


        # Post.timestamp > datetime.now(),

db.session.query(Post)\
    .filter(
        Post.mechanism_id == mech, 
        Post.date_shift == date, 
        Post.shift == shift
    )\
    .delete()



#=======================================================
# time_start  = datetime(2022, 7, 23, 13, 17, 0)
# time_finish = datetime(2022, 7, 23, 16, 30, 0)
# time = time_start

# # lat=42.815608
# # lon=132.892540
# lat=0
# lon=0
# # x=409
# # y=1048
# i = 0

# while time<time_finish:
#     i+=1
#     time+=timedelta(minutes=1)
#     if not i%3!=0: #frequency
#         continue
#     new_post = Post(
#                 timestamp=time-timedelta(hours=10),
#                 mechanism_id= mech,
#                 value=2,
#                 value3=20,
#                 count=i,
#                 latitude=lat,
#                 longitude=lon,
#                 terminal=13,
#     )
#     db.session.add(new_post)
#     print(new_post)
db.session.commit()
print('FINISH')
