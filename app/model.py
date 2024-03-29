from app import db, login
from datetime import datetime, timedelta, date
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from config import HOURS
from typing import Tuple


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
    timestamp = db.Column(db.DateTime, index=True)
    date_shift = db.Column(db.Date, index=True)
    shift = db.Column(db.Integer, index=True)
    terminal = db.Column(db.SmallInteger, index=True)

    def __init__(self, mechanism_id, latitude=0, longitude=0, value=None, value2=None, value3=None, count=None, terminal=0, timestamp=None):
        if timestamp:
            self.timestamp = timestamp
        elif timestamp is None:
            self.timestamp = datetime.now()
        self.value = value
        self.value2 = value2
        self.value3 = value3
        self.count = count
        self.latitude = latitude
        self.longitude = longitude
        self.mechanism_id = mechanism_id
        self.date_shift, self.shift = self._get_date_and_shift()
        self.terminal = terminal
        # delete after update all mechanism api
        self.timestamp -= timedelta(hours=HOURS)
        d = f'{self.date_shift} | {self.shift}: {self.mechanism_id} - {value}, {value2}, {value3}, {count}, {latitude}, {longitude}'
        with open('logs/post.txt', 'w') as f:  # little test
            f.write(d)

    def __repr__(self):
        return f'{self.timestamp} {self.value} '

    def _get_date_and_shift(self) -> Tuple[date, int]:
        hour = self.timestamp.hour
        if hour >= 8 and hour < 20:
            date_shift = self.timestamp.date()
            shift = 1
        elif hour < 8:
            date_shift = self.timestamp.date() - timedelta(days=1)
            shift = 2
        else:
            date_shift = self.timestamp.date()
            shift = 2
        return date_shift, shift

    def add_post(self):
        print(super().get_tables_for_bind())


class User(UserMixin, db.Model):
    # not use
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
    greifer_num = db.Column(db.Integer, index=True)
    greifer_vol = db.Column(db.Integer, index=True)
    fio = db.Column(db.String(64), index=True)
    data_nach = db.Column(db.DateTime, index=True)
    data_kon = db.Column(db.DateTime, index=True)
    data_smen = db.Column(db.DateTime, index=True)
    smena = db.Column(db.Integer, index=True)
    port = db.Column(db.Integer, index=True)

    def __init__(self, id, inv_num, greifer_num, greifer_vol, fio, data_nach, data_kon, data_smen, smena, port):
        self.id = id
        self.inv_num = inv_num
        self.greifer_num = greifer_num
        self.greifer_vol = greifer_vol
        self.fio = fio
        self.data_nach = data_nach
        self.data_kon = data_kon
        self.data_smen = data_smen
        self.smena = smena
        self.port = port

    def __repr__(self):
        return f'{self.inv_num}, {self.greifer_num}, {self.greifer_vol},\
                {self.fio}, {self.data_nach}, {self.data_kon},\
                {self.data_smen}, {self.smena}, {self.port}'

    def get(self):
        return [self.inv_num, self.greifer_num, self.greifer_vol, self.fio, self.data_nach, self.data_kon, self.data_smen, self.smena, self.port]


class Mechanism_downtime_1C(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inv_num = db.Column(db.Integer, index=True)
    data_smen = db.Column(db.DateTime)
    smena = db.Column(db.Integer)
    data_nach = db.Column(db.DateTime)
    data_kon = db.Column(db.DateTime)
    id_downtime = db.Column(db.Integer)

    def __init__(self, id, inv_num, data_smen, smena, data_nach, data_kon, id_downtime):
        self.id = id
        self.inv_num = inv_num
        self.data_smen = data_smen
        self.smena = smena
        self.data_nach = data_nach
        self.data_kon = data_kon
        self.id_downtime = id_downtime

    def __repr__(self):
        return f'{self.inv_num}, {self.data_smen}, {self.smena}, {self.data_nach}, {self.data_kon}, {self.id_downtime}'

    def get(self):
        return [self.inv_num, self.data_smen, self.smena, self.data_nach, self.data_kon, self.id_downtime]


class Downtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'{self.id}, {self.name}'

    def get(self):
        return [self.id, self.name]


class Rfid_work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mechanism_id = db.Column(db.Integer, db.ForeignKey('mechanism.id'))
    # rfid_id = db.Column(db.String(10), db.ForeignKey('rfid_ids.rfid_id'))
    count = db.Column(db.Integer)
    rfid_id = db.Column(db.String(10))
    flag = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, index=True)
    date_shift = db.Column(db.Date, index=True)
    shift = db.Column(db.Integer, index=True)

    def __init__(self, mechanism_id, count, rfid_id, flag, timestamp=None):
        self.timestamp = timestamp or datetime.now()
        self.mechanism_id = mechanism_id
        self.count = count
        self.rfid_id = rfid_id
        self.flag = flag
        self.date_shift, self.shift = self._get_date_and_shift()

    def __repr__(self):
        return f'{str(self.timestamp.strftime("%d.%m.%Y %H:%M:%S"))} | {self.date_shift} | {self.shift} | {self.id} | {self.mechanism_id} | {self.count} | {self.rfid_id} | {self.flag}'

    def get(self):
        return [self.mechanism_id, self.count, self.rfid_id, self.flag, self.timestamp]

    def _get_date_and_shift(self) -> Tuple[date, int]:
        hour = self.timestamp.hour
        if hour >= 8 and hour < 20:
            date_shift = self.timestamp.date()
            shift = 1
        elif hour < 8:
            date_shift = self.timestamp.date() - timedelta(days=1)
            shift = 2
        else:
            date_shift = self.timestamp.date()
            shift = 2
        return date_shift, shift


class Rfid_ids(db.Model):
    rfid_id = db.Column(db.String(10), primary_key=True)  # format 12,345678
    fio = db.Column(db.String(64))

    def __init__(self, rfid_id, fio):
        self.rfid_id = rfid_id
        self.fio = fio

    def __repr__(self):
        return f'{self.rfid_id}, {self.fio}'
