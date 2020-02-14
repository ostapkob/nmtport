# from run import db
from datetime import datetime, timedelta
from app import db
from app.model import USM, USM_data
from functions import today_shift_date, add_post

m_ids = 32046, 32047, 32711, 32740, 32770, 32771, 32772, 32773, 32941, 32942, 33287
for m_id in m_ids:
    post = USM_data(value=0.99, latitude=23, longitude=12, mechanism_id=m_id)
    db.session.add(post)
    db.session.commit()

# m_id = 32047
# now = datetime.utcnow() - timedelta(seconds=6200)
# p = USM_data(value=0.99, latitude=23, longitude=12, mechanism_id=m_id, timestamp=now)
# post = USM_data(value=0.99, latitude=23, longitude=12, mechanism_id=m_id) #, timestamp=now)
# last = db.session.query(USM_data).filter(USM_data.mechanism_id==post.mechanism_id).order_by(USM_data.timestamp.desc()).first()

# db.session.add(post)
# db.session.commit()

# add_post(post)



# date_shift, shift = today_shift_date()
# print('------------')
# data_per_shift = db.session.query(USM_data).filter(
#         USM_data.date_shift == date_shift, USM_data.shift == shift, USM_data.mechanism_id == m_id).all()
# for el in data_per_shift:
#     print(el.value, el.timestamp)



# start = db.session.query(USM_data.timestamp).filter(USM_data.mechanism_id == 32046).first()
# ss = db.session.query(USM_data).filter(USM_data.mechanism_id == 32046).order_by(USM_data.timestamp.desc()).first()
# print(start.value, start.timestamp)
# p1 = USM_data(body="post from john", author=u1, timestamp=now + timedelta(seconds=1))

# u = User(username='maloy', email='maloy888@yandex.ru')




# db.session.add(u)
# db.session.commit()

# print(User.query.all())
# print(User.query.filter_by(username='potap').first())

# c1 = Category(name='Python')
# c2 = Category(name='Linux')
# p = USM_data(title='ppperer', body='it work', category_id=1)
# p = USM_data(title='lin', body='yes')
# c1.posts.append(p)
# db.session.add(c2)
# print(User.query.all())
# p = USM_data(value=0.5, latitude=23, longitude=12, mechanism_id=32046) #, timestamp=dt)
# print(User.query.filter_by(username='potap').first())

# c1 = Category(name='Python')
# c2 = Category(name='Linux')
# p = USM_data(title='ppperer', body='it work', category_id=1)
# p = USM_data(title='lin', body='yes')
# c1.posts.append(p)
# db.session.add(c2)
# c1=Category.query.get(1)
# print(c1.posts)

# print(c1.posts)
# posts = USM_data.query.all()
# posts = USM.query.all()
# for p in posts:
    # db.session.delete(p)

# db.session.commit()
# query = Category.query.options(joinedload('posts'))
# for cat in query:
#     print(cat, cat.posts)

# print(USM_data.query.filter_by(category_id=2).first())
# obj = session.query(USM_data).order_by(USM_data.id.desc()).offset(1).first()
# p = USM_data.query.filter_by(id=1).id.desc().first()
# p =   USM_data.query.filter_by(mechanism_id=1).order_by(USM_data.id.desc()).limit(1)
# for i in p:
    # print(i.value, i.mechanism_id, sep=' | ')

# all_mech_id = [m.id for m in USM.query.all()]
# print(all_mech_id)
# db.session.add(p)
# db.session.commit()


# m1=Mechanism.query.get(1)
# pp = m1.posts
# for p in pp:
#     print(p)

# p1= USM_data.query.get(1)
# print(p1.mech.name)
# print(USM_data.query.all())
# print(datetime.date(datetime.now()))
# print(datetime.time(datetime.now()))



