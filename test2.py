from datetime import datetime, timedelta, timezone
from functions import shift_date
from app import db
from app.model import Post, Mechanism

date_shift, shift = shift_date()
hh =   db.session.query(Post.value, Post.mechanism_id).filter(Post.shift==1, Post.date_shift==date_shift, Post.value >0.6).order_by(Post.mechanism_id).offset(1)
# print(hh)
hours=[db.session.query(Post.value, Post.id).filter(Post.shift==shift, Post.date_shift==date_shift)]
# hours=[db.session.query(Post).filter(Post.shift==1, Post.date_shift==date_shift, Post.value>=0.6).order_by(Post.mechanism_id).limit(3)]
hours=[db.session.query(Post).filter(Post.shift==1, Post.date_shift==date_shift, Post.value>=0.6).order_by(Post.mechanism_id)]

for hour in hours:
    for h in hour:
        print(h.value, h.mech.number, h.date_shift, h.shift, end=' | ')

all_mech_id = [m.id for m in Mechanism.query.all()]
posts =   [Post.query.filter_by(mechanism_id=p).order_by(Post.id.desc()).limit(10) for p in all_mech_id]
print(posts)
x = db.session.query(Post.value, Mechanism.name).join(Mechanism).all()
print(len(x), x)
y = db.session.query(Post).filter(Post.date_shift==date_shift, Post.shift==shift).order_by(Post.mechanism_id).all()
yy = [(x.value, x.mech.name) for x in y]
print(len(yy), yy)

