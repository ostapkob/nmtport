from app import db
from datetime import datetime, timedelta


class Mechanism(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(64), index=True)
    type = db.Column(db.String(64), index=True)
    model = db.Column(db.String(64), index=True)
    number = db.Column(db.SmallInteger, index=True)
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
    value = db.Column(db.Float)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # date = db.Column(db.Date,  default=datetime.utcnow)
    # time = db.Column(db.Time,  default=datetime.utcnow)
    date_shift = db.Column(db.Date)
    shift = db.Column(db.Integer)

    def __init__(self, value, latitude, longitude, mechanism_id):
        hour = datetime.now().hour
        if hour > 8 and hour < 20:
            date_shift = datetime.now()
            shift = 1
        elif hour < 8:
            date_shift = datetime.now() - timedelta(days=1)
            shift = 2
        else:
            date_shift = datetime.now()
            shift = 2

        self.value = value
        self.latitude = latitude
        self.longitude = longitude
        self.mechanism_id = mechanism_id
        self.shift = shift
        self.date_shift = date_shift
        print(date_shift)
    def __repr__(self):
        return f'<{self.timestamp}>'


