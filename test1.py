from sqlalchemy.orm import joinedload
# from run import db
from app import db

from app.model import Mechanism, Post
db.create_all()

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
# m = Mechanism(12, company='nmtp', type='usm', model='PowerTrack', number=12, name='PowerTrack13')
# p = Post(value=0.5, latitude=23, longitude=12, mechanism_id=1)
# db.session.add(p)
# db.session.commit()

# print(User.query.all())
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
# a = [mech.id for mech in Mechanism.query.all()]
# print(a)
# posts = Post.query.all()
# posts = Mechanism.query.all()
# for p in posts:
    # db.session.delete(p)

# db.session.commit()
# query = Category.query.options(joinedload('posts'))
# for cat in query:
#     print(cat, cat.posts)

# print(Post.query.filter_by(category_id=2).first())


all_mech_id = [m.id for m in Mechanism.query.all()]
print(all_mech_id)
# db.session.add(p)
# db.session.commit()
