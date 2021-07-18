#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import db
from app.model import Post
from datetime import date

date = date(2021, 7, 6)
shift = 1
value = 0 
mech =  32771 

cursor = db.session.query(Post).filter(Post.mechanism_id == mech,
                                       Post.date_shift == date, Post.shift == shift, Post.value == value)

# db.session.query(Post)\
#     .filter(Post.mechanism_id == mech, Post.date_shift == date, Post.shift == shift, Post.value == value)\
#     .update({"value": 2})

count = 0
for i in cursor:
    print(i)
    count += 1
print('--------------------------------')
print(count, 'items have been updated')

db.session.commit()
