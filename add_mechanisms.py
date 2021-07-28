from datetime import datetime, timedelta
from app.functions import today_shift_date
from app.model import Mechanism, User, generate_password_hash, Work_1C_1
from app import db
import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
db.create_all()
from psw import users

mech = [
    # (22272, 'nmtp', 'kran', 'sokol', 36, 'кран-36'),
    # (22152, 'nmtp', 'kran', 'sokol', 40, 'кран-40'),
    # (13969, 'nmtp', 'kran', 'sokol', 32, 'кран-32'),
    # (6573,  'nmtp', 'kran', 'albatross', 25, 'кран-25'),
    # (14194, 'nmtp', 'kran', 'sokol', 11, 'кран-11'),
    # (15512, 'nmtp', 'kran', 'sokol', 14, 'кран-14'),
    # (15510, 'nmtp', 'kran', 'sokol', 16, 'кран-16'),
    # (15511, 'nmtp', 'kran', 'sokol', 33, 'кран-33'),
    # (4513,  'nmtp', 'kran', 'sokol', 47, 'кран-47'),
    # (30271, 'nmtp', 'kran', 'sokol', 54, 'кран-54'),
    # (30301, 'nmtp', 'kran', 'sokol', 4, 'кран-4'),
    # (14195, 'nmtp', 'kran', 'sokol', 8, 'кран-8'),
    # (13893, 'nmtp', 'kran', 'sokol', 12, 'кран-12'),
    # (15125, 'nmtp', 'kran', 'sokol', 13, 'кран-13'),
    # (4934,  'nmtp', 'kran', 'sokol', 20, 'кран-20'),
    # (5908,  'nmtp', 'kran', 'sokol', 22, 'кран-22'),
    # (32046, 'nmtp', 'usm', 'PowerTrack', 1, 'PowerTrack-1'),
    # (32047, 'nmtp', 'usm', 'PowerTrack', 2, 'PowerTrack-2'),
    # (32711, 'nmtp', 'usm', 'Edge', 3, 'Edge-3'),
    # (32740, 'nmtp', 'usm', 'Edge', 4, 'Edge-4'),
    # (32770, 'nmtp', 'usm', 'Screen', 5, 'Screen-5'),
    # (32771, 'nmtp', 'usm', 'Screen', 6, 'Screen-6'),
    # (32772, 'nmtp', 'usm', 'Screen', 7, 'Screen-7'),
    # (32773, 'nmtp', 'usm', 'Screen', 8, 'Screen-8'),
    # (32941, 'nmtp', 'usm', 'Electric', 9, 'Electric-9'),
    # (32942, 'nmtp', 'usm', 'Electric', 10, 'Electric-10'),
    # (33287, 'nmtp', 'usm', 'Edge', 11, 'Edge-11'),
    # (34213, 'nmtp', 'usm', 'Edge', 12, 'Edge-12'),
    # (34214, 'nmtp', 'usm', 'Edge', 13, 'Edge-13'),
    # (32777, 'nmtp', 'sennebogen', '860', 1, 'Sennebogen-1'),
    # (32778, 'nmtp', 'sennebogen', '860', 2, 'Sennebogen-2'),
    # (33297, 'nmtp', 'sennebogen', '860', 3, 'Sennebogen-3'),
    # (33428, 'nmtp', 'sennebogen', '860', 4, 'Sennebogen-4'),
    # (33429, 'nmtp', 'sennebogen', '860', 5, 'Sennebogen-5'),
    # (33522, 'nmtp', 'sennebogen', '860', 6, 'Sennebogen-6'),
    # (33611, 'nmtp', 'sennebogen', '860', 7, 'Sennebogen-7'),
    # (33609, 'nmtp', 'sennebogen', '860', 8, 'Sennebogen-8'),
    # (33610, 'nmtp', 'sennebogen', '860', 9, 'Sennebogen-9'),
]

for id, company, type, model, number, name in mech:
    db.session.add(Mechanism(id, company, type, model, number, name))
    print(id, company, type, model, number, name)

# for id, username, password in users:
#     db.session.add(User(id, username, password))

# for p in User.query.all():
#     db.session.delete(p)

# work_1c = [(2, 33287, 111, 5, 'Петров Ф. А.'),
#       (1, 5908, 112, 8, 'Иванов Ф. А.')]

# for id, inv_num, greifer_num, greifer_vol, fio  in work_1c:
#     start = datetime.now() - timedelta(hours=5)
#     finish = datetime.now() + timedelta(hours=5)
#     date_shift, shift =  today_shift_date()
#     db.session.add(Work_1C_1(id, inv_num, greifer_num, greifer_vol, fio, start, finish, date_shift, shift))


db.session.commit()

# m = Mechanism(32777, company='nmtp', type='sennebogen', model='860', number=1, name='Sennebogen-1')
a = [mech.id for mech in Mechanism.query.all()]
print(a)
# b = [(user.username, user.password_hash) for user in User.query.all()]
# print('---------------')
# print(b)
