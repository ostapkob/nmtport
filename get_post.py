from datetime import datetime, timedelta
from app import db
from functions import today_shift_date, all_mechanisms_id, in_hours, multiple_5
from app.model import Mechanism, Post
from pprint import pprint
db.create_all()
date_shift, shift = today_shift_date()

cursor = db.session.query(Post).filter(
    Post.date_shift == date_shift, Post.shift == shift).order_by(Post.mechanism_id).all()

data_per_shift = {}
for el in cursor:
    if data_per_shift.get(el.mech.name):
        data_per_shift[el.mech.name].append(el)
    else:
        data_per_shift[el.mech.name] = [el]

for key, values in data_per_shift.items():
    print(key, end=' : ')
    for val in values:
        print(val.value, multiple_5(val.timestamp),  end=" | ")
    print()

start = datetime.combine(date_shift, datetime.min.time())
if shift == 1:
    start=start.replace(hour=8, minute=0, second=0, microsecond=0)
else:
    start=start.replace(hour=20, minute=0, second=0, microsecond=0)
time_by_5_minut ={start:None}
for i in range(143):
    start+=timedelta(minutes=5)
    time_by_5_minut[start]=None

