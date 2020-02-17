# from run import db
from datetime import datetime, timedelta
from app import db
from app.model import Mechanism, Post
from functions import today_shift_date, add_post

m_ids = 32046, 32047, 32711, 32740, 32770, 32771, 32772, 32773, 32941, 32942, 33287, 32777,
for m_id in m_ids:
    post = Post(value=0.99, latitude=23, longitude=12, mechanism_id=m_id)
    db.session.add(post)
    db.session.commit()

# m_id = 32047
# now = datetime.utcnow() - timedelta(seconds=6200)
# p = Post(value=0.99, latitude=23, longitude=12, mechanism_id=m_id, timestamp=now)
# post = Post(value=0.99, latitude=23, longitude=12, mechanism_id=m_id) #, timestamp=now)
# last = db.session.query(Post).filter(Post.mechanism_id==post.mechanism_id).order_by(Post.timestamp.desc()).first()

# db.session.add(post)
# db.session.commit()

# add_post(post)



# date_shift, shift = today_shift_date()
# print('------------')
# data_per_shift = db.session.query(Post).filter(
#         Post.date_shift == date_shift, Post.shift == shift, Post.mechanism_id == m_id).all()
# for el in data_per_shift:
#     print(el.value, el.timestamp)



# start = db.session.query(Post.timestamp).filter(Post.mechanism_id == 32046).first()
# ss = db.session.query(Post).filter(Post.mechanism_id == 32046).order_by(Post.timestamp.desc()).first()
# print(start.value, start.timestamp)
# p1 = Post(body="post from john", author=u1, timestamp=now + timedelta(seconds=1))

# u = User(username='maloy', email='maloy888@yandex.ru')




# db.session.add(u)
# db.session.commit()

# print(User.query.all())
# print(User.query.filter_by(username='potap').first())

# c1 = Category(name='Python')
# c2 = Category(name='Linux')
# p = Post(title='ppperer', body='it work', category_id=1)
# p = Post(title='lin', body='yes')
# c1.posts.append(p)
# db.session.add(c2)
# print(User.query.all())
# p = Post(value=0.5, latitude=23, longitude=12, mechanism_id=32046) #, timestamp=dt)
# print(User.query.filter_by(username='potap').first())

# c1 = Category(name='Python')
# c2 = Category(name='Linux')
# p = Post(title='ppperer', body='it work', category_id=1)
# p = Post(title='lin', body='yes')
# c1.posts.append(p)
# db.session.add(c2)
# c1=Category.query.get(1)
# print(c1.posts)

# print(c1.posts)
# posts = Post.query.all()
# posts = Mechanism.query.all()
# for p in posts:
    # db.session.delete(p)

# db.session.commit()
# query = Category.query.options(joinedload('posts'))
# for cat in query:
#     print(cat, cat.posts)

# print(Post.query.filter_by(category_id=2).first())
# obj = session.query(Post).order_by(Post.id.desc()).offset(1).first()
# p = Post.query.filter_by(id=1).id.desc().first()
# p =   Post.query.filter_by(mechanism_id=1).order_by(Post.id.desc()).limit(1)
# for i in p:
    # print(i.value, i.mechanism_id, sep=' | ')

# all_mech_id = [m.id for m in Mechanism.query.all()]
# print(all_mech_id)
# db.session.add(p)
# db.session.commit()


# m1=Mechanism.query.get(1)
# pp = m1.posts
# for p in pp:
#     print(p)

# p1= Post.query.get(1)
# print(p1.mech.name)
# print(Post.query.all())
# print(datetime.date(datetime.now()))
# print(datetime.time(datetime.now()))



