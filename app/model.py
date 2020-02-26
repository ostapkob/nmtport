from app import db
from datetime import datetime, timedelta


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
    # timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    timestamp = db.Column(db.DateTime, index=True)
    date_shift = db.Column(db.Date)
    shift = db.Column(db.Integer)
    # this column must form by GPS
    terminal = db.Column(db.SmallInteger, index=True)

    def __init__(self, mechanism_id, latitude=0, longitude=0, value=None,value2=None, value3=None,  timestamp=None):
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
        self.latitude = latitude
        self.longitude = longitude
        self.mechanism_id = mechanism_id
        self.shift = shift
        self.date_shift = date_shift
        self.terminal = terminal

        d = str(timestamp) + " " + str(hour) + " " + str(date_shift) + " " + str(shift)
        with open('post.txt', 'w') as f:
            f.write(d)


    def __repr__(self):
        return f'{self.value}'

    def add_post(self):
        print(super().get_tables_for_bind())
        # print(super().)

