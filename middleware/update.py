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
from app.model import Post
from datetime import date

date = date(2021, 10, 5)
shift = 2
value = 3 
mech = 28369 # kran 58
mech = 25390 # kran 1
# cursor = db.session.query(Post).filter(Post.mechanism_id == mech,
#                                        Post.date_shift == date, Post.shift == shift, Post.value == value)

# db.session.query(Post)\
#     .filter(Post.mechanism_id == mech, Post.date_shift == date, Post.shift == shift, Post.value == value)\
#     .update({"value": 5})

# cursor = db.session.query(Post).filter(Post.terminal == 11,
#                                        Post.date_shift == date, Post.shift == shift)

cursor = db.session.query(Post).filter(Post.mechanism_id == mech,
                                       Post.date_shift == date,
                                       Post.shift == shift,
                                       )

count = 0
for i in cursor:
    print(i.terminal)
    count += 1

# db.session.query(Post)\
#     .filter(Post.terminal == 12, Post.date_shift == date, Post.shift == shift)\
#     .update({"terminal": 11})

db.session.query(Post)\
    .filter(Post.mechanism_id == mech, Post.date_shift == date, Post.shift == shift)\
    .delete()

print('--------------------------------')
print(count, 'items have been updated')

db.session.commit()
