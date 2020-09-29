from app import db, login
from datetime import datetime, timedelta
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Mechanism(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(64), index=True)
    type = db.Column(db.String(64), index=True)
    model = db.Column(db.String(64), index=True)
    number = db.Column(db.SmallInteger, index=True)  # 32768 should be enough
    name = db.Column(db.String(64), index=True, unique=True)
    posts = db.relationship('Post', backref='mech', lazy='dynamic')

    def __init__(self, id, company, type, model, number, name):
        self.id = id
        self.company = company
        self.type = type
        self.model = model
        self.number = number
        self.name = name

    def __repr__(self):
        return f'<{self.name}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mechanism_id = db.Column(db.Integer, db.ForeignKey('mechanism.id'))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    value = db.Column(db.Float)
    value2 = db.Column(db.Float)
    value3 = db.Column(db.Integer)
    count = db.Column(db.Integer)
    # timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    timestamp = db.Column(db.DateTime, index=True)
    date_shift = db.Column(db.Date)
    shift = db.Column(db.Integer)
    # this column must form by GPS
    terminal = db.Column(db.SmallInteger, index=True)

    def __init__(self, mechanism_id, latitude=0, longitude=0, value=None, value2=None, value3=None, count=None,  timestamp=None):
        hour = datetime.now().hour
        if hour >= 8 and hour < 20:
            date_shift = datetime.now()
            shift = 1
        elif hour < 8:
            date_shift = datetime.now() - timedelta(days=1)
            shift = 2
        else:
            date_shift = datetime.now()
            shift = 2

        terminal = 1  # this column must form by GPS, may be
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.utcnow()
        self.value = value
        self.value2 = value2
        self.value3 = value3
        self.count = count
        self.latitude = latitude
        self.longitude = longitude
        self.mechanism_id = mechanism_id
        self.shift = shift
        self.date_shift = date_shift
        self.terminal = terminal

        # d = str(date_shift) + ": " + str(latitude) +', ' + str(longitude) + ', '  + str(value) + ', ' + str(value2) + ', ' + str(value3)
        # d = date_shift + ": " + latitude +', ' + longitude + ', '  + value + ', ' + value2 + ', ' + value3
        d = f'{date_shift}: {self.mechanism_id} - {value}, {value2}, {value3}, {count}, {latitude}, {longitude}'
        with open('post.txt', 'w') as f:
            f.write(d)

    def __repr__(self):
        return f'{self.timestamp} {self.value} '

    def add_post(self):
        print(super().get_tables_for_bind())
        # print(super().)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = generate_password_hash(password_hash)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)




class Work_1C_1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inv_num = db.Column(db.Integer, index=True)
    greifer_num =db.Column(db.Integer, index=True)
    greifer_vol =db.Column(db.Integer, index=True)
    fio=db.Column(db.String(64), index=True)
    data_nach = db.Column(db.DateTime, index=True)
    data_kon = db.Column(db.DateTime, index=True)

    def __init__(self, id, inv_num, greifer_num, greifer_vol, fio, data_nach, data_kon):
        self.id = id
        self.inv_num = inv_num
        self.greifer_num =greifer_num
        self.greifer_vol =greifer_vol
        self.fio=fio
        self.data_nach =data_nach
        self.data_kon =data_kon

    def __repr__(self):
        # return f'{self.inv_num}, {self.greifer_num}, {self.greifer_vol}, {self.fio}, {self.data_nach}, {self.data_kon}'
        return [self.inv_num, self.greifer_num, self.greifer_vol, self.fio, self.data_nach, self.data_kon]

    def get(self):
        return [self.inv_num, self.greifer_num, self.greifer_vol, self.fio, self.data_nach, self.data_kon]

