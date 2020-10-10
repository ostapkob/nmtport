from app import db
from app.model import Mechanism, User, generate_password_hash, Work_1C_1
from app.functions import today_shift_date
from psw import users
db.create_all()
from datetime import datetime, timedelta

mech = [(32046, 'nmtp', 'usm', 'PowerTrack', 1, 'PowerTrack-1'),
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
        (15125, 'nmtp', 'kran', 'sokol', 13, 'кран-13'),
        (5908,  'nmtp', 'kran', 'sokol', 22, 'кран-22'),
        ]


for id, company, type, model, number, name in mech:
    db.session.add(Mechanism(id, company, type, model, number, name))

for id, username, password in users:
    db.session.add(User(id, username, password))

# for p in User.query.all():
#     db.session.delete(p)

work_1c = [(2, 33287, 111, 5, 'Петров Ф. А.'),
      (1, 5908, 112, 8, 'Иванов Ф. А.')]

# for id, inv_num, greifer_num, greifer_vol, fio  in work_1c:
#     start = datetime.now() - timedelta(hours=5)
#     finish = datetime.now() + timedelta(hours=5)
#     date_shift, shift =  today_shift_date()
#     db.session.add(Work_1C_1(id, inv_num, greifer_num, greifer_vol, fio, start, finish, date_shift, shift))



db.session.commit()

# m = Mechanism(32777, company='nmtp', type='sennebogen', model='860', number=1, name='Sennebogen-1')
a = [mech.id for mech in Mechanism.query.all()]
print(a)
b = [(user.username, user.password_hash) for user in User.query.all()]
print('---------------')
print(b)

