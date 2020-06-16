from app import db
from app.model import Mechanism, User, generate_password_hash
db.create_all()

mech = [ (32046, 'nmtp', 'usm', 'PowerTrack', 1, 'PowerTrack-1'),
        (32047, 'nmtp', 'usm', 'PowerTrack', 2, 'PowerTrack-2'),
        (32711, 'nmtp', 'usm', 'Edge', 3, 'Edge-3'),
        (32740, 'nmtp', 'usm', 'Edge', 4, 'Edge-4'),
        (32770, 'nmtp', 'usm', 'Screen', 5, 'Screen-5'),
        (32771, 'nmtp', 'usm', 'Screen', 6, 'Screen-6'),
        (32772, 'nmtp', 'usm', 'Screen', 7, 'Screen-7'),
        (32773, 'nmtp', 'usm', 'Screen', 8, 'Screen-8'),
        (32941, 'nmtp', 'usm', 'Electric', 9, 'Electric-9'),
        (32942, 'nmtp', 'usm', 'Electric', 10, 'Electric-10'),
        (33287, 'nmtp', 'usm', 'Edge', 11, 'Edge-11'),
        (32777, 'nmtp', 'sennebogen', '860', 1, 'Sennebogen-1'),
        (30301, 'nmtp', 'kran', 'sokol', 4, 'кран-4'),
        (13893, 'nmtp', 'kran', 'sokol', 12, 'кран-12'),
        (5908,  'nmtp', 'kran', 'sokol', 22, 'кран-22'),
        ]


# for id, company, type, model, number, name in mech:
#     db.session.add(Mechanism(id, company, type, model, number, name))


users = [ (1, 'ostap', '1813'),
         (3, 'ya', '123'),
         (2, 'nmtp', 'port')]

for id, username, password in users:
    db.session.add(User(id, username, password))

# for p in User.query.all():
#     db.session.delete(p)

db.session.commit()

# m = Mechanism(32777, company='nmtp', type='sennebogen', model='860', number=1, name='Sennebogen-1')
a = [mech.id for mech in Mechanism.query.all()]
b = [(user.username, user.password_hash) for user in User.query.all()]
print(a)
print('---------------')
print(b)

