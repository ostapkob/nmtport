from datetime import datetime, timedelta, timezone
from functions import shift_date, all_mechanisms_id
from app import db
from app.model import Post, Mechanism
from pprint import pprint
date_shift, shift = shift_date()
# hh =   db.session.query(Post.value, Post.mechanism_id).filter(Post.shift==1, Post.date_shift==date_shift, Post.value >0.6).order_by(Post.mechanism_id).offset(1)
# # print(hh)
# hours=[db.session.query(Post.value, Post.id).filter(Post.shift==shift, Post.date_shift==date_shift)]
# # hours=[db.session.query(Post).filter(Post.shift==1, Post.date_shift==date_shift, Post.value>=0.6).order_by(Post.mechanism_id).limit(3)]
# hours=[db.session.query(Post).filter(Post.shift==1, Post.date_shift==date_shift, Post.value>=0.6).order_by(Post.mechanism_id)]

# for hour in hours:
#     for h in hour:
#         print(h.value, h.mech.number, h.date_shift, h.shift, end=' | ')

# posts =   [Post.query.filter_by(mechanism_id=p).order_by(Post.id.desc()).limit(10) for p in all_mechanisms_id()]
# print(posts)

cursor = db.session.query(Post).filter(Post.date_shift==date_shift, Post.shift==shift).order_by(Post.mechanism_id).all()
print(cursor)
data_per_shift={}
for el in cursor:
    if data_per_shift.get(el.mech.id):
        data_per_shift[el.mech.id].append(el)
    else:
        data_per_shift[el.mech.id]=[el]

