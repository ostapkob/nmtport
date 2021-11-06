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

date = date(2021, 11, 2)
shift = 2
mech = 32770
# mech = 28369 # kran 58
# mech = 25390 # kran 1
# cursor = db.session.query(Post).filter(Post.mechanism_id == mech,
#                                        Post.date_shift == date, Post.shift == shift, Post.value == value)

db.session.query(Post)\
    .filter(Post.mechanism_id == mech, 
            Post.date_shift == date, 
            Post.shift == shift, 
            # Post.value == value,
            )\
    .update({"value": 0.7})

# db.session.query(Post).filter(
#     Post.mechanism_id == mech, 
#     Post.terminal == 13,
#     Post.date_shift == date,
#     Post.shift == shift
# ).update({"terminal": 15})

# cursor = db.session.query(Post).filter(
#     Post.mechanism_id == mech, 
#     Post.date_shift == date,
#     Post.shift == shift
# )

# for i in cursor:
#     print(i)

# cursor = db.session.query(Post).filter(
#     Post.mechanism_id == mech,
#     Post.date_shift == date,
    # Post.value > 0.3,
    # Post.value < 0.4,
    # Post.shift == shift,
   # )

# count = 0
# for i in cursor:
#     print(i)
#     count += 1

# db.session.query(Post)\
#     .filter(
#         Post.mechanism_id == mech,
#         Post.date_shift == date, 
#         Post.value > 0.2,
#         Post.value < 0.3,
#         Post.shift == shift
#     )\
#     .update({"value": 0.5})

# db.session.query(Post)\
#     .filter(
#         Post.mechanism_id == mech, 
#         Post.date_shift == date, 
#         Post.shift == shift
#     )\
#     .delete()
#=======================================================
# time_start  = datetime(2021, 11, 1, 22, 5, 0)
# time_finish = datetime(2021, 11, 1, 22, 7, 0)
# time = time_start

# lat=42.815608
# lon=132.892540
# x=409
# y=1048
# i = 0

# while time<time_finish:
#     i+=1
#     time+=timedelta(minutes=1)
#     if i%2==0: #frequency
#         continue
#     new_post = Post(
#                 timestamp=time-timedelta(hours=10),
#                 mechanism_id=mech, 
#                 value=1,
#                 value3=20,
#                 count=i,
#                 latitude=lat,
#                 longitude=lon,
#                 terminal=9,
#     )
#     db.session.add(new_post)
db.session.commit()
