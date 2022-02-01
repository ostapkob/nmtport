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
date = date(2022, 1, 30)
shift = 2
mech = kran[10]
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
    # Post.value > 0.3,
    # Post.value < 0.4,
    # Post.shift == shift,
   # )

# count = 0
# for i in cursor:
#     print(i.timestamp, i.timestamp+delta)
#     count += 1

print(mech)
db.session.query(Post)\
    .filter(
        Post.mechanism_id ==33428,
        Post.date_shift == date, 
        Post.shift == shift,
        # Post.value == 1,
    )\
    .update({"terminal": 9})
    # .update({"value": Post.value*0.55})

# db.session.query(Post)\
    # .filter(
        # Post.mechanism_id == mech, 
        # Post.timestamp > datetime.now(),
        # Post.date_shift == date, 
        # Post.shift == shift
    # )\
    # .delete()
#=======================================================
# time_start  = datetime(2022, 1, 6, 5, 6, 0)
# time_finish = datetime(2022, 1, 6, 5, 24, 0)
# time = time_start

# lat=42.815608
# lon=132.892540
# x=409
# y=1048
# i = 0

# while time<time_finish:
#     i+=1
#     time+=timedelta(minutes=1)
    # if i%2!=0: #frequency
    #     continue
    # new_post = Post(
    #             timestamp=time-timedelta(hours=10),
    #             mechanism_id= mech,
    #             value=0.5,
    #             value3=20,
    #             count=i,
    #             latitude=lat,
    #             longitude=lon,
    #             terminal=13,
    # )
    # db.session.add(new_post)
db.session.commit()
print('FINISH')
