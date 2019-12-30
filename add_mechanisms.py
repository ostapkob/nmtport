# from run import db
from datetime import datetime, timedelta
from app import db
from app.model import Mechanism, Post
# db.create_all()

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


m = Mechanism(32046, company='nmtp', type='usm', model='PowerTrack', number=1, name='PowerTrack-1')
db.session.add(m)
m = Mechanism(32047, company='nmtp', type='usm', model='PowerTrack', number=2, name='PowerTrack-2')
db.session.add(m)
m = Mechanism(32711, company='nmtp', type='usm', model='Edge', number=3, name='Edge-3')
db.session.add(m)
m = Mechanism(32740, company='nmtp', type='usm', model='Edge', number=4, name='Edge-4')
db.session.add(m)
m = Mechanism(32770, company='nmtp', type='usm', model='Screen', number=5, name='Screen-5')
db.session.add(m)
m = Mechanism(32771, company='nmtp', type='usm', model='Screen', number=6, name='Screen-6')
db.session.add(m)
m = Mechanism(32772, company='nmtp', type='usm', model='Screen', number=7, name='Screen-7')
db.session.add(m)
m = Mechanism(32773, company='nmtp', type='usm', model='Screen', number=8, name='Screen-8')
db.session.add(m)
m = Mechanism(32941, company='nmtp', type='usm', model='Electric', number=9, name='Electric-9')
db.session.add(m)
m = Mechanism(32942, company='nmtp', type='usm', model='Electric', number=10, name='Electric-10')
db.session.add(m)
m = Mechanism(33287, company='nmtp', type='usm', model='Edge', number=11, name='Edge-11')
db.session.add(m)
# m = Mechanism(32777, company='nmtp', type='sennebogen', model='860', number=1, name='Sennebogen-1')
# db.session.add(m)
db.session.commit()

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
a = [mech.id for mech in Mechanism.query.all()]
print(a)
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



